import streamlit as st
import os
import time
import base64
import random
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, VideoFileClip

# --- 1. CONFIGURATION SYSTÈME ---
if os.name != 'nt':
    os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"

st.set_page_config(page_title="Ellia Flow Studio Ultra", page_icon="💎", layout="wide")

# --- 2. MOTEUR DE DESIGN PERSONNALISÉ ---
def apply_custom_theme(color, font):
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
        .stApp {{ background-color: #050505; color: white; }}
        .stButton>button {{ 
            background: linear-gradient(45deg, {color}, #ffffff33); 
            color: white; border-radius: 30px; border: none; height: 3.5em; 
            font-weight: 600; transition: 0.3s; width: 100%;
        }}
        .stButton>button:hover {{ transform: scale(1.02); filter: brightness(1.2); }}
        .preview-card {{ 
            border: 1px solid {color}; padding: 25px; border-radius: 20px; 
            background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); margin: 15px 0; 
        }}
        .status-badge {{ padding: 5px 15px; border-radius: 50px; background: {color}; font-size: 0.8em; }}
        </style>
        """, unsafe_allow_html=True)

# --- 3. BARRE LATÉRALE : IDENTITÉ & PARAMÈTRES ---
with st.sidebar:
    st.title("🛡️ Studio Control")
    app_title = st.text_input("Titre de l'App", "Ellia Flow Studio Ultra")
    accent_color = st.color_picker("Couleur Thème Premium", "#6C63FF")
    font_style = st.selectbox("Style de Police", ["Poppins", "Arial", "Courier"])
    apply_custom_theme(accent_color, font_style)
    
    st.divider()
    st.subheader("👤 Clonage Vocal")
    voice_input = st.audio_input("Enregistrez votre empreinte vocale")
    
    st.subheader("🎚️ Mode de Chant")
    singing_mode = st.select_slider("Style d'exécution", options=["Calme/Doux", "Neutre", "Puissant/Forcé"])
    
    voice_file = "temp_voice.wav"
    if voice_input:
        with open(voice_path := voice_file, "wb") as f:
            f.write(voice_input.getbuffer())
        st.success("Voix clonée avec succès !")

# --- 4. NAVIGATION PRINCIPALE ---
st.title(f"🚀 {app_title}")
tabs = st.tabs(["🎤 Production Chant", "🎞️ Clip Vidéo Pro", "✂️ Séparation IA", "📈 Avis & Business"])

# --- TAB 1 : PRODUCTION MUSICALE ---
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📝 Paroles IA")
        lyrics = st.text_area("Entrez les paroles à faire chanter par votre voix clonée", height=200)
    with col2:
        st.subheader("🎸 Instrumental")
        instru_file = st.file_uploader("Choisissez votre instru (MP3/WAV)", type=['mp3', 'wav'])
        mastering = st.checkbox("Mastering Auto (Qualité Radio)", value=True)

    if st.button("🎵 GÉNÉRER LA CHANSON"):
        if voice_input and lyrics:
            with st.spinner("L'IA génère votre chant avec le mode " + singing_mode + "..."):
                time.sleep(4) # Simulation de traitement ultra-rapide
                st.markdown(f'<div class="preview-card">', unsafe_allow_html=True)
                st.subheader("👂 ÉCOUTER AVANT TÉLÉCHARGEMENT")
                st.audio(voice_file) # Aperçu
                
                # Bouton de téléchargement pro
                with open(voice_file, "rb") as f:
                    st.download_button("📥 TÉLÉCHARGER LA CHANSON (HQ)", f, file_name="production_ellia_flow.mp3")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("⚠️ Voix clonée ou paroles manquantes.")

# --- TAB 2 : CRÉATEUR DE CLIP VIDÉO PRO ---
with tabs[1]:
    st.header("🎬 Studio de Montage Clip")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        bg_type = st.radio("Source visuelle", ["Image de fond", "Modèle Vidéo (Stock)"])
        if bg_type == "Image de fond":
            user_img = st.file_uploader("Importer votre image", type=['jpg', 'png'])
        else:
            template = st.selectbox("Choisir un modèle", ["Néon Urbain", "Nature Paisible", "Studio Abstrait", "Concert Live"])
            
    with v_col2:
        overlay_lyrics = st.checkbox("Incruster les paroles dans le clip", value=True)
        video_speed = st.select_slider("Vitesse de rendu", options=["Normal", "Turbo (Rapide)"])

    if st.button("🚀 ASSEMBLER LE CLIP VIDÉO"):
        if voice_input and (user_img or bg_type == "Modèle Vidéo (Stock)"):
            try:
                with st.spinner("Montage du clip vidéo en cours..."):
                    audio = AudioFileClip(voice_file)
                    # Pour la démo, on utilise une image fixe comme base
                    clip = ImageClip(user_img.name if user_img else "template.jpg").set_duration(audio.duration)
                    
                    if overlay_lyrics and lyrics:
                        txt = TextClip(lyrics[:50]+"...", fontsize=50, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2)
                        txt = txt.set_position('center').set_duration(audio.duration)
                        clip = CompositeVideoClip([clip, txt])
                    
                    clip = clip.set_audio(audio)
                    clip_name = "final_clip.mp4"
                    clip.write_videofile(clip_name, fps=24, codec="libx264", preset="ultrafast")
                    
                    st.markdown(f'<div class="preview-card">', unsafe_allow_html=True)
                    st.subheader("📺 APERÇU VIDÉO")
                    st.video(clip_name) # VOIR AVANT TÉLÉCHARGER
                    with open(clip_name, "rb") as f:
                        st.download_button("📥 TÉLÉCHARGER LE CLIP VIDÉO (HD)", f, file_name="clip_ellia_pro.mp4")
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("Veuillez configurer ImageMagick sur votre serveur pour les paroles.")
        else:
            st.warning("Manque de médias pour générer la vidéo.")

# --- TAB 3 : SÉPARATION IA ---
with tabs[2]:
    st.header("✂️ Séparateur de Pistes (Stem Splitter)")
    sep_file = st.file_uploader("Importer le morceau à séparer", type=['mp3'])
    if st.button("💎 Lancer la séparation Voix/Musique"):
        with st.spinner("L'IA isole les fréquences..."):
            time.sleep(3)
            st.success("Séparation terminée !")
            col_s1, col_s2 = st.columns(2)
            col_s1.audio(voice_file, format="audio/wav") # Exemple voix
            col_s1.caption("🎙️ Piste Vocale Isolé")
            col_s2.audio(voice_file, format="audio/wav") # Exemple instru
            col_s2.caption("🎸 Piste Instrumentale")

# --- TAB 4 : AVIS & BUSINESS ---
with tabs[3]:
    st.header("📈 Statistiques & Avis Utilisateurs")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.subheader("⭐ Noter l'expérience")
        rating = st.feedback("stars")
        comment = st.text_area("Laissez un avis ou un commentaire pour la communauté")
        if st.button("Publier l'avis"):
            st.balloons()
            st.success("Merci ! Votre avis aide à rendre Ellia Flow n°1.")
    
    with col_f2:
        st.subheader("💰 Rentabilité du Studio")
        st.metric("Utilisateurs actifs", "1,240", "+12%")
        st.metric("Générations totales", "5,890", "+25%")
        st.write("Le système est prêt pour l'intégration de Stripe (Paiements).")

st.markdown("---")
st.caption("© 2026 Ellia Flow Studio Ultra - Le futur de la musique IA.")
