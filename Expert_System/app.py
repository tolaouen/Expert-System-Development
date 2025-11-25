from flask import Flask, jsonify, request
from jsonschema import validate, ValidationError
import json
import os 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_ROOT, 'data')
os.makedirs(DATA_DIR, exist_ok=True)


fact_array_schema = {
    "$schema": "https://json_schema.org/draft/2020-12/schema",
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "description", "value"],
        "properties": {
            "id": {"type": "string"},
            "description": {"type": "string"},
            "value": {"type": "boolean"},
            "tags": {"type": "array", "items": {"type": "string"}}
        }
    }
}

rule_array_schema = {
    "$schema": "https://json_schema.org/draft/2020-12/schema",
    "type": "array", 
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "conditions", "conclusion"], # Fixed: added "conditions"
        "properties": {
            "id": {"type": "string", "minLength": 1},
            "conditions": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string", "minLength": 1}
            },
            "conclusion": {"type": "string", "minLength": 1},
            "certainty": {"type": "number", "minimum": 0, "maximum": 1},
            "explain": {"type": "string"}
        }
    }
}

def load_json(filename: str):
    """Load JSON from ./data/<filename>."""

    path= os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"Require file not Found: {path}")
    
def error_payload(e: ValidationError, filelabel:str):
    """Produce rich error payload for schema validation"""
    return {
        "file": filelabel,
        "message": e.message,
        "path": list(e.path),
        "schema_path": list(e.schema_path)
    }

def clamp01(x: float)-> float:
    """Clamp numberic confidence to [0, 1]."""

    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0
    
try:

    facts = load_json('facts.json')
    rules = load_json('rules.json')
    taxonomy = load_json('taxonomy.json')

except FileNotFoundError as e:
    print(f"ERROR: {e}")
    print("Please ensure data/facts.json, data/rules.json, and data/taxonomy.json exist.")
    exit(1)

try:
    validate(instance=facts, schema=fact_array_schema)
    validate(instance=rules, schema=rule_array_schema)
except ValidationError as e:
    print(f"ERROR: Data validation failed: {e.message}")
    exit(1)

PARENT = taxonomy.get("parent", {})
FACT_VALUE = {f["id"]: bool(f["value"]) for f in facts}  

def ancestors(concept: str):
    """Yield all ancestors of a concept in the taxonomy."""
    seen = set()
    cur = concept
    
    while cur in PARENT and PARENT[cur] not in seen:
        parent = PARENT[cur]
        seen.add(parent)
        yield parent
        cur = parent

def expand_observations(obs_conf: dict)-> dict:
    """Propagate observation confidences up the taxonomy. """
    if not PARENT:
        return obs_conf
    expanded = dict(obs_conf)
    for fid, c in list(obs_conf.items()):
        for anc in ancestors(fid):
            expanded[anc] = max(expanded.get(anc, 0.0), c)
    return expanded

def evaluate_rule(rule: dict, obs_conf: dict):
    """Return (fires:boolean, score:float)"""
    cond_ids = rule.get("conditions", [])
    if not cond_ids:
        return (False, 0.0  )
    
    cond_scores = []
    for cid in cond_ids:
        c = clamp01(obs_conf.get(cid, 0.0 ))
        if c <= 0.0:
            return (False, 0.0 )
        cond_scores.append(c)
    
    base = min(cond_scores)
    cf = clamp01(rule.get("certainty", 1.0))
    return (True, base * cf)

app = Flask(__name__)

@app.get("/health/")
def health():
    return jsonify({"status": "ok"})

@app.get("/facts/")
def get_facts():
    """Return all facts from data/facts.json"""
    return jsonify(facts)

@app.get("/rules/")
def get_rules():
    """Return all rules from data/rules.json"""
    return jsonify(rules)

@app.route("/validate/", methods=["GET", "POST"])
def validate_payloads():
    """Validate facts and/or rules against schemas"""
    if request.method == "GET":
        return jsonify({
            "usage": "POST JSON with 'facts' and/or 'rules' to validate.",
            "schemas": ["facts_array_schema", "rule_array_schema"]

        })

    payload = request.get_json(force=True, silent=True) or {}
    errors = []

    if "facts" in payload:
        try: 
            validate(payload["facts"], fact_array_schema)
        except ValidationError as e:
            errors.append(error_payload(e, "facts"))

    return jsonify({"valid": len(errors) == 0, "errors": errors})

@app.route("/infer/", methods=["GET", "POST"])
def infer():
    """
    Inference endpoint supporting both GET and POST.

    GET: https://127.0.0.1:5000/infer/?facts=f1,f2&weight=f1:1.0,f2:0.8&useTrueFacts=false
    POST: JSON body with facts , useTrueFacts
 
   """
    
    if request.method == "GET":
        
        facts_param = request.args.get("facts", "")
        weights_param = request.args.get("weights", "")
        use_true_facts = request.args.get("useTrueFacts", "false").lower() == "true"
        observed_ids = set(f.strip() for f in facts_param.split(",") if f.strip())
        weights = {}
        if weights_param:
            for pair in weights_param.split(","):
                if ":" in pair:
                    fid, conf = pair.split(":", 1)
                    try:
                        weights[fid.strip()] = float(conf.strip())
                    except ValueError:
                        pass

    else:
        payload = request.get_json(force=True, silent=True) or {}
        observed_ids = set(payload.get("facts"), [])
        weights = payload.get("weights", {})
        use_true_facts = bool(payload.get("useTrueFacts", False))

    if use_true_facts:
        observed_ids.update(fid for fid, val in FACT_VALUE.items() if val is True)

    obs_conf = {}
    for fid in observed_ids:
        obs_conf[fid] = clamp01(weights.get(fid, 1.0))

    obs_conf = expand_observations(obs_conf)

    fired = []
    for rule in rules:
        fires, score = evaluate_rule(rule, obs_conf)
        if fires and score > 0.0:
            fired.append({
                "rule": rule["id"],
                "conclusion": rule["conclusion"],
                "score": round(score, 3),
                "explain": rule.get("explain", ""),
                "conditions": rule.get("conditions", [])
            })

    aggregate = {}
    for r in fired:
        k = r["conclusion"]
        aggregate[k] = max(aggregate.get(k, 0.0), r["score"])

    ranked = sorted(
        [{"conclusion": k, "score": round(v, 3)} for k, v in aggregate.items()],
        key=lambda x: x["score"],
        reverse=True 
    )

    return jsonify({
        "matched_rules": fired,
        "ranked_conclusions": ranked,
        "observations": [{"id": k, "confidence": v} for k, v in sorted(obs_conf.items())]
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG") == "1"
    )


    

