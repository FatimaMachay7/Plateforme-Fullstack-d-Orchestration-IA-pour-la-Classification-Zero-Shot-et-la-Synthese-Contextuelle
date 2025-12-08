from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client= TestClient(app)
@patch("main.query_huggingface")
def test_classify_status_code(mock_query):
    mock_query.return_value = [{"label":"technologie", "score": 0.96}]
    response= client.post("/classify", json={"text":"Hello world"})
    assert response.status_code ==200
    assert response.json()== {"category": "technologie", "score":0.96}