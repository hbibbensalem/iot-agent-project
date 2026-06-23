import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# URL du backend
API_URL = os.getenv("API_URL", "http://localhost:8000")


# ========== FONCTIONS (définitions uniquement) ==========

def get_data():
    """Récupère les données depuis le backend API"""
    try:
        response = requests.get(f"{API_URL}/data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            if len(df) > 0:
                df['datetime'] = pd.to_datetime(df['created_at'])
                df = df.sort_values('datetime')
            return df
        else:
            return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def main():
    """Point d'entrée principal de l'application Streamlit"""
    st.set_page_config(page_title="🤖 Agent IoT Dashboard", layout="wide")

    st.title("🤖 Agentic IoT - Tableau de Bord")
    st.markdown("---")

    # Mise à jour auto
    st.sidebar.header("⚙️ Paramètres")
    auto_refresh = st.sidebar.checkbox("Rafraîchissement auto", value=True)
    refresh_interval = st.sidebar.slider("Intervalle (sec)", 5, 60, 10)

    if st.sidebar.button("🔄 Rafraîchir maintenant"):
        st.rerun()

    # Récupérer données
    df = get_data()

    if len(df) == 0:
        st.warning("Aucune donnée trouvée. Lance le simulateur !")
        st.info(f"API URL: {API_URL}")
        st.stop()

    # Métriques
    st.header("📊 Métriques en temps réel")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌡️ Température moyenne", f"{df['temperature'].mean():.1f}°C")
    with col2:
        st.metric("💧 Humidité moyenne", f"{df['humidity'].mean():.1f}%")
    with col3:
        alertes = len(df[df['severity'].isin(['high', 'critical'])])
        st.metric("🚨 Alertes critiques", alertes)
    with col4:
        st.metric("📡 Messages reçus", len(df))

    st.markdown("---")

    # Graphiques
    st.header("📈 Évolution des capteurs")
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🌡️ Température")
        st.line_chart(df.set_index('datetime')[['temperature']])

    with col_right:
        st.subheader("💧 Humidité")
        st.line_chart(df.set_index('datetime')[['humidity']])

    # Distribution des statuts
    st.header("📋 Distribution des décisions")
    status_counts = df['status'].value_counts()
    st.bar_chart(status_counts)

    # Tableau des alertes
    st.header("🚨 Dernières alertes")
    alertes_df = df[df['severity'].isin(['high', 'critical'])].tail(10)
    if len(alertes_df) > 0:
        for _, row in alertes_df.iterrows():
            with st.expander(f"🔴 {row['status'].upper()} - {row['datetime'].strftime('%H:%M:%S')}"):
                st.write(f"**Température:** {row['temperature']}°C")
                st.write(f"**Humidité:** {row['humidity']}%")
                st.write(f"**Action:** {row['action']}")
                st.write(f"**Raison:** {row['reason']}")
    else:
        st.success("✅ Aucune alerte critique !")

    # Dernières données
    st.header("📡 Dernières données reçues")
    st.dataframe(df.tail(10)[['datetime', 'temperature', 'humidity', 'status', 'severity']].sort_values('datetime', ascending=False))

    # Auto refresh
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()


# ========== PROTECTION CRITIQUE ==========
# Ce bloc ne s'exécute QUE quand on fait "streamlit run app.py"
# Il ne s'exécute PAS quand on fait "import app"
if __name__ == "__main__":
    main()