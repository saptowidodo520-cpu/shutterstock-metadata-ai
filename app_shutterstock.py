import streamlit as st
from google import genai
import google.genai.types as types
from PIL import Image

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Stock Metadata AI", layout="centered")

st.title("📸 Stock Metadata AI")
st.caption("Generator Deskripsi & Keyword Otomatis untuk Shutterstock (SDK 2026)")

# API Key Anda yang sudah aktif
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    # Jika dijalankan di laptop tanpa secrets, Anda bisa input lewat sidebar browser
    API_KEY = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

if API_KEY:
    # Pilih Tipe Media
    option = st.radio("Pilih Tipe Media:", ["Gambar", "Video"])
    
    if option == "Gambar":
        file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
    else:
        file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

    if file:
        if option == "Gambar":
            st.image(file, use_column_width=True)
        else:
            st.video(file)

        if st.button("🚀 Generate Metadata"):
            with st.spinner("AI sedang menganalisis konten dengan Gemini 1.5 Flash..."):
                try:
                    # Menggunakan Client SDK Baru
                    client = genai.Client(api_key=API_KEY)
                    
                    prompt = """
                    You are an expert Stock Photography and Video SEO Specialist. 
                    Analyze the uploaded file and provide:
                    1. Description (Title): 7-15 words, SEO-friendly, English, commercial context, no subjective words.
                    2. Keywords: Exactly 50 relevant keywords, English, comma-separated, covering main subject, activity, environment, and abstract concepts.
                    
                    Strictly format the output as follows:
                    TITLE: [put title here]
                    KEYWORDS: [put keywords here]
                    """
                    
                    # Proses berdasarkan tipe media menggunakan model terbaru
                    if option == "Gambar":
                        img = Image.open(file)
                        response = client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=[prompt, img]
                        )
                    else:
                        video_bytes = file.read()
                        video_part = types.Part.from_bytes(data=video_bytes, mime_type="video/mp4")
                        response = client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=[prompt, video_part]
                        )
                    
                    res_text = response.text
                    
                    # Parsing Hasil Title dan Keywords
                    try:
                        title = res_text.split("TITLE:")[1].split("KEYWORDS:")[0].strip()
                        keywords = res_text.split("KEYWORDS:")[1].strip()
                    except:
                        title = "Gagal memproses judul otomatis."
                        keywords = res_text

                    st.success("Analisis Selesai!")
                    
                    # Kotak output dengan tombol salin instan
                    st.subheader("📝 Title (Copy Below)")
                    st.code(title, language=None)
                    
                    st.subheader("🔑 Keywords (Copy Below)")
                    st.code(keywords, language=None)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan sistem: {e}")
