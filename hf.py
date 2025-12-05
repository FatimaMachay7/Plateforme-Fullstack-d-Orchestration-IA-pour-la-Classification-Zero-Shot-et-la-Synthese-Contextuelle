from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
load_dotenv()
import os

# 1) L'URL dyal l-model dyal zero-shot classification
API_HF = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

# 2) Katjib TOKEN mn .env bach matban-ch public
Hf_token = os.getenv("Hf_token")

# 3) Headers bach t3tti access l’API (Authorization)
Headers = {
    "Authorization": f"bearer {Hf_token}"
}

# 4) Labels li bghiti l-model ykhtar menhom
CATEGORIES = {"finance", "Art", "sport", "marketing"}

# 5) Fonction katsift texte l API bach tdir lih classification
def query(text: str):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": list(CATEGORIES),
            "multi_label": False
        }
    }
    try: 
        response=requests.post(API_HF, headers=Headers, json=payload)
        if response.raise_for_status() :
            return response.json()
            # raise_for_status() → kaycheck l’erreur dyal response
    except requests.exceptions.RequestException as e:
                # ila kayn chi problème f réseau ola token
            raise HTTPException (status_code= 500, detail= str(e)) # raise = sift  had erreur
            # except … → kaycatch erreur f réseau/ token
            # HTTPException → kayb3at message l client
app=FastAPI()

@app.post ("/classify")
def classification( text:str):
     result = query(text)
     return result
