import time
import random
import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# URL du backend API (à configurer après déploiement)
API_URL = os.getenv("API_URL", "http://localhost:8000")

def simulate_sensor():
    print("✅ Simulateur démarré")
    print(f"📡 Envoie vers: {API_URL}/ingest")

    try:
        while True:
            # Simulation de données capteur
            temperature = round(random.uniform(18.0, 38.0), 1)
            humidity = round(random.uniform(30.0, 85.0), 1)

            # Parfois on simule une anomalie (10% de chance)
            if random.random() < 0.1:
                temperature = round(random.uniform(35.0, 42.0), 1)
                print("🔥 ANOMALIE SIMULÉE !")

            data = {
                "device_id": "capteur-salle-101",
                "temperature": temperature,
                "humidity": humidity,
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "location": "bureau-etage-2"
            }

            try:
                response = requests.post(
                    f"{API_URL}/ingest",
                    json=data,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    status = result["analysis"]["status"]
                    severity = result["analysis"]["severity"]
                    print(f"📡 Envoyé → Temp: {temperature}°C | Hum: {humidity}% | Status: {status} | Severity: {severity}")
                else:
                    print(f"❌ Erreur API: {response.status_code}")

            except Exception as e:
                print(f"❌ Erreur connexion: {e}")

            time.sleep(5)  # Toutes les 5 secondes

    except KeyboardInterrupt:
        print("
🛑 Arrêt du simulateur")

if __name__ == "__main__":
    simulate_sensor()
