import streamlit as st
import os
import time
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

# --- 1. CONFIGURATION SYSTÈME ---
# Correction pour ImageMagick sur Streamlit Cloud
if os.name != 'nt':
    os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

st.set_page_config(page_title="Ellia Flow Studio Ultra", page_icon="💎", layout="wide")

# --- 2. DESIGN & PERSONNALISATION ---
st.sidebar.title("🎨 Design du Studio")
theme_title = st.sidebar.text_input("Titre personnalisé", "Ellia Flow Studio Ultra")
accent_color = st.sidebar.color_picker("Couleur principale", "#6C63FF")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    .stButton>button {{ 
        background: {accent_color}; color: white; border-radius: 25px; 
        font-weight: bold; border: none; width: 100%; height: 3em;
    }}
    .preview-box {{ 
        border: 2px solid {accent_color}; padding: 20px; border-radius: 15px; 
        background: #1a1c23; margin: 15px 0; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. VOTRE VOIX (CLONAGE) ---
with st.sidebar:
    st.header("👤 Votre Voix")
    # Utilisation d'une clé unique pour éviter les erreurs de rafraîchissement
    audio_record = st.audio_input("Enregistrez-vous pour le clonage", key="voice_recorder")
    
    st.divider()
    st.subheader("🎚️ Style de Chant")
    singing_intensity = st.select_slider("Intensité", options=["Calmement", "Normal", "Forcé"])
    
    voice_path = "cloned_voice.wav"
    if audio_record:
        with open(voice_path, "wb") as f:
            f.write(audio_record.getbuffer())
        st.success("Voix prête ✅")

# --- 4. NAVIGATION ---
st.title(f"🚀 {theme_title}")
tabs = st.tabs(["🎤 Musique & Chant", "✂️ Séparation", "🎬 Clip Vidéo", "⭐ Avis & Notes"])

# --- TAB 1 : CHANT IA & INSTRUMENTAL ---
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        lyrics = st.text_area("✍️ Paroles pour l'IA", height=150)
    with col2:
        instru = st.file_uploader("📂 Mettre l'instrumental de votre choix", type=['mp3', 'wav'])
    
    if st.button("🎵 GÉNÉRER LA CHANSON"):
        if audio_record and lyrics:
            with st.spinner(f"L'IA chante {singing_intensity}..."):
                time.sleep(3) # Simulation IA
                st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                st.subheader("👂 ÉCOUTER AVANT DE TÉLÉCHARGER")
                st.audio(voice_path)
                with open(voice_path, "rb") as f:
                    st.download_button("📥 TÉLÉCHARGER LA CHANSON", f, file_name="chanson_ellia.mp3")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Enregistrez votre voix et écrivez les paroles.")

# --- TAB 2 : SÉPARATION ---
with tabs[1]:
    st.header("✂️ Séparateur Voix & Sons")
    sep_file = st.file_uploader("Fichier à séparer", type=['mp3'])
    if st.button("Lancer la séparation"):
        st.info("Traitement haute précision en cours...")

# --- TAB 3 : CLIP VIDÉO (MODÈLES & PAROLES) ---
with tabs[2]:
    st.header("🎬 Créateur de Clip Vidéo")
    c1, c2 = st.columns(2)
    with c1:
        img_bg = st.file_uploader("📸 Votre image ou vidéo", type=['jpg', 'png', 'mp4'])
        model_vid = st.selectbox("Ou choisir un modèle de vidéo", ["Aucun", "Néon Urbain", "Galaxie", "Studio Pro"])
    with c2:
        font_size = st.slider("Taille des paroles", 20, 80, 40)
        show_lyrics = st.checkbox("Afficher les paroles sur le clip", value=True)

    if st.button("🚀 ASSEMBLER LE CLIP"):
        if img_bg and audio_record:
            with st.spinner("Rendu du clip avec paroles..."):
                # Simulation de création vidéo
                time.sleep(4)
                output_vid = "final_clip.mp4"
                # (Ici la logique MoviePy comme dans mes précédents messages)
                
                st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                st.subheader("📺 VOIR AVANT DE TÉLÉCHARGER")
                st.video(voice_path) # Démo (remplacer par output_vid)
                st.download_button("📥 TÉLÉCHARGER LE CLIP", voice_path, file_name="clip_ellia.mp4")
                st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 4 : AVIS & NOTES ---
with tabs[3]:
    st.header("⭐ Avis sur l'Application")
    with st.form("feedback"):
        note = st.feedback("stars")
        user_comment = st.text_area("Votre commentaire")
        if st.form_submit_button("Publier l'avis"):
            st.success("Merci ! Votre avis est précieux pour notre succès.")
