import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image

from utils.modul_llm_vision import GeminiAPI

# Pengaturan awal API
api_key = "GEMINI API"
gemini_api = GeminiAPI(api_key)

# Judul Aplikasi
st.title("Kalkulator AI")

# Inisialisasi Canvas
if 'canvas' not in st.session_state:
    st.session_state.canvas = np.zeros((480, 640, 3), dtype="uint8")

# Membuat Canvas yang Dapat Digambar
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    width=640,
    height=480,
    drawing_mode="freedraw",
    key="canvas",
    update_streamlit=True,
)

# Tombol Analisis
if st.button("Analisis"):
    if canvas_result.image_data is not None:
         # Menyimpan dan Menganalisis Gambar
        img = Image.fromarray(canvas_result.image_data.astype("uint8"), 'RGBA')
        img.save("canvas.png")
        
        # Upload gambar dan generate payload untuk Gemini API
        payload = gemini_api.generate_payload("canvas.png", "Selesaikan masalah matematika berikut dan tulis dalam format markdown dan jika menulis equation menggunakan format latex yang diapit dengan $$. Penulisan harus jelas terlihat jika dimasukkan ke dalam st.markdown() dan langkah-langkah equationnya harus dipisahkan dengan new line")

        # Menampilkan Solusi dari AI
        st.header("Jawaban AI")
        response = gemini_api.get_response()
        st.markdown(response)
