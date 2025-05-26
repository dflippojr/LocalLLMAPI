from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class Prompt(BaseModel):
    prompt: str
    model: str = "deepseek-r1"  # Default model if none specified

@app.get("/models")
def list_models():
    try:
        res = requests.get("http://ollama:11434/api/tags")
        return res.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Ollama: {str(e)}")

@app.post("/generate")
def generate(req: Prompt):
    try:
        data = {"model": req.model, "prompt": req.prompt}
        res = requests.post("http://ollama:11434/api/generate", json=data)
        return res.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Ollama: {str(e)}")
