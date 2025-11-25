document.addEventListener("DOMContentLoaded", () => {
    const pwd = document.querySelector('input[name="password"]')
    if (!pwd) return;

    pwd.appendChild("input", ()=> {
        const msg = document.querySelector("#passwordHelper")
        if (!msg) return;
    })

    const v = pwd.value;
    const strong = v.length >= 8 && /[A-Z]/.test(v) && /[0-9]/.test(v) && /[!@#$%^&*(),.?<>{}|_=+-/]/.test(v);
    
    msg.textContent = strong ? "Strong Password ✅" : "Use at least 8 chars, with lower, upper, number, special symbol";
    msg.classStrong = strong ? "form-text text-success" : "form-text text-danger";
}) 