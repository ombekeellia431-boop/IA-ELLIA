import streamlit as st
import os
from gtts import gTTS

# --- SECTION VOIX IA ---
st.subheader("🎙️ Création de la Voix")
paroles = st.text_input("Entrez le texte à transformer en voix :", "Bonjour, voici ma nouvelle chanson.")

if st.button("Générer la Voix"):
    # 1. Création du fichier
    tts = gTTS(text=paroles, lang='fr')
    nom_fichier = "ma_voix_ia.mp3"
    tts.save(nom_fichier)
    
    # 2. FONCTION ÉCOUTER (Lecteur Audio)
    st.write("▶️ Écoutez votre extrait :")
    st.audio(nom_fichier)
    
    # 3. FONCTION TÉLÉCHARGER (Bouton)
    with open(nom_fichier, "rb") as file:
        st.download_button(
            label="💾 Télécharger la voix (MP3)",
            data=file,
            file_name="voix_elli_ia.mp3",
            mime="audio/mp3"
        )
    st.success("Prêt pour le téléchargement !")

# --- SECTION SÉPARATION DE MUSIQUE ---
st.divider()
st.subheader("✂️ Séparateur de Paroles")
# On utilise le chargeur de fichier que vous avez déjà
audio_upload = st.file_uploader("Choisissez un morceau", type=["mp3", "wav"])

if audio_upload:
    # Permet d'écouter le fichier original avant traitement
    st.write("Musique originale :")
    st.audio(audio_upload)
    
    if st.button("Extraire les paroles"):
        st.info("Traitement en cours...")
        # (Ici votre logique de séparation ajoutée précédemment)
        st.success("Paroles extraites !")
        # Ajouter ici le lecteur et le bouton pour le résultat extrait
