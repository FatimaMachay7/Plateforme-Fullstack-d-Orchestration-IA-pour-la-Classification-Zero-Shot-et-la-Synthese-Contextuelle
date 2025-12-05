# import os
# import requests
# from dotenv import load_dotenv
# from fastapi import FastAPI
# app=FastAPI()

# load_dotenv()
# API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
# headers = {
#     "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
# }

# def query(text :str):
#     response = requests.post(API_URL, headers=headers, json={
#     "inputs": text,
#     "parameters": {"candidate_labels": ["refund", "legal", "faq"]},
# })
#     return response.json()

# output = query("Je suis hahah")
# print (output)

# @app.post('/huggingface')
# def hugginface(text:str):
#     resu= query(text)
#     return resu