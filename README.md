# 🤖 Agentic IoT System

Système IoT agentique complet avec analyse IA en temps réel.

## 🏗️ Architecture

```
Simulateur (Railway) → Backend API (Render) → Supabase (PostgreSQL)
                                            ↓
                                    Dashboard (Render)
```

| Composant | Technologie | Déployé sur |
|-----------|-------------|-------------|
| Simulateur | Python + Requests | Railway |
| Backend API | FastAPI + Groq LLM | Render |
| Base de données | PostgreSQL | Supabase |
| Dashboard | Streamlit | Render |
| CI/CD | GitHub Actions | GitHub |

## 🚀 Déploiement

### 1. Supabase (Base de données)
- Créer un projet sur [supabase.com](https://supabase.com)
- Créer la table `sensor_readings`:
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

### 2. Backend (Render)
- Créer un Web Service sur [render.com](https://render.com)
- Connecter le repo GitHub
- Root Directory: `backend`
- Build Command: `docker build -t iot-backend .`
- Start Command: `docker run -p 8000:8000 iot-backend`
- Variables d'environnement:
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
  - `GROQ_API_KEY`

### 3. Dashboard (Render)
- Créer un Web Service sur [render.com](https://render.com)
- Root Directory: `dashboard`
- Build Command: `docker build -t iot-dashboard .`
- Start Command: `docker run -p 8501:8501 iot-dashboard`
- Variable: `API_URL` (URL du backend)

### 4. Simulateur (Railway)
- Créer un projet sur [railway.app](https://railway.app)
- Deploy from GitHub repo
- Root Directory: `simulator`
- Variable: `API_URL` (URL du backend)

## 📊 Dashboard

Accéder au dashboard à l'URL fournie par Render.

## 🔧 Technologies

- **FastAPI** - Backend API
- **Streamlit** - Dashboard
- **Groq LLM** - Analyse IA
- **Supabase** - Base de données PostgreSQL
- **Render** - Hébergement cloud
- **Railway** - Hébergement simulateur
- **GitHub Actions** - CI/CD

## 📝 License

MIT
