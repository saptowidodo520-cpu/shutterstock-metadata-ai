import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Stock Metadata AI", layout="centered")
st.title("📸 Stock Metadata AI (Mode Diagnosis)")
st.caption("Uji Coba Jalur Langsung Tanpa Brankas Secrets")

# Kita munculkan kotak input terbuka (tanpa sensor) agar hurufnya bisa dicek manual
API_KEY = st.text_input("PASTE API KEY JALUR PRIBADI ANDA DI SINI:", type="default")

if API_KEY:
    st.info(f"Status Kunci -> Panjang: {len(API_KEY)} karakter | Awalan: {API_KEY[:6]}...")
    
    file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
    if file:
        st.image(file, use_column_width=True)
        
        if st.button("🚀 Test Tembus Google"):
            with st.spinner("Sedang mengetuk pintu server Google..."):
                try:
                    # Jalur pintas langsung menggunakan kunci dari kotak teks
                    client = genai.Client(api_key=API_KEY.strip())
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=["Respond with exactly one word: Success", Image.open(file)]
                    )
                    st.success(f"🎉 LUAR BIASA BERHASIL! Respon Google: {response.text}")
                    st.balloons()
                except Exception as e:
                    st.error(f"Google menolak di pintu depan karena: {e}")
else:
    st.warning("Silakan tempel (paste) API Key gres Anda pada kotak di atas untuk memulai tes.")
