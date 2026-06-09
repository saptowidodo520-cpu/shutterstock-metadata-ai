import streamlit as st
from google import genai
import google.genai.types as types
from PIL import Image

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Stock Metadata AI", layout="centered")

st.title("📸 Stock Metadata AI")
st.caption("Generator Deskripsi & 50 Keyword Otomatis untuk Shutterstock")

# Sistem Keamanan: Mengambil API Key dari Brankas Secrets atau Sidebar Browser
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

if API_KEY:
    # Pilih Tipe Media yang akan di-submit
    option = st.radio("Pilih Tipe Media:", ["Gambar", "Video"])
    
    if option == "Gambar":
        file = st.file_uploader("Upload Foto Anda", type=["jpg", "jpeg", "png"])
    else:
        file = st.file_uploader("Upload Video Anda", type=["mp4", "mov", "avi"])

    if file:
        if option == "Gambar":
            st.image(file, use_column_width=True)
        else:
            st.video(file)

        if st.button("🚀 Generate Metadata"):
            with st.spinner("AI sedang menganalisis konten untuk Shutterstock..."):
                try:
                    # Menggunakan Client SDK dengan kunci gres Anda
                    client = genai.Client(api_key=API_KEY.strip())
                    
                    prompt = """
                    You are an expert Stock Photography and Video SEO Specialist. 
                    Analyze the uploaded file and provide high-quality commercial metadata:
                    1. Description (Title): 7-15 words, highly SEO-friendly, written in English, focus on commercial context, purely descriptive, no subjective words (DO NOT use words like beautiful, amazing, stunning).
                    2. Keywords: Exactly 50 highly relevant keywords, in English, comma-separated, covering main subject, color, texture, environment, lighting, and abstract commercial concepts.
                    
                    Strictly format the output exactly as follows:
                    TITLE: [put title here]
                    KEYWORDS: [put keywords here]
                    """
                    
                    if option == "Gambar":
                        img = Image.open(file)
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[prompt, img]
                        )
                    else:
                        video_bytes = file.read()
                        video_part = types.Part.from_bytes(data=video_bytes, mime_type="video/mp4")
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[prompt, video_part]
                        )
                    
                    res_text = response.text
                    
                    # Proses pemisahan otomatis (Parsing)
                    try:
                        title = res_text.split("TITLE:")[1].split("KEYWORDS:")[0].strip()
                        keywords = res_text.split("KEYWORDS:")[1].strip()
                    except:
                        title = "Gagal memisahkan judul otomatis."
                        keywords = res_text

                    st.success("Analisis Selesai!")
                    
                    st.subheader("📝 Title / Description (Tinggal Klik Copy)")
                    st.code(title, language=None)
                    
                    st.subheader("🔑 50 Keywords (Tinggal Klik Copy)")
                    st.code(keywords, language=None)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan sistem: {e}")
else:
    st.warning("Silakan masukkan API Key Anda untuk memulai analisis.")
