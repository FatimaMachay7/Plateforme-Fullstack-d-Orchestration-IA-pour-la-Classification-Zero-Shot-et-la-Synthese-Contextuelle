 async function classifyText() {
        const text = document.getElementById('text').value;

        try {
            const response = await fetch( "http://127.0.0.1:8000/classify", { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            if (!response.ok) {
                const error = await response.json();
                document.getElementById('result').innerText = "Erreur : " + error.detail;
                return;
            }

            const data = await response.json();

            document.getElementById('result').innerText =
                `Catégorie: ${data.category} et Score: ${data.score.toFixed(2)}`;
        
        } catch (err) {
            document.getElementById('result').innerText = "Erreur de connexion serveur.";
        }
    }
async function gemini() {
    const prompt =document.getElementById('geminiPrompt').value;
    try {
        const response= await fetch ("http://127.0.0.1:8000/gemini", {
            method: 'PORT',
            headers: {'Content-Type':' application/json'},
            body: JSON.stringify({ "prompt": "hello"
            })
        });
        if (!response.ok) {
            const error = await response.json();
            document.getElementById('geminiResponse').innerText= "Erreur :" + (error.detail|| "Problème serveur");
            return
        }
        const data = await response.json();
        document.getElementById('geminiResponse').innerText = data.response;
    } catch (err) {
        document.getElementById('geminiResponse').innerText ="Erreur  de connexion serveur.";
    } 
}