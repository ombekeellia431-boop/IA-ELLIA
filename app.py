
import streamlit as st
import os
import random
import numpy as np
from gtts import gTTS
from music21 import note, stream, tempo, midi
from pydub import AudioSegment
from moviepy.editor import ImageClip, AudiofileClip,VideofileClip
import io
# --- CONFIGURATION DU STUDIO ---
st.set_page_config(page_title="ELLI-IA Studio Pro", layout="wide")
st.title("🎬 ELLI-IA : Studio de Production & Séparation")

# --- 1. SÉPARATEUR DE PAROLES (NOUVEAU) ---
st.header("✂️ 1. Séparateur de Paroles")
st.write("Isolez la voix d'une chanson pour créer votre propre remix.")
file_to_split = st.file_uploader("Chargez un morceau (MP3/WAV)", type=["mp3", "wav"], key="split")

path_paroles_extraites = "paroles_extraites.mp3"

if file_to_split:
    st.audio(file_to_split)
    if st.button("🚀 Extraire les paroles maintenant"):
        with st.spinner("Analyse et extraction..."):
            # Technique d'inversion de phase (légère pour le serveur)
            sound = AudioSegment.from_file(file_to_split)
            channels = sound.split_to_mono()
            if len(channels) >= 2:
                voix = channels[0].overlay(channels[1].invert_phase())
                voix.export(path_paroles_extraites, format="mp3")
                st.success("Extraction terminée !")
                st.audio(path_paroles_extraites)
                with open(path_paroles_extraites, "rb") as f:
                    st.download_button("📥 Télécharger les paroles seules", f, "paroles_elli_ia.mp3")
            else:
                st.error("Le fichier doit être en stéréo pour séparer les pistes.")

# --- 2. ENREGISTREMENT ET CLONAGE ---
st.header("🎙️ 2. Voix & Clonage")
choix_v = st.radio("Source :", ["Microphone", "Texte IA"])
path_voix = "voix_finale.mp3"

if choix_v == "Microphone":
    audio_mic = st.audio_input("Parlez ici pour enregistrer")
    if audio_mic:
        with open(path_voix, "wb") as f: f.write(audio_mic.read())
else:
    txt = st.text_area("Texte à dire :", "Mon nouveau hit avec ELLI-IA")
    if st.button("Générer la Voix IA"):
        gTTS(text=txt, lang='fr').save(path_voix)

if os.path.exists(path_voix):
    st.audio(path_voix)
    with open(path_voix, "rb") as f:
        st.download_button("📥 Télécharger la voix", f, "ma_voix.mp3")

# --- 3. INSTRUMENTAL AUTOMATIQUE ---
st.header("🎹 3. Musique de Fond")
if st.button("🎼 Générer un Instrumental"):
    s = stream.Stream()
    s.append(tempo.MetronomeMark(number=110))
    for _ in range(8):
        s.append(note.Note(random.choice(['C4', 'G4', 'A4']), quarterLength=1.0))
    mf = midi.translate.streamToMidiFile(s)
    mf.open("instru.mid", 'wb')
    mf.write()
    mf.close()
    st.success("Musique générée !")

# --- 4. CLIP VIDÉO FINAL ---
st.header("🖼️ 4. Création du Clip Vidéo")
media_file = st.file_uploader("Image ou Vidéo pour le fond", type=["jpg", "png", "mp4"])

if st.button("🎬 Créer le Clip avec ma Musique"):
    if os.path.exists(path_voix) and media_file:
        with st.spinner("Montage en cours..."):
            audio = AudioFileClip(path_voix)
            # Sauvegarde temporaire du média
            ext = media_file.name.split('.')[-1]
            with open(f"temp.{ext}", "wb") as f: f.write(media_file.read())
            
            if ext in ["jpg", "png"]:
                clip = ImageClip(f"temp.{ext}").set_duration(audio.duration)
            else:
                clip = VideoFileClip(f"temp.{ext}").subclip(0, min(10, audio.duration))
            
            clip = clip.set_audio(audio)
            clip.write_videofile("clip_final.mp4", fps=24)
            st.video("clip_final.mp4")
            with open("clip_final.mp4", "rb") as f:
                st.download_button("📥 Télécharger le CLIP VIDÉO", f, "mon_chef_doeuvre.mp4")
    else:
        st.warning("Générez une voix et ajoutez un fichier image/vidéo d'abord.")
