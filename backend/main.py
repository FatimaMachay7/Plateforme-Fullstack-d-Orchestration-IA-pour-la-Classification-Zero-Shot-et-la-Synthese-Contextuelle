import os
import requests 
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from database import get_db
from models import Base, classification
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

HF_TOKEN = os.getenv("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}
templates = Jinja2Templates(directory="templates")
CATEGORIES = [
    "Finance", "Politique", "Marketing",
    "Santé", "Technologie",
    "Art", "Sport", "Climat","Éducation"
]

class TextInput(BaseModel):
    text: str

class ClassificationResponse(BaseModel):
    category: str
    score: float


@app.get("/")
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def query_huggingface(text: str):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": CATEGORIES,
            "multi_label": False
        }
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion HuggingFace : {e}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"HuggingFace API failed: {response.text}"
        )

    try:
        result = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail=f"Réponse non JSON : {response.text}")

    return result

@app.post("/classify", response_model=ClassificationResponse)
def classify_text(input_data: TextInput, db: Session = Depends(get_db)):
    result = query_huggingface(input_data.text)

    # Si HuggingFace renvoie une erreur
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    # Vérifier le format normal
    if not isinstance(result, list) or len(result) == 0:
        raise HTTPException(status_code=500, detail=f"Format inattendu : {result}")

    item = result[0]

    if "label" not in item or "score" not in item:
        raise HTTPException(status_code=500, detail=f"Format invalide : {item}")

    category = item["label"]
    score = float(item["score"])

    # Sauvegarde BDD
    entry = classification(
        input_text=input_data.text,
        category=category,
        score=score
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {"category": category, "score": score}


