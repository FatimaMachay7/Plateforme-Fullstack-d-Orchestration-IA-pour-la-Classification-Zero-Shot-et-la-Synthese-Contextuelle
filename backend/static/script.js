const API_BASE = "http://127.0.0.1:8000";

function getText() {
    return document.getElementById("inputText").value;
}

function showResult(data) {
    const box = document.getElementById("resultBox");
    box.textContent = JSON.stringify(data, null, 2);
    console.log("Résultat :", data);
}

function showError(error) {
    document.getElementById("resultBox").textContent = "❌ ERREUR : " + error;
    console.error(error);
}

async function classifyText() {
    try {
        const text = getText();
        if (!text) return alert("Veuillez écrire un texte.");
        const res = await fetch(`${API_BASE}/classify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        showResult(data);
    } catch (e) {
        showError(e);
    }
}

async function analyzeGemini() {
    try {
        const text = getText();
        if (!text) return alert("Veuillez écrire un texte.");
        const res = await fetch(`${API_BASE}/gemini`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        showResult(data);
    } catch (e) {
        showError(e);
    }
}

async function classifyAndGemini() {
    try {
        const text = getText();
        if (!text) return alert("Veuillez écrire un texte.");
        const res = await fetch(`${API_BASE}/gemini-classify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        showResult(data);
    } catch (e) {
        showError(e);
    }
}
