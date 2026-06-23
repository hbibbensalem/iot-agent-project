
readme_content = '''# 🤖 Agentic IoT System

Système IoT agentique complet avec analyse IA en temps réel. Capteurs simulés → Backend API (FastAPI + Groq LLM) → Supabase (PostgreSQL) → Dashboard Streamlit.

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-FF6B35?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" />
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" />
  <img src="https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" />
</p>

---

## 🏗️ Architecture

```
┌─────────────┐      HTTP POST      ┌──────────────┐      ┌─────────────┐
│ Simulateur  │ ──────────────────► │ Backend API  │ ────► │  Supabase   │
│  (Railway)  │   toutes les 5s     │   (Render)   │       │(PostgreSQL) │
│   Python    │                     │ FastAPI+Groq │       │             │
└─────────────┘                     └──────────────┘       └──────┬──────┘
                                                                  │
                                                                  │ GET /data
                                                                  ▼
                                                           ┌─────────────┐
                                                           │  Dashboard  │
                                                           │   (Render)  │
                                                           │  Streamlit  │
                                                           └─────────────┘
```

| Composant | Technologie | Plateforme | Statut |
|-----------|-------------|------------|--------|
| 🔄 Simulateur | Python + Requests | Railway | 24/7 |
| ⚡ Backend API | FastAPI + Groq LLM | Render | [Live](https://iot-agent-project.onrender.com/health) |
| 🗄️ Base de données | PostgreSQL | Supabase | Active |
| 📊 Dashboard | Streamlit | Render | [Live](https://iot-agent-dashboard.onrender.com) |
| 🚀 CI/CD | GitHub Actions | GitHub | ✅ Automatisé |

---

## ✨ Fonctionnalités

- 📡 **Simulation temps réel** - Capteurs IoT simulés (température, humidité)
- 🧠 **Analyse IA** - Classification automatique par Groq LLM (normal/warning/critical)
- 🚨 **Alertes intelligentes** - Actions recommandées selon la gravité
- 📊 **Dashboard temps réel** - Visualisation avec Streamlit
- 🔄 **Déploiement auto** - CI/CD GitHub Actions → Render + Railway

---

## 📸 Dashboard

### Métriques en temps réel
![Dashboard - Métriques](https://raw.githubusercontent.com/hbibbensalem/iot-agent-project/main/screenshots/dashboard_metrics.png)

### Distribution des décisions IA
![Dashboard - Distribution](https://raw.githubusercontent.com/hbibbensalem/iot-agent-project/main/screenshots/dashboard_distribution.png)

### Alertes critiques et données
![Dashboard - Alertes](https://raw.githubusercontent.com/hbibbensalem/iot-agent-project/main/screenshots/dashboard_alerts.png)

---

## 🚀 Déploiement Rapide

### 1. Supabase (Base de données)

```sql
create table sensor_readings (
  id uuid default gen_random_uuid() primary key,
  device_id text,
  temperature float,
  humidity float,
  timestamp text,
  location text,
  status text,
  severity text,
  action text,
  reason text,
  created_at timestamp with time zone default now()
);
```

### 2. Variables d\'environnement

| Service | Variable | Description |
|---------|----------|-------------|
| Backend | `SUPABASE_URL` | URL projet Supabase |
| Backend | `SUPABASE_KEY` | Clé service Supabase |
| Backend | `GROQ_API_KEY` | Clé API Groq |
| Dashboard | `API_URL` | URL backend Render |
| Simulateur | `API_URL` | URL backend Render |

### 3. Plateformes Cloud

| Service | Action | Root Directory |
|---------|--------|----------------|
| **Backend** | Web Service sur Render | `backend/` |
| **Dashboard** | Web Service sur Render | `dashboard/` |
| **Simulateur** | Deploy from GitHub sur Railway | `simulator/` |

---

## 📁 Structure du projet

```
iot-agent-project/
├── .github/workflows/
│   └── ci.yml              # CI/CD Pipeline
├── backend/
│   ├── main.py             # FastAPI API
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── app.py              # Streamlit Dashboard
│   ├── requirements.txt
│   └── Dockerfile
├── simulator/
│   ├── simulator.py        # Simulateur capteurs
│   ├── requirements.txt
│   └── Dockerfile
├── screenshots/
│   ├── dashboard_metrics.png
│   ├── dashboard_distribution.png
│   └── dashboard_alerts.png
└── README.md
```

---

## 🔗 URLs du projet

| Service | URL |
|---------|-----|
| 🏥 Health Check | https://iot-agent-project.onrender.com/health |
| 📊 Dashboard | https://iot-agent-dashboard.onrender.com |
| 📡 API Data | https://iot-agent-project.onrender.com/data |
| 🐙 GitHub | https://github.com/hbibbensalem/iot-agent-project |

---

## 🧪 CI/CD Pipeline

```
Push sur main → Test → Build Docker → Deploy Render
```

- ✅ Tests d\'import Python
- ✅ Linting flake8
- ✅ Build images Docker
- 🚀 Auto-deploy Backend + Dashboard sur Render

---

## 🛠️ Technologies

| Domaine | Stack |
|---------|-------|
| **Backend** | Python, FastAPI, Docker |
| **Frontend** | Streamlit |
| **IA/LLM** | Groq API, Prompt Engineering |
| **Base de données** | PostgreSQL, Supabase |
| **Cloud** | Render, Railway |
| **DevOps** | GitHub Actions, Docker, CI/CD |
| **IoT** | Simulation capteurs, HTTP/REST |

---

## 📝 Auteur

**Hbib Ben Salem** - [LinkedIn](https://linkedin.com/in/hbibbensalem) | [GitHub](https://github.com/hbibbensalem)

---

## 📜 License

MIT © 2026
'''

with open('/mnt/agents/output/README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("README.md créé avec succès!")
