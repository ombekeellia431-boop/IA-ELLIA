import streamlit as st
import os
import io
import tempfile
import pandas as pd
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
import whisper
import urllib.parse

# Imports MoviePy
try:
    from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip
except ImportError:
    from moviepy.video.VideoClip import ImageClip, TextClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- FONCTION POUR SAUVEGARDER LA NOTE ---
def sauvegarder_note(note_val):
    file_path = "notes.csv"
    nouvelle_note = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "note": note_val + 1}
    df = pd.DataFrame([nouvelle_note])
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

# --- CONFIGURATION DU STUDIO ---
st.set_page_config(page_title="ELLI-IA Studio Ultimate", layout="wide")
st.title("🎬 ELLI-IA : Studio de Production IA Complet")

if 'paroles' not in st.session_state:
    st.session_state['paroles'] = "Les paroles apparaîtront ici..."

# --- 1. MUSIQUE & EXTRACTION DE PAROLES ---
st.header("✂️ 1. Musique & Extraction de Paroles")
file_to_split = st.file_uploader("Chargez l'instrumental (MP3/WAV)", type=["mp3", "wav"])

if file_to_split:
    st.audio(file_to_split)
    if st.button("🤖 Extraire les paroles avec l'IA (Whisper)"):
        with st.spinner("L'IA analyse l'audio..."):
            model = whisper.load_model("base")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(file_to_split.getvalue())
                path_audio = tmp.name
            result = model.transcribe(path_audio)
            st.session_state['paroles'] = result["text"]
    
    paroles_finales = st.text_area("Vérifiez et modifiez les paroles :", value=st.session_state['paroles'], height=150)
    st.session_state['paroles'] = paroles_finales

# --- 2. VOIX & CLONAGE ---
st.divider()
st.header("🎙️ 2. Voix & Clonage")
methode_voix = st.selectbox("Méthode :", ["🎤 Enregistrement Direct", "🤖 Texte vers IA", "👤 Clonage"])
voix_pour_mix = None

if methode_voix == "🎤 Enregistrement Direct":
    audio_mic = st.audio_input("Chantez ici")
    if audio_mic:
        voix_pour_mix = AudioSegment.from_file(audio_mic)
elif methode_voix == "🤖 Texte vers IA":
    txt_ia = st.text_input("Texte :", "Production ELLI-IA")
    if st.button("Générer la voix"):
        tts = gTTS(text=txt_ia, lang='fr')
        fp = io.BytesIO(); tts.write_to_fp(fp); fp.seek(0)
        voix_pour_mix = AudioSegment.from_file(fp, format="mp3"); st.audio(fp)
elif methode_voix == "👤 Clonage":
    if st.button("Démarrer le Clonage"):
        tts = gTTS(text=st.session_state['paroles'], lang='fr')
        fp = io.BytesIO(); tts.write_to_fp(fp); fp.seek(0)
        voix_pour_mix = AudioSegment.from_file(fp, format="mp3"); st.audio(fp)

# --- 3. MIXAGE & ÉCOUTE ---
st.divider()
st.header("🎵 3. Mixage & Écoute")
audio_mix_final = None
if file_to_split and voix_pour_mix:
    if st.button("🎚️ Mixer"):
        instr = AudioSegment.from_file(file_to_split)
        mix = instr.overlay(voix_pour_mix)
        buf = io.BytesIO(); mix.export(buf, format="mp3")
        audio_mix_final = buf.getvalue()
        st.audio(audio_mix_final, format="audio/mp3")
        st.download_button("📥 Télécharger MP3", audio_mix_final, "mix.mp3")

# --- 4. CLIP VIDÉO ---
st.divider()
st.header("🎞️ 4. Montage du Clip Vidéo")
media_fond = st.file_uploader("Image ou Vidéo de fond", type=["jpg", "png", "mp4"])

if audio_mix_final and media_fond:
    col1, col2 = st.columns(2)
    with col1: couleur_texte = st.color_picker("Couleur du texte", "#FFFFFF")
    with col2: taille_police = st.slider("Taille", 20, 100, 50)

    if st.button("🎬 Générer le Clip Final"):
        with st.spinner("Montage en cours..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fa:
                fa.write(audio_mix_final); p_audio = fa.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(media_fond.name)[1]) as fm:
                fm.write(media_fond.read()); p_media = fm.name
            try:
                audio_clip = AudioFileClip(p_audio)
                if media_fond.type.startswith("image"):
                    bg = ImageClip(p_media).set_duration(            else:
                bg = VideoFileClip(p_media).subclip(0, min(VideoFileClip(p_media).duration, audio_clip.duration))

            # --- Création du texte ---
            txt = TextClip(
                st.session_state['paroles'], 
                fontsize=taille_police, 
                color=couleur_texte, 
                font='DejaVu-Sans-Bold', 
                method='caption', 
                size=(bg.w * 0.9, None),
                stroke_color='black',
                stroke_width=1
            ).set_duration(audio_clip.duration).set_pos(('center', 'bottom'))

            # --- Assemblage Final ---
            final_video = CompositeVideoClip([bg, txt]).set_audio(audio_clip)
            final_video.write_videofile("clip_final.mp4", fps=24, codec="libx264")
            st.video("clip_final.mp4")
            
            with open("clip_final.mp4", "rb") as vf:
                st.download_button("📩 Télécharger Clip (MP4)", vf, "clip_ellia_flow.mp4")

        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")







# --- 5. NOTATION & PARTAGE ---
st.divider()
st.header("🌟 Votre avis & Partage")
col_note, col_partage = st.columns(2)

with col_note:
    st.subheader("Notez l'application")
    note_utilisateur = st.feedback("stars")
    if note_utilisateur is not None:
        sauvegarder_note(note_utilisateur)
        st.success("Merci ! Note enregistrée.")
    
    # Affichage de la moyenne (Tableau de bord)
    if os.path.exists("notes.csv"):
        data_notes = pd.read_csv("notes.csv")
        moyenne = data_notes['note'].mean()
        st.metric("Note moyenne des utilisateurs", f"{moyenne:.1f} / 5")

with col_partage:
    st.subheader("Partagez le Studio")
    url_app = "https://votre-app-elli-ia.streamlit.app" 
    message = urllib.parse.quote(f"J'ai créé ma chanson avec ELLI-IA ! Teste-le ici : {url_app}")
    st.markdown(f"""
    <div style="display: flex; gap: 15px;">
        <a href="https://wa.me/?text={message}" target="_blank"><img src="https://img.icons8.com/color/48/whatsapp.png" width="45"></a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={url_app}" target="_blank"><img src="https://img.icons8.com/color/48/facebook-new.png" width="45"></a>
        <a href="https://www.tiktok.com/" target="_blank"><img src="https://img.icons8.com/color/48/tiktok.png" width="45"></a>
    </div>
    """, unsafe_allow_html=True)
