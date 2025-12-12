import os
import requests
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import classification
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Répertoires
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "frontend", "templates")

# Static & Templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


API_URL ="https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
HF_TOKEN =os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
CATEGORIES = ["Finance", "Politique", "Marketing","Santé","Technologie","Art","Sport","Climat","Éducation"]

class TextInput(BaseModel):
    text: str

def query_huggingface(text: str):
    payload = {"inputs": text, "parameters": {"candidate_labels": CATEGORIES, "multi_label": False}}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"HuggingFace API error: {e}")

@app.post("/classify")
def classify_text(data: TextInput, db: Session = Depends(get_db)):
    result = query_huggingface(data.text)
    
    
    # Traitement robuste des différents formats de HF
    try:
        if isinstance(result, dict) and "labels" in result and "scores" in result:
            category = result["labels"][0]
            score = float(result["scores"][0])
        elif isinstance(result, list) and len(result) > 0 and "label" in result[0] and "score" in result[0]:
            category = result[0]["label"]
            score = float(result[0]["score"])
        else:
            raise HTTPException(status_code=500, detail=f"Format inattendu : {result}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur traitement HF: {e}")

    # Sauvegarde en DB
    entry = classification(input_text=data.text, category=category, score=score)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {"text": data.text, "huggingface_category": category, "huggingface_score": score}

# Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

@app.post("/gemini")
def gemini_AI(data: TextInput):
    try:
        prompt = f"Analyse ce texte et résume-le : {data.text}"
        gemini_result = gemini_model.generate_content(prompt)
        return {"text": data.text, "gemini_analysis": gemini_result.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")

@app.post("/gemini-classify")
def gemini_and_classify(data: TextInput, db: Session = Depends(get_db)):
    try:
        hf_result = query_huggingface(data.text)
        # Traitement robuste HF
        if isinstance(hf_result, dict) and "labels" in hf_result and "scores" in hf_result:
            category = hf_result["labels"][0]
            score = float(hf_result["scores"][0])
        elif isinstance(hf_result, list) and len(hf_result) > 0 and "label" in hf_result[0] and "score" in hf_result[0]:
            category = hf_result[0]["label"]
            score = float(hf_result[0]["score"])
        else:
            raise HTTPException(status_code=500, detail=f"Format inattendu HF : {hf_result}")

        # Sauvegarde en DB
        entry = classification(input_text=data.text, category=category, score=score)
        db.add(entry)
        db.commit()
        db.refresh(entry)

        # Analyse Gemini
        prompt = f"Analyse ce texte et explique pourquoi il est classé dans '{category}' : {data.text}"
        gemini_result = gemini_model.generate_content(prompt)

        return {
            "text": data.text,
            "huggingface_category": category,
            "huggingface_score": score,
            "gemini_analysis": gemini_result.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
