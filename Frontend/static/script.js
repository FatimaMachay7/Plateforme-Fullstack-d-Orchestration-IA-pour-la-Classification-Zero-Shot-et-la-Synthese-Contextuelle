// script.js - SIMPLE

// L'adresse de votre serveur
const serveur = 'http://localhost:8000';

// Récupérer les éléments de la page
const monTexte = document.getElementById('monTexte');
const btnClassifier = document.getElementById('btnClassifier');
const btnGemini = document.getElementById('btnGemini');
const btnTout = document.getElementById('btnTout');
const chargement = document.getElementById('chargement');
const resultat = document.getElementById('resultat');

// Fonction 1 : Classifier le texte
btnClassifier.onclick = function() {
    // Récupérer le texte
    const texte = monTexte.value;
    
    // Vérifier si le texte n'est pas vide
    if (texte === '') {
        alert('Écrivez du texte avant de classifier !');
        return;
    }
    
    // Afficher le chargement
    chargement.style.display = 'block';
    resultat.style.display = 'none';
    
    // Envoyer au serveur
    fetch(serveur + '/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: texte })
    })
    .then(response => response.json())
    .then(data => {
        // Cacher le chargement
        chargement.style.display = 'none';
        
        // Afficher le résultat
        resultat.style.display = 'block';
        resultat.innerHTML = `
            <div class="info">
                <strong>Catégorie :</strong> ${data.huggingface_category}
            </div>
            <div class="info">
                <strong>Score :</strong> ${Math.round(data.huggingface_score * 100)}%
            </div>
        `;
    })
    .catch(error => {
        chargement.style.display = 'none';
        resultat.style.display = 'block';
        resultat.innerHTML = '<p style="color: red;">Erreur : ' + error + '</p>';
    });
};

// Fonction 2 : Analyser avec Gemini
btnGemini.onclick = function() {
    const texte = monTexte.value;
    
    if (texte === '') {
        alert('Écrivez du texte avant d\'analyser !');
        return;
    }
    
    chargement.style.display = 'block';
    resultat.style.display = 'none';
    
    fetch(serveur + '/gemini', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: texte })
    })
    .then(response => response.json())
    .then(data => {
        chargement.style.display = 'none';
        resultat.style.display = 'block';
        resultat.innerHTML = `
            <div class="info">
                <strong>Analyse :</strong><br>
                ${data.gemini_analysis}
            </div>
        `;
    })
    .catch(error => {
        chargement.style.display = 'none';
        resultat.style.display = 'block';
        resultat.innerHTML = '<p style="color: red;">Erreur : ' + error + '</p>';
    });
};

// Fonction 3 : Tout faire en même temps
btnTout.onclick = function() {
    const texte = monTexte.value;
    
    if (texte === '') {
        alert('Écrivez du texte !');
        return;
    }
    
    chargement.style.display = 'block';
    resultat.style.display = 'none';
    
    fetch(serveur + '/gemini-classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: texte })
    })
    .then(response => response.json())
    .then(data => {
        chargement.style.display = 'none';
        resultat.style.display = 'block';
        resultat.innerHTML = `
            <div class="info">
                <strong>Catégorie :</strong> ${data.huggingface_category}
            </div>
            <div class="info">
                <strong>Score :</strong> ${Math.round(data.huggingface_score * 100)}%
            </div>
            <div class="info">
                <strong>Analyse :</strong><br>
                ${data.gemini_analysis}
            </div>
        `;
    })
    .catch(error => {
        chargement.style.display = 'none';
        resultat.style.display = 'block';
        resultat.innerHTML = '<p style="color: red;">Erreur : ' + error + '</p>';
    });
};