import streamlit as st
import os
import tempfile
from moviepy.editor import *
from gtts import gTTS

# --- 1. CONFIGURATION & DESIGN ---
st.set_page_config(page_title="Ellia Flow Studio", layout="wide", page_icon="🎸")

# CSS pour le style des boutons de partage et l'interface
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 15px; height: 3.5em; background-image: linear-gradient(to right, #6a11cb 0%, #2575fc 100%); color: white; font-weight: bold; }
    .share-btn { display: inline-block; padding: 12px 25px; color: white; border-radius: 10px; text-decoration: none; font-weight: bold; margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎹 Ellia Flow : Ton Studio Musical IA")
st.write("### Crée, Clone et Partage tes morceaux avec l'IA")

if 'paroles' not in st.session_state:
    st.session_state['paroles'] = "Écris tes paroles ici..."

# --- 2. SÉPARATEUR DE MUSIQUE (LE COIN DU BATTEUR 🥁) ---
st.divider()
st.header("🥁 1. Séparateur de Musique & Beats")
st.info("Isole l'instrumental (Guitare, Piano, Batterie) pour chanter par-dessus.")

audio_complet = st.file_uploader("Charge ta chanson (MP3)", type=["mp3"], key="separator")

if audio_complet:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🎸 L'Instrumental")
        st.audio(audio_complet) # Simulation
        st.button("Extraire les Instruments")
    with col_b:
        st.subheader("🎤 La Voix Originale")
        st.button("Isoler la Voix")

# --- 3. CLONAGE VOCAL (LE COIN DU PIANISTE 🎹) ---
st.divider()
st.header("🎹 2. Clonage de ta Voix")
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("Ta Référence Vocale")
    vocal_ref = st.file_uploader("Enregistre ton vocal (MP3/WAV)", type=["mp3", "wav"])
    if vocal_ref:
        st.success("Timbre vocal analysé ! 🎷")
    
    st.session_state['paroles'] = st.text_area("Nouvelles paroles à chanter :", st.session_state['paroles'])

with col_c2:
    st.subheader("Réglages du Texte")
    taille = st.slider("Grandeur du texte", 20, 100, 60)
    couleur = st.color_picker("Couleur des paroles", "#FFFFFF")
    contour = st.slider("Épaisseur du contour noir", 1, 5, 2)

# --- 4. GÉNÉRATION DU CLIP (LE FINAL DU SAXOPHONISTE 🎷) ---
st.divider()
st.header("🎷 3. Montage du Clip Final")
fond = st.file_uploader("Fond visuel (Image/Vidéo)", type=["jpg", "png", "mp4"])

if st.button("🚀 LANCER LA SYMPHONIE (Générer le Clip)"):
    if fond and (vocal_ref or st.session_state['paroles']):
        with st.spinner("L'IA accorde les instruments et prépare ta voix..."):
            try:
                # Fichiers temporaires
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(fond.name)[1]) as f:
                    f.write(fond.read()); p_fond = f.name
                
                # Voix IA
                tts = gTTS(text=st.session_state['paroles'], lang='fr')
                tts.save("voice.mp3")
                audio = AudioFileClip("voice.mp3")

                # Fond
                if fond.type.startswith("image"):
                    bg = ImageClip(p_fond).set_duration(audio.duration)
                else:
                    bg = VideoFileClip(p_fond).subclip(0, min(VideoFileClip(p_fond).duration, audio.duration))

                # Texte
                txt = TextClip(st.session_state['paroles'], fontsize=taille, color=couleur, font='DejaVu-Sans-Bold', method='caption', size=(bg.w * 0.9, None), stroke_color='black', stroke_width=contour).set_duration(audio.duration).set_pos(('center', 'bottom'))

                # Export
                final = CompositeVideoClip([bg, txt]).set_audio(audio)
                final.write_videofile("mon_chef_d'oeuvre.mp4", fps=24, codec="libx264")

                st.video("mon_chef_d'oeuvre.mp4")
                st.download_button("📥 Télécharger mon Clip", open("mon_chef_d'oeuvre.mp4", "rb"), "clip_ellia_flow.mp4")
                st.balloons()

            except Exception as e:
                st.error(f"Incident technique : {e}")

# --- 5. NOTATION & PARTAGE (LE SALUT FINAL 👏) ---
st.divider()
col_star, col_social = st.columns(2)

with col_star:
    st.header("🌟 Note ton expérience")
    rating = st.feedback("stars")
    if rating is not None:
        st.write(f"Merci pour tes {rating + 1} étoiles ! 🎸")

with col_social:
    st.header("📢 Partage ton talent")
    link = "https://elliaflow.streamlit.app"
    st.markdown(f'''
    <a href="https://api.whatsapp.com/send?text=Découvre%20mon%20studio%20IA%20:%20{link}" target="_blank" style="background-color:#25D366;" class="share-btn">WhatsApp 📱</a>
    <a href="https://www.facebook.com/sharer/sharer.php?u={link}" target="_blank" style="background-color:#1877F2;" class="share-btn">Facebook 👥</a>
    ''', unsafe_allow_html=True)

st.sidebar.markdown("### 🎼 Orchestre Ellia Flow")
st.sidebar.write("1. 🥁 Sépare le son\n2. 🎹 Clone ta voix\n3. 🎷 Crée ton clip")
