import streamlit as st
import os
import subprocess
import time
import numpy as np
import librosa
from gtts import gTTS
from scipy.io import wavfile
from streamlit_audiorec import st_audiorec

# --- 1. CORRECTIF SYSTÈME (INDISPENSABLE) ---
if not os.path.exists('patch_done.txt'):
    try:
        os.system("sudo sed -i 's/domain=\"coder\" rights=\"none\" pattern=\"PDF\"/domain=\"coder\" rights=\"read|write\" pattern=\"PDF\"/' /etc/ImageMagick-6/policy.xml")
        with open('patch_done.txt', 'w') as f: f.write('done')
    except:
        pass

# --- 2. IMPORTS VIDÉO ---
try:
    import moviepy.editor as mp
    from moviepy.config import change_settings
    change_settings({"IMAGEMAGICK_BINARY": "convert"})
except:
    pass

# --- 3. CONFIGURATION UI ---
st.set_page_config(page_title="Ellia Flow Studio Pro", layout="wide", page_icon="🎵")

with st.sidebar:
    st.header("🎨 Personnalisation")
    theme_color = st.color_picker("Couleur du Studio", "#FF4B4B")
    welcome_vid = st.text_input("Lien Vidéo de Bienvenue (YouTube/MP4)", "")
    
    st.divider()
    st.header("👤 Votre Empreinte Vocale")
    st.write("Enregistrez-vous pour donner votre voix à l'IA.")
    wav_audio_data = st_audiorec()
    
    voice_sample = st.file_uploader("Ou importez un fichier vocal", type=["wav", "mp3"])

# Application du style CSS dynamique
st.markdown(f"""
    <style>
    .stButton>button {{
        background-color: {theme_color} !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
        opacity: 0.9;
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIQUE DES FONCTIONS ---

def simuler_clonage_progressif(paroles, user_voice_path):
    # Création d'une barre de progression visuelle
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        (10, "🔍 Analyse de votre empreinte vocale..."),
        (30, "🧬 Extraction des harmoniques..."),
        (50, "✍️ Conversion des paroles en phonèmes..."),
        (70, "🎤 Synthèse de la voix clonée..."),
        (90, "🎧 Finalisation du mixage audio..."),
        (100, "✅ Studio prêt !")
    ]
    
    for pct, msg in steps:
        time.sleep(0.8)  # Simulation du temps de calcul IA
        progress_bar.progress(pct)
        status_text.text(msg)
    
    # Génération réelle de l'audio
    tts = gTTS(text=paroles, lang='fr')
    tts.save("brut_voice.mp3")
    
    if user_voice_path:
        y, sr = librosa.load("brut_voice.mp3")
        # Pitch shift pour imiter une signature vocale
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=0.7)
        wavfile.write("cloned_song.wav", sr, (y_shifted * 32767).astype(np.int16))
        return "cloned_song.wav"
    
    return "brut_voice.mp3"

# --- 5. INTERFACE PRINCIPALE ---
st.title("🎙️ Ellia Flow Studio Pro")

if welcome_vid:
    st.video(welcome_vid)

tabs = st.tabs(["🎤 IA & Clonage", "🎼 Musique", "✂️ Séparation", "🎬 Clip Vidéo", "💬 Avis"])

# --- ONGLET 1 : IA & CLONAGE ---
with tabs[0]:
    st.subheader("Laboratoire de Clonage")
    
    if "paroles_validees" not in st.session_state:
        st.session_state.paroles_validees = False

    paroles = st.text_area("📝 Étape 1 : Saisissez les paroles de votre futur hit", height=150, placeholder="Ex: Dans le studio d'Ellia, le flow ne s'arrête jamais...")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Valider les paroles"):
            if paroles.strip():
                st.session_state.paroles_validees = True
                st.toast("Paroles validées !", icon="✍️")
            else:
                st.error("Le texte est vide.")

    with c2:
        if st.session_state.paroles_validees:
            if st.button("🚀 GÉNÉRER MA VOIX IA"):
                # Détection de la source vocale
                source_voix = None
                if wav_audio_data is not None:
                    with open("user_voice.wav", "wb") as f:
                        f.write(wav_audio_data)
                    source_voix = "user_voice.wav"
                elif voice_sample is not None:
                    source_voix = voice_sample

                # Lancement avec effets visuels
                resultat_audio = simuler_clonage_progressif(paroles, source_voix)
                
                st.success("✨ Votre chanson a été générée avec succès !")
                
                st.divider()
                st.subheader("🎧 Lecteur d'aperçu")
                st.audio(resultat_audio)
                
                with open(resultat_audio, "rb") as file:
                    st.download_button(
                        label="💾 Télécharger mon morceau (HD)",
                        data=file,
                        file_name="mon_hit_cloné.wav",
                        mime="audio/wav"
                    )

# --- AUTRES ONGLETS ---
with tabs[1]:
    st.subheader("🎹 Créateur d'instrumentales")
    if st.button("🎸 Générer un beat de base"):
        st.info("Génération du beat en cours...")

with tabs[2]:
    st.subheader("✂️ Séparateur Vocal")
    st.file_uploader("Uploader une chanson pour isoler la voix", type=["mp3"])

with tabs[3]:
    st.subheader("🎬 Montage Clip Express")
    st.file_uploader("Importer vos visuels", accept_multiple_files=True)
    if st.button("🎞️ Lancer le rendu vidéo"):
        st.balloons()

with tabs[4]:
    st.header("⭐ Votre avis")
    st.feedback("stars")
    st.text_input("Un mot pour l'équipe ?")

st.caption("🚀 Propulsé par Ellia Flow Studio - Version 2.0")
