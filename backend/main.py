import os
import json
import httpx
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="IoT Agent API", version="1.0")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

class SensorData(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    timestamp: str
    location: str

async def analyze_with_groq(temperature: float, humidity: float) -> dict:
    """Appelle Groq LLM pour analyser les données capteur"""
    prompt = f"""
    Tu es un agent IA IoT qui analyse des données de capteurs.

    Données reçues:
    - Température: {temperature}°C
    - Humidité: {humidity}%

    Règles:
    - Température normale: 18-25°C
    - Température élevée: 25-30°C
    - Température critique: >30°C
    - Humidité normale: 40-60%

    Réponds UNIQUEMENT en JSON avec ce format:
    {{
        "status": "normal|warning|critical",
        "severity": "low|medium|high|critical",
        "action": "action recommandée",
        "reason": "explication courte"
    }}
    """

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Tu es un agent IoT expert. Réponds uniquement en JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 200
            }
        )

        if response.status_code != 200:
            return {
                "status": "unknown",
                "severity": "low",
                "action": "Vérifier manuellement",
                "reason": f"Erreur API Groq: {response.status_code}"
            }

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # Extraire le JSON de la réponse
        try:
            # Nettoyer si le LLM a mis du markdown
            content = content.replace("```json", "").replace("```", "").strip()
            analysis = json.loads(content)
            return analysis
        except:
            return {
                "status": "unknown",
                "severity": "low",
                "action": "Vérifier manuellement",
                "reason": "Réponse LLM non parsable"
            }

@app.post("/ingest")
async def ingest_data(data: SensorData):
    """Reçoit les données du simulateur, analyse avec Groq, stocke dans Supabase"""

    # Analyse avec Groq
    analysis = await analyze_with_groq(data.temperature, data.humidity)

    # Préparer l'enregistrement
    record = {
        "device_id": data.device_id,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "timestamp": data.timestamp,
        "location": data.location,
        "status": analysis["status"],
        "severity": analysis["severity"],
        "action": analysis["action"],
        "reason": analysis["reason"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    # Insérer dans Supabase
    result = supabase.table("sensor_readings").insert(record).execute()

    return {
        "success": True,
        "analysis": analysis,
        "record": record
    }

@app.get("/data")
async def get_data(limit: int = 100):
    """Récupère les dernières données pour le dashboard"""
    result = supabase.table("sensor_readings").select("*").order("created_at", desc=True).limit(limit).execute()
    return result.data

@app.get("/health")
async def health():
    return {"status": "ok", "service": "iot-agent-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"# Redeploy" 
