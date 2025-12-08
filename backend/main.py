import os
import requests 
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database import get_db
from models import classification
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

load_dotenv()  # <-- obligatoire pour charger HF_TOKEN

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
# Le modél Hugging Face


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

# Le Gemini API :
# Charger la clé API depuis .env

class Prompt(BaseModel):
    text: str
class Geminirequest(BaseModel):
    prompt:str
    
API_KEY= os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model= genai.GenerativeModel("gemini-2.5-flash")
@app.post("/gemini")
def gemini_AI(data :Geminirequest):
    response= model.generate_content(data.prompt)
    return {"reponse": response.text}