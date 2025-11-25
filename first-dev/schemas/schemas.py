
facts_array_schema = {
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

rules_array_schema = {
    "$schema": "https://json_schema.org/draft/2020-12/schema",
    "type": "array", 
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "conditions", "conclusion"], 
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