import streamlit as st
import pymupdf4llm
import tempfile
import os
import google.generativeai as genai

# 1. AI Баптаулары
API_KEY = "AIzaSyBqjnipuNBOegklTpoIsLo2suvI2fk3ibg" 
genai.configure(api_key=API_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Almagmur AI", page_icon="⚡", layout="wide")

# 2. Дизайн (Dark Premium + Pricing Cards)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #FF4B4B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px;
    }

    /* Тарифтік карталар стилі */
    .pricing-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 50px;
    }
    .price-card {
        background-color: #1A1C23;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #30363D;
        text-align: center;
        width: 100%;
        transition: 0.3s;
    }
    .price-card:hover {
        border-color: #FF4B4B;
        transform: translateY(-10px);
    }
    .price-card h3 { color: #A0AEC0; font-size: 1.2rem; }
    .price-card h2 { font-size: 2.5rem; margin: 10px 0; }
    .price-card ul { list-style: none; padding: 0; color: #718096; }
    .price-card li { margin: 10px 0; }
    
    /* Батырмалар */
    div.stButton > button {
        background: linear-gradient(90deg, #FF4B4B 0%, #ED213A 100%);
        color: white; border: none; border-radius: 10px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Басты бөлім
st.markdown('<h1 class="hero-title">Almagmur AI Engine</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#A0AEC0;">Құжаттарды талдаудың жаңа деңгейі</p>', unsafe_allow_html=True)

# Файл жүктеу
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        st.success("Файлдар жүктелді! AI талдауға дайын.")

st.markdown("---")

# 4. PRICING TABLE (Сен сұраған бөлім)
st.markdown("<h2 style='text-align: center;'>Тарифтік жоспарлар</h2>", unsafe_allow_html=True)

p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    st.markdown("""
    <div class="price-card">
        <h3>СТАРТЕР</h3>
        <h2>0 ₸</h2>
        <ul>
            <li>✅ 50 файл айына</li>
            <li>✅ Gemini 1.5 Flash</li>
            <li>✅ Markdown экспорты</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Тегін бастау", key="p1"):
        st.toast("Стартер жоспары қосылды!")

with p_col2:
    st.markdown("""
    <div class="price-card" style="border: 1px solid #FF4B4B;">
        <h3 style="color: #FF4B4B;">PRO</h3>
        <h2>9 900 ₸</h2>
        <ul>
            <li>✅ Шексіз файлдар</li>
            <li>✅ Gemini 1.5 Pro (Ultra)</li>
            <li>✅ Приоритетті қолдау</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("PRO-ға өту", key="p2"):
        st.toast("Төлем бетіне бағыттау...")

with p_col3:
    st.markdown("""
    <div class="price-card">
        <h3>БИЗНЕС</h3>
        <h2>Жеке</h2>
        <ul>
            <li>✅ Командалық қолжетімділік</li>
            <li>✅ API интеграция</li>
            <li>✅ Kaspi Pay шешімдері</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Консультация", key="p3"):
        st.toast("Менеджер хабарласады")

# Footer
st.markdown("<br><p style='text-align: center; color: #4A5568;'>© 2026 Almagmur AI | Professional Edition</p>", unsafe_allow_html=True)

