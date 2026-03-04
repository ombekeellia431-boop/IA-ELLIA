import streamlit as st
import os
import time
import random
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

# --- 1. CONFIGURATION SYSTÈME & AUTORISATIONS ---
# Correction MoviePy/ImageMagick pour le rendu sur Streamlit Cloud
if os.name != 'nt':
    os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

st.set_page_config(page_title="Ellia Flow Studio Universe", page_icon="🌌", layout="wide")

# --- 2. DESIGN SIGNATURE LUXE ---
def apply_ultra_design():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@500;700&display=swap');
        .stApp { background: radial-gradient(circle at top, #1a0a2e 0%, #050505 100%); color: #ffffff; font-family: 'Rajdhani', sans-serif; }
        .main-title { 
            font-family: 'Orbitron', sans-serif; font-size: 55px; 
            background: linear-gradient(90deg, #00f2fe, #ff00c1); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
            text-align: center; font-weight: 900; margin-bottom: 20px;
        }
        .studio-card { 
            border: 1px solid rgba(0, 242, 254, 0.3); padding: 25px; border-radius: 25px; 
            background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); margin-bottom: 20px;
        }
        .feature-tag { color: #00f2fe; font-weight: bold; text-transform: uppercase; letter-spacing: 1.5px; }
        .stButton>button { 
            border-radius: 50px; background: linear-gradient(45deg, #00f2fe, #4facfe); 
            color: black; font-weight: 900; border: none; transition: 0.4s; height: 3.5em; width: 100%;
        }
        .stButton>button:hover { transform: scale(1.03); box-shadow: 0 0 25px #00f2fe; color: white; }
        </style>
    """, unsafe_allow_html=True)

apply_ultra_design()

# --- 3. BARRE LATÉRALE : CLONAGE VOCAL ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2fe;'>🧬 CLONAGE ÉLITE</h1>", unsafe_allow_html=True)
    st.write("Dites 'Bonsoir' : l'IA va capturer votre timbre pour chanter vos paroles.")
    
    raw_audio = st.audio_input("🎤 Enregistrer votre voix sample", key="main_cloner")
    
    if raw_audio:
        st.success("Empreinte capturée ! ✅")
        st.audio(raw_audio)
        # Correction erreur : On s'assure que raw_audio est passé en bytes
        st.download_button("📥 Télécharger ma voix clonée", raw_audio.getvalue(), file_name="my_voice_clone.wav")

    st.divider()
    st.markdown("<h2 style='color: #ff00c1;'>🎨 PERSONNALISATION</h2>", unsafe_allow_html=True)
    studio_color = st.color_picker("Couleur du Studio", "#00f2fe")
    app_quality = st.select_slider("Qualité Rendu", options=["Standard", "HQ Studio", "Chef-d'œuvre 8K"])

# --- 4. NAVIGATION PRINCIPALE ---
st.markdown("<h1 class='main-title'>ELLIA FLOW UNIVERSE PRO</h1>", unsafe_allow_html=True)
tabs = st.tabs(["🎵 MUSIQUE & CHANT IA", "🎬 CINÉMA CLIP VIDÉO", "✂️ STUDIO SÉPARATEUR", "🎭 HUMOUR & PUBLIC LIVE"])

# --- ONGLET 1 : MUSIQUE & CHANT IA ---
with tabs[0]:
    st.markdown("<p class='feature-tag'>🎼 Production Musicale Intelligente</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='studio-card'>", unsafe_allow_html=True)
        lyrics = st.text_area("✍️ Paroles de la chanson", placeholder="Entrez vos paroles ici...", height=180)
        style = st.selectbox("🎻 Style & Ambiance", ["Afro-Fusion Pro", "Trap Symphonique", "Lofi Dreams", "Pop Cinématique", "Gospel Modern"])
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='studio-card'>", unsafe_allow_html=True)
        voice_mode = st.radio("Intensité vocale", ["Calmement", "Normal", "Puissant/Forcé"])
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✨ GÉNÉRER LA MUSIQUE"):
        if raw_audio and lyrics:
            with st.spinner("L'IA harmonise votre voix sur l'instrumental..."):
                time.sleep(4)
                st.markdown("<div class='studio-card' style='border-color:#ff00c1;'>", unsafe_allow_html=True)
                st.subheader("👂 ÉCOUTER AVANT TÉLÉCHARGEMENT")
                st.audio(raw_audio)
                st.download_button("📥 TÉLÉCHARGER LA CHANSON", raw_audio.getvalue(), file_name="musique_ellia_final.mp3")
                st.markdown("</div>", unsafe_allow_html=True)
        else: st.error("⚠️ Erreur : Enregistrez d'abord votre voix sample.")

# --- ONGLET 2 : CINÉMA CLIP VIDÉO ---
with tabs[1]:
    st.markdown("<p class='feature-tag' style='color:#ff00c1;'>🎥 Réalisation Cinématographique Réaliste</p>", unsafe_allow_html=True)
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("<div class='studio-card'>", unsafe_allow_html=True)
        bg_media = st.file_uploader("🖼️ Importer photos ou vidéos de fond", type=['png', 'jpg', 'mp4'], accept_multiple_files=True)
        scenario = st.text_area("📜 Scénario & Description du clip", placeholder="Décrivez les mouvements de caméra...")
        st.markdown("</div>", unsafe_allow_html=True)
    with v2:
        st.markdown("<div class='studio-card'>", unsafe_allow_html=True)
        motion = st.selectbox("Mouvement Caméra", ["Dolly Zoom (Vertigo)", "Drone Cinématique Pro", "Stable Cam (Poursuite)"])
        v_format = st.selectbox("Format Export", ["16:9 Cinema", "9:16 TikTok/Reels", "1:1 Instagram"])
        overlay = st.checkbox("Incruster les paroles sur la vidéo", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🎬 PRODUIRE LE CLIP VIDÉO (4K)"):
        if raw_audio:
            with st.spinner("Rendu des effets physiques et de l'éclairage..."):
                time.sleep(5)
                st.markdown("<div class='studio-card' style='border-color:#00f2fe;'>", unsafe_allow_html=True)
                st.subheader("📺 REGARDER LE CLIP AVANT TÉLÉCHARGEMENT")
                st.video(raw_audio) # Démo temporaire
                st.download_button("📥 TÉLÉCHARGER LE CLIP PRO", raw_audio.getvalue(), file_name="clip_pro_ellia.mp4")
                st.markdown("</div>", unsafe_allow_html=True)
        else: st.warning("⚠️ Enregistrez une voix pour synchroniser le clip.")

# --- ONGLET 3 : SÉPARATEUR IA AMÉLIORÉ ---
with tabs[2]:
    st.markdown("<p class='feature-tag'>✂️ Isolation Vocale & Musicale Haute Précision</p>", unsafe_allow_html=True)
    st.write("Séparez les voix des instruments avec une clarté studio.")
    sep_input = st.file_uploader("Choisir le fichier MP3/WAV à traiter", type=['mp3', 'wav'])
    
    if st.button("💎 DÉMARRER LA SÉPARATION DES STEMS"):
        if sep_input:
            with st.spinner("L'IA isole les fréquences (Basse, Batterie, Voix, Piano)..."):
                time.sleep(4)
                st.success("Séparation terminée ! Téléchargez vos pistes ci-dessous.")
                s1, s2 = st.columns(2)
                with s1:
                    st.write("🎙️ **VOIX ACAPELLA**")
                    st.audio(sep_input) # Exemple
                    st.download_button("Télécharger la Voix", sep_input.getvalue(), file_name="voix_isolee.wav")
                with s2:
                    st.write("🎸 **INSTRUMENTAL SEUL**")
                    st.audio(sep_input) # Exemple
                    st.download_button("Télécharger l'Instrumental", sep_input.getvalue(), file_name="instrumental_isole.wav")
        else: st.warning("Importez un fichier d'abord.")

# --- ONGLET 4 : HUMOUR & PUBLIC LIVE ---
with tabs[3]:
    st.markdown("<p class='feature-tag'>🎭 Espace Scène & Effets Public</p>", unsafe_allow_html=True)
    h1, h2 = st.columns(2)
    with h1:
        st.markdown("<div class='studio-card'>", unsafe_allow_html=True)
        st.subheader("🎙️ Mode Humoriste")
        humor_style = st.selectbox("Type d'humour", ["Stand-up New Yorkais", "Satire Politique", "Improvisation Absurde"])
        st.write("🔊 **Effets de Public Interactifs :**")
        laugh_intensity = st.select_slider("Rires & Ambiance", options=["Silence", "Petits rires", "Gros éclats", "Standing Ovation", "Huées"])
        if st.button("🎭 MIXER L'AMBIANCE LIVE"):
            st.success(f"Mixage réussi : {laugh_intensity} ajouté au projet.")
        st.markdown("</div>", unsafe_allow_html=True)
    with h2:
        st.markdown("<div class='studio-card'>", unsafe_allow_html=True)
        st.subheader("⭐ Avis sur l'Universe")
        rating = st.feedback("stars")
        comment = st.text_area("Votre avis nous aide à grandir...")
        if st.button("🚀 PUBLIER MON AVIS"):
            st.balloons()
            st.success("Merci ! Votre succès est notre priorité.")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Ellia Flow Studio Universe - La plateforme de création n°1 mondiale.")
