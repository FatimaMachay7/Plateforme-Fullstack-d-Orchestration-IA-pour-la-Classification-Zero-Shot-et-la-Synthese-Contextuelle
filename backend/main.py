import os
import requests
from fastapi import FastAPI, HTTPException,  Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import classification
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# HuggingFace
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

CATEGORIES = ["Finance", "Politique", "Marketing","Santé","Technologie","Art","Sport","Climat","Éducation"]

class TextInput(BaseModel):
    text: str

def query_huggingface(text: str):
    payload = {"inputs": text,"parameters":{"candidate_labels": CATEGORIES,"multi_label": False}}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"HuggingFace API error: {e}")

@app.post("/classify")
def classify_text(data: TextInput, db: Session = Depends(get_db)):
    result = query_huggingface(data.text)
    if not isinstance(result, list) or len(result) == 0:
        raise HTTPException(status_code=500, detail=f"Format inattendu : {result}")
    category = result[0]["label"]
    score = float(result[0]["score"])
    entry = classification(input_text=data.text, category=category, score=score)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"text": data.text, "huggingface_category": category, "huggingface_score": score}

# Gemini
API_KEY= os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

@app.post("/gemini")
def gemini_AI(data: TextInput):
    prompt = f"Analyse ce texte et résume- le : {data.text}"
    gemini_result = gemini_model.generate_content(prompt)
    return {"text": data.text, "gemini_analysis": gemini_result.text}

@app.post("/gemini-classify")
def gemini_and_classify(data: TextInput):
    try:
        payload = {"inputs": data.text,"parameters":{"candidate_labels": CATEGORIES,"multi_label": False}}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code !=200:
            return {"error": f"HuggingFace API error {response.status_code} : {response.text}"}
        hf_response = response.json()
        category = hf_response[0]["label"]
        score = float(hf_response[0]["score"])
        prompt = f"Analyse ce texte et explique pourquoi il est classé dans '{category}' : {data.text}"
        resultat_gemini = gemini_model.generate_content(prompt)
        return {"text": data.text, "huggingface_category": category, "huggingface_score": score, "gemini_analysis": resultat_gemini.text}
    except Exception as e:
        return {"error": str(e)}
