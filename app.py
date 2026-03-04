import streamlit as st
import os
import time
import numpy as np
import librosa
import random
from gtts import gTTS
from scipy.io import wavfile
from streamlit_mic_recorder import mic_recorder

# --- 1. CORRECTIF SYSTÈME ---
if not os.path.exists('patch_done.txt'):
    try:
        os.system("sudo sed -i 's/domain=\"coder\" rights=\"none\" pattern=\"PDF\"/domain=\"coder\" rights=\"read|write\" pattern=\"PDF\"/' /etc/ImageMagick-6/policy.xml")
        with open('patch_done.txt', 'w') as f: f.write('done')
    except: pass

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="Ellia Flow Studio Pro", layout="wide", page_icon="🎙️")

with st.sidebar:
    st.header("🎨 Design")
    theme_color = st.color_picker("Couleur Studio", "#FF4B4B")
    welcome_vid = st.text_input("URL Vidéo Bienvenue", "")
    st.divider()
    st.header("👤 Empreinte Vocale")
    audio_record = mic_recorder(start_prompt="🎤 Enregistrer ma voix", stop_prompt="🛑 Arrêter", key='studio_recorder')

# CSS Correctif (Ligne 58 safe)
st.markdown(f"""
    <style>
    .stButton>button {{
        background-color: {theme_color} !important;
        color: white !important;
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE IA ---
def generer_paroles_ia(theme):
    templates = [
        f"Dans le flow de {theme}, je trouve ma voie, le rythme s'installe, j'ai plus de choix.",
        f"Écoute le son de {theme} qui résonne, dans tout le studio, plus rien ne m'étonne.",
        f"C'est Ellia Flow sur un air de {theme}, je lâche les mots, j'évite les problèmes."
    ]
    return random.choice(templates)

def simuler_clonage(text, audio_bytes):
    bar = st.progress(0)
    msg = st.empty()
    for p in [20, 50, 80, 100]:
        msg.text(f"⏳ IA en action... {p}%")
        time.sleep(0.7)
        bar.progress(p)
    
    tts = gTTS(text=text, lang='fr')
    tts.save("output.mp3")
    
    if audio_bytes:
        y, sr = librosa.load("output.mp3")
        y_mod = librosa.effects.pitch_shift(y, sr=sr, n_steps=0.6)
        wavfile.write("clone_final.wav", sr, (y_mod * 32767).astype(np.int16))
        return "clone_final.wav"
    return "output.mp3"

# --- 4. INTERFACE ---
st.title("🎙️ Ellia Flow Studio Pro")
if welcome_vid: st.video(welcome_vid)

tabs = st.tabs(["🎤 IA & Clonage", "🎼 Musique", "🎬 Vidéo", "💬 Avis"])

with tabs[0]:
    st.subheader("Générateur de Hit")
    
    # Aide à l'écriture
    theme_input = st.text_input("Thème de la chanson (ex: Amour, Succès, Rue)")
    if st.button("🪄 Générer des paroles par IA"):
        if theme_input:
            st.session_state.paroles_gen = generer_paroles_ia(theme_input)
        else: st.warning("Entre un thème !")

    # Zone de texte
    current_paroles = st.text_area("Paroles", value=st.session_state.get('paroles_gen', ""), height=100)
    
    if st.button("🚀 VALIDER ET FAIRE CHANTER MON CLONE"):
        if current_paroles:
            voice_data = audio_record['bytes'] if audio_record else None
            res = simuler_clonage(current_paroles, voice_data)
            
            st.audio(res)
            with open(res, "rb") as f:
                st.download_button("📥 Télécharger mon morceau", f, "mon_hit.wav")
            
            # Système de partage
            st.divider()
            st.write("📢 **Partager mon talent :**")
            share_url = "https://elliaflow.streamlit.app"
            st.code(f"Écoute mon nouveau hit créé sur Ellia Flow Studio ! {share_url}")

with tabs[1]:
    st.button("🎸 Créer une instrumentale")

with tabs[2]:
    st.button("🎞️ Générer le Clip Vidéo")

with tabs[3]:
    st.feedback("stars")
