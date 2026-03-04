import streamlit as st
import os
from streamlit_mic_recorder import mic_recorder  # Nouvelle bibliothèque stable

# --- 1. CORRECTIF SYSTÈME ---
if not os.path.exists('patch_done.txt'):
    os.system("sudo sed -i 's/domain=\"coder\" rights=\"none\" pattern=\"PDF\"/domain=\"coder\" rights=\"read|write\" pattern=\"PDF\"/' /etc/ImageMagick-6/policy.xml")
    with open('patch_done.txt', 'w') as f: f.write('done')

# --- 2. CONFIGURATION UI ---
st.set_page_config(page_title="Ellia Flow Studio Pro", layout="wide")

# Correction de ton erreur Ligne 58 : On définit theme_color AVANT le CSS
with st.sidebar:
    st.header("🎨 Personnalisation")
    theme_color = st.color_picker("Couleur du Studio", "#FF4B4B")
    
    st.divider()
    st.header("👤 Enregistre ta voix")
    # Nouvel enregistreur qui fonctionne sur mobile et PC
    audio = mic_recorder(start_prompt="🎤 Cliquer pour enregistrer", stop_prompt="🛑 Arrêter")

# Application du CSS sécurisé
st.markdown(f"""
    <style>
    .stButton>button {{
        background-color: {theme_color} !important;
        color: white !important;
        border-radius: 12px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFACE PRINCIPALE ---
st.title("🎙️ Ellia Flow Studio Pro")

tabs = st.tabs(["🎤 IA & Clonage", "🎼 Musique", "🎬 Clip"])

with tabs[0]:
    paroles = st.text_area("✍️ Paroles")
    if st.button("🚀 GÉNÉRER MON CLONE"):
        if audio:
            st.success("Voix capturée avec succès !")
            # Ton code de clonage ici...
        else:
            st.warning("Enregistre d'abord ta voix dans la barre de gauche !")
