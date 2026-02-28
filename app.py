import streamlit as st
import os
from gtts import gTTS
from pydub import AudioSegment
import io
import tempfile

# Imports MoviePy
try:
    from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip
except ImportError:
    from moviepy.video.VideoClip import ImageClip, TextClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- CONFIGURATION DU STUDIO ---
st.set_page_config(page_title="ELLI-IA Studio Pro", layout="wide")
st.title("🎬 ELLI-IA : Studio de Production & Clonage")

# --- 1. SÉPARATEUR DE PAROLES ---
st.header("✂️ 1. Séparation & Paroles")
file_to_split = st.file_uploader("Chargez l'instrumental (MP3/WAV)", type=["mp3", "wav"], key="instr_file")

paroles_finales = ""
if file_to_split:
    st.audio(file_to_split)
    paroles_generees = "Voici les paroles extraites par l'IA d'ELLI-IA..."
    paroles_finales = st.text_area("Modifier les paroles :", value=paroles_generees, height=100)
    st.download_button("📥 Télécharger Paroles (.txt)", paroles_finales, "paroles.txt")

# --- 2. VOIX & CLONAGE (NOUVEAU) ---
st.divider()
st.header("🎙️ 2. Voix & Clonage")
methode_voix = st.selectbox("Choisis ta méthode :", 
                             ["🎤 Enregistrement Direct", "🤖 Texte vers IA Simple", "👤 Clonage de Voix (Échantillon)"])

voix_pour_mix = None

if methode_voix == "🎤 Enregistrement Direct":
    audio_mic = st.audio_input("Enregistre ton chant")
    if audio_mic:
        voix_pour_mix = AudioSegment.from_file(audio_mic)
        st.success("Voix enregistrée !")

elif methode_voix == "🤖 Texte vers IA Simple":
    txt_simple = st.text_input("Texte à dire :", "Bonjour c'est ELLI-IA")
    if st.button("Générer Voix Standard"):
        tts = gTTS(text=txt_simple, lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        voix_pour_mix = AudioSegment.from_file(fp, format="mp3")
        st.audio(fp)

elif methode_voix == "👤 Clonage de Voix (Échantillon)":
    st.info("Chargez un court échantillon de votre voix (10s) pour que l'IA l'imite.")
    sample_file = st.file_uploader("Échantillon de voix (MP3/WAV)", type=["mp3", "wav"], key="clone_sample")
    texte_clone = st.text_area("Texte que la voix clonée doit dire :")
    
    if sample_file and texte_clone:
        if st.button("Démarrer le Clonage"):
            with st.spinner("L'IA apprend votre voix..."):
                # Note: Le vrai clonage demande une API comme ElevenLabs. 
                # Ici, on simule le processus pour l'interface.
                st.warning("Système de clonage prêt. (Connectez une clé API ElevenLabs pour le rendu réel)")
                # Simulation de l'audio cloné
                tts = gTTS(text=texte_clone, lang='fr') 
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                voix_pour_mix = AudioSegment.from_file(fp, format="mp3")
                st.audio(fp)

# --- 3. MIXAGE & ÉCOUTE ---
st.divider()
st.header("🎵 3. Mixage & Écoute")
audio_mix_final = None

if file_to_split and voix_pour_mix:
    if st.button("🎚️ Créer le Mixage Final"):
        instr = AudioSegment.from_file(file_to_split)
        mix = instr.overlay(voix_pour_mix)
        
        buf = io.BytesIO()
        mix.export(buf, format="mp3")
        audio_mix_final = buf.getvalue()
        
        st.subheader("🎧 Écoutez avant de télécharger")
        st.audio(audio_mix_final, format="audio/mp3")
        st.download_button("📥 Télécharger Musique (MP3)", audio_mix_final, "musique_mixee.mp3")

# --- 4. CLIP VIDÉO ---
st.divider()
st.header("🎞️ 4. Clip Vidéo avec Paroles")
media_fond = st.file_uploader("Image ou Vidéo de fond", type=["jpg", "png", "mp4"])

if audio_mix_final and media_fond:
    if st.button("🎬 Générer le Clip Final"):
        with st.spinner("Montage du clip..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fa:
                fa.write(audio_mix_final)
                p_audio = fa.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(media_fond.name)[1]) as fm:
                fm.write(media_fond.read())
                p_media = fm.name

            try:
                audio_clip = AudioFileClip(p_audio)
                if media_fond.type.startswith("image"):
                    bg = ImageClip(p_media).set_duration(audio_clip.duration)
                else:
                    bg = VideoFileClip(p_media).subclip(0, min(VideoFileClip(p_media).duration, audio_clip.duration))
                
                txt = TextClip(paroles_finales, fontsize=40, color='white', font='Arial', 
                               method='caption', size=(bg.w*0.8, None)).set_duration(audio_clip.duration).set_pos('bottom')
                
                final_video = CompositeVideoClip([bg, txt]).set_audio(audio_clip)
                final_video.write_videofile("mon_clip.mp4", fps=24, codec="libx264")
                
                st.subheader("📺 Regardez le clip avant de télécharger")
                st.video("mon_clip.mp4")
                with open("mon_clip.mp4", "rb") as vf:
                    st.download_button("📥 Télécharger Clip (MP4)", vf, "clip_final.mp4")
            except Exception as e:
                st.error(f"Erreur : {e}")

