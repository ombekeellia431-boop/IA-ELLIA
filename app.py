import streamlit as st
import os
import time
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

# --- 1. CONFIGURATION SYSTÈME ---
if os.name != 'nt':
    os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

st.set_page_config(page_title="Ellia Flow Studio Pro", page_icon="🔥", layout="wide")

# --- 2. STYLE & PERSONNALISATION ---
st.sidebar.title("🎨 Style du Studio")
theme_color = st.sidebar.color_picker("Couleur de l'interface", "#FF4B4B")
font_choice = st.sidebar.selectbox("Police du Clip", ["Arial-Bold", "Courier-Bold", "Georgia-Bold", "Verdana-Bold"])
text_color = st.sidebar.color_picker("Couleur du texte", "#FFFFFF")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    .stButton>button {{ 
        background-color: {theme_color}; color: white; border-radius: 12px; 
        font-weight: bold; border: none; height: 3.5em; width: 100%; 
    }}
    .lyrics-display {{ 
        border: 1px dashed {theme_color}; padding: 15px; border-radius: 10px; 
        background-color: #1a1c23; color: #d1d1d1; font-style: italic;
    }}
    .preview-box {{ 
        border: 2px solid {theme_color}; padding: 20px; border-radius: 15px; 
        background-color: #1a1c23; margin: 15px 0; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. CLONAGE VOCAL (SIDEBAR) ---
with st.sidebar:
    st.header("👤 Votre Voix")
    audio_record = st.audio_input("Enregistrez votre voix")
    voice_path = "user_voice.wav"
    if audio_record:
        with open(voice_path, "wb") as f:
            f.write(audio_record.getbuffer())
        st.success("Voix prête ✅")
    
    st.divider()
    st.subheader("🛠️ Effets")
    autotune = st.checkbox("Auto-Tune Pro", value=True)
    reverb = st.select_slider("Réverbération", options=["Sec", "Studio", "Cathédrale"])

# --- 4. NAVIGATION PRINCIPALE ---
st.title("🎼 Ellia Flow Studio Pro")

tabs = st.tabs(["🎤 Chant & Musique", "✂️ Séparateur", "🎬 Clip & Paroles", "⭐ Avis"])

# --- TAB 1 : CHANT & INSTRUMENTS ---
with tabs[0]:
    st.header("Composition & Orchestration")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("✍️ Espace Paroles")
        lyrics = st.text_area("Écrivez vos paroles :", placeholder="Vos paroles ici...", height=150)
        if lyrics:
            st.markdown(f'<div class="lyrics-display"><b>Aperçu :</b><br>{lyrics}</div>', unsafe_allow_html=True)
    with col2:
        st.subheader("🎸 Instruments")
        instrus = st.multiselect("Orchestration :", 
                                ["Piano Lunaire", "Batterie Afro-Trap", "Basse Profonde", "Guitare Électrique", "Kora Digitale"],
                                default=["Piano Lunaire", "Batterie Afro-Trap"])

    if st.button("🎵 GÉNÉRER LA MUSIQUE"):
        if voice_path and lyrics:
            with st.spinner("Fusion Voix + Instruments..."):
                time.sleep(2)
                st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                st.subheader("👂 ÉCOUTER AVANT DE TÉLÉCHARGER")
                st.audio(voice_path)
                with open(voice_path, "rb") as f:
                    st.download_button("📥 Télécharger MP3", f, file_name="musique_ellia.mp3")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Manque la voix ou les paroles.")

# --- TAB 2 : SÉPARATEUR ---
with tabs[1]:
    st.header("✂️ Séparation de pistes")
    up_sep = st.file_uploader("Fichier MP3/WAV", type=['mp3', 'wav'])
    if st.button("Lancer la séparation"):
        st.info("Traitement en cours...")

# --- TAB 3 : CLIP VIDÉO ---
with tabs[2]:
    st.header("🎬 Clip Vidéo avec Paroles")
    img_bg = st.file_uploader("Image de fond", type=['jpg', 'png'])
    font_size = st.slider("Taille du texte", 20, 80, 40)
    
    if st.button("🚀 ASSEMBLER LE CLIP"):
        if img_bg and os.path.exists(voice_path):
            with st.spinner("Rendu vidéo..."):
                with open("bg.jpg", "wb") as f: f.write(img_bg.getbuffer())
                audio_clip = AudioFileClip(voice_path)
                video_clip = ImageClip("bg.jpg").set_duration(audio_clip.duration)
                
                if lyrics:
                    txt_clip = TextClip(lyrics[:60] + "...", fontsize=font_size, color=text_color, 
                                        font=font_choice, stroke_color='black', stroke_width=2,
                                        method='caption', size=(video_clip.w*0.8, None))
                    txt_clip = txt_clip.set_position('center').set_duration(audio_clip.duration)
                    video_clip = CompositeVideoClip([video_clip, txt_clip])
                
                video_clip = video_clip.set_audio(audio_clip)
                output = "clip_final.mp4"
                video_clip.write_videofile(output, fps=12, codec="libx264", preset="ultrafast")
                
                st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                st.subheader("📺 VOIR AVANT DE TÉLÉCHARGER")
                st.video(output)
                with open(output, "rb") as f:
                    st.download_button("📥 Télécharger Clip", f, file_name="clip_ellia.mp4")
                st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 4 : AVIS ---
with tabs[3]:
    st.header("⭐ Votre Avis")
    with st.form("feedback"):
        rate = st.select_slider("Note", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
        nom = st.text_input("Pseudo")
        if st.form_submit_button("Envoyer"):
            st.success(f"Merci {nom} !")

st.markdown("---")
st.caption("© 2026 Ellia Flow Studio Pro - Créativité illimitée")
