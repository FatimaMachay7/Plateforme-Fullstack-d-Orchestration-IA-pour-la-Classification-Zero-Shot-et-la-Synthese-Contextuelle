import os
import requests 
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from database import get_db
from models import classification
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # <-- obligatoire pour charger HF_TOKEN

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

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
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()
    
    
@app.post("/classify", response_model=ClassificationResponse)
def classify_text(input_data: TextInput, db: Session = Depends(get_db)):
    result = query_huggingface(input_data.text)

    # HuggingFace renvoie une liste de dicts [{'label': ..., 'score': ...}, ...]
    if not isinstance(result, list) or len(result) == 0:
        raise HTTPException(status_code=500, detail=f"Format inattendu : {result}")

    # On prend le premier élément (catégorie principale)
    category = result[0]["label"]
    score = float(result[0]["score"])

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