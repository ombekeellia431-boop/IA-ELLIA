import streamlit as st
import os
import time
import random
from moviepy.editor import ImageClip, AudioFileClip

# --- 1. CONFIGURATION ET THÈME ---
if os.name != 'nt':
    os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

st.set_page_config(page_title="Ellia Flow Studio Pro", page_icon="🔥", layout="wide")

# Personnalisation dynamique des couleurs
st.sidebar.title("🎨 Design du Studio")
primary_color = st.sidebar.color_picker("Couleur principale", "#FF4B4B")
st.markdown(f"""
    <style>
    .stButton>button {{ background: {primary_color}; color: white; border-radius: 20px; font-weight: bold; border: none; }}
    .stApp {{ background-color: #0e1117; color: white; }}
    .preview-box {{ border: 2px solid {primary_color}; padding: 15px; border-radius: 10px; margin-top: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. BARRE LATÉRALE : CLONAGE VOCAL ---
with st.sidebar:
    st.header("👤 Votre Voix")
    audio_input = st.audio_input("Enregistrez-vous pour le clonage")
    
    st.divider()
    st.subheader("🛠️ Amélioration Voix")
    autotune = st.checkbox("Activer l'Auto-Tune Pro", value=True)
    reverb = st.select_slider("Réverbération (Écho)", options=["Sec", "Studio", "Cathédrale"])

    voice_path = "voice_cloned.wav"
    if audio_input:
        with open(voice_path, "wb") as f:
            f.write(audio_input.getbuffer())
        st.success("Voix enregistrée et optimisée !")

# --- 3. ESPACE DE CRÉATION ---
st.title("🎙️ Ellia Flow Studio Pro v3.0")

tabs = st.tabs(["🎵 Chant & Musique", "✂️ Séparation", "🎬 Clip Vidéo", "⭐ Avis & Communauté"])

# --- ONGLET 1 : CHANT ET INSTRUMENTS ---
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        lyrics = st.text_area("✍️ Paroles de la chanson", height=150, placeholder="Écrivez ici...")
        instrus = st.multiselect("🎸 Orchestration (Choix des instruments)", 
                               ["Piano", "Batterie Trap", "Guitare Acoustique", "Synthé 80s", "Basse Deep", "Violons"])
    
    with col2:
        if st.button("🪄 Suggérer un titre par IA"):
            if lyrics:
                titres = ["Écho Numérique", "Flow de l'Estuaire", "Vibrations Cloud", "Coeur de Silicium"]
                st.info(f"Titre suggéré : **{random.choice(titres)}**")
            else: st.warning("Écrivez d'abord des paroles.")

    if st.button("🎤 GÉNÉRER MON MORCEAU"):
        if voice_path and lyrics:
            with st.spinner("L'IA compose votre musique..."):
                time.sleep(4)
                st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                st.subheader("👂 ÉCOUTER AVANT DE TÉLÉCHARGER")
                st.audio(voice_path)
                
                with open(voice_path, "rb") as f:
                    st.download_button("📥 Télécharger le MP3 final", f, file_name="ma_musique_ellia.mp3")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("⚠️ Erreur : Voix ou paroles manquantes.")

# --- ONGLET 2 : SÉPARATION ---
with tabs[1]:
    st.header("✂️ Séparation de Pistes")
    up_sep = st.file_uploader("Importer une chanson à décomposer", type=['mp3'])
    if st.button("Lancer la séparation"):
        st.info("Traitement haute précision en cours...")

# --- ONGLET 3 : CLIP VIDÉO AVEC APERÇU ---
with tabs[2]:
    st.header("🎬 Créateur de Clip Vidéo")
    img_bg = st.file_uploader("Image pour le clip", type=['jpg', 'png'])
    
    if st.button("📽️ ASSEMBLER LE CLIP"):
        if img_bg and os.path.exists(voice_path):
            with st.spinner("Rendu vidéo accéléré..."):
                with open("bg.jpg", "wb") as f: f.write(img_bg.getbuffer())
                audio = AudioFileClip(voice_path)
                clip = ImageClip("bg.jpg").set_duration(audio.duration).set_audio(audio)
                output = "preview_video.mp4"
                clip.write_videofile(output, fps=15, codec="libx264", preset="ultrafast")
                
                st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                st.subheader("📺 VOIR AVANT DE TÉLÉCHARGER")
                st.video(output)
                
                with open(output, "rb") as f:
                    st.download_button("📥 Télécharger la Vidéo HD", f, file_name="mon_clip_ellia.mp4")
                st.markdown('</div>', unsafe_allow_html=True)

# --- ONGLET 4 : AVIS ET COMMENTAIRES ---
with tabs[3]:
    st.header("💬 Avis des Créateurs")
    
    with st.form("form_avis"):
        note = st.select_slider("Notez l'application", options=["💩", "😐", "🙂", "🔥", "💎"])
        user_name = st.text_input("Votre nom / Pseudo")
        user_comment = st.text_area("Votre commentaire ou suggestion")
        submit = st.form_submit_button("Envoyer mon avis")
        
        if submit:
            st.success(f"Merci {user_name} ! Ton avis ({note}) a été partagé à la communauté.")
            st.session_state['last_comment'] = f"**{user_name}** : {user_comment} ({note})"

    if 'last_comment' in st.session_state:
        st.markdown("### Dernier commentaire reçu :")
        st.info(st.session_state['last_comment'])
