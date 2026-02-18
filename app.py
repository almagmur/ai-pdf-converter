import streamlit as st
from streamlit_option_menu import option_menu
import pymupdf4llm
import tempfile
import os
import google.generativeai as genai
from docx import Document

# --- ҚАУІПСІЗДІК БАПТАУЛАРЫ ---
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Almagmur AI", page_icon="⚡", layout="wide")

# --- ЖОҒАРҒЫ МӘЗІР (NAVIGATION) ---
selected = option_menu(
    menu_title=None, 
    options=["Home", "Features", "Pricing", "Support"], 
    icons=["house", "gear", "credit-card", "chat-dots"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1A1C23"},
        "icon": {"color": "#AB68FF", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#2D2F39"},
        "nav-link-selected": {"background-color": "#AB68FF"},
    }
)

# --- ФУНКЦИЯЛАР ---
def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# --- БЕТТЕР МАЗМҰНЫ ---

# 1. HOME БЕТІ (Негізгі файл жүктеу)
if selected == "Home":
    st.markdown("<h1 style='text-align: center;'>Transform Documents into AI-Ready Data</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Instantly convert PDF and Word into clean markdown.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_files = st.file_uploader("", type=["pdf", "docx"], accept_multiple_files=True)
        if uploaded_files:
            full_text = ""
            for file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                    tmp.write(file.getvalue())
                    tmp_path = tmp.name
                content = pymupdf4llm.to_markdown(tmp_path) if file.name.endswith('.pdf') else read_docx(tmp_path)
                full_text += content
                os.remove(tmp_path)
            
            st.success("Files ready!")
            user_q = st.text_input("Ask AI about your files:")
            if st.button("Transform Now →"):
                res = ai_model.generate_content(f"Context: {full_text[:10000]}\nQuestion: {user_q}")
                st.info(res.text)

# 2. FEATURES БЕТІ
if selected == "Features":
    st.header("✨ Күшті мүмкіндіктер")
    f_col1, f_col2, f_col3 = st.columns(3)
    f_col1.metric("Жылдамдық", "0.5 сек", "Fast")
    f_col2.metric("Дәлдік", "99%", "High")
    f_col3.metric("Форматтар", "PDF, DOCX", "Multi")
    st.write("Біздің жүйе кез келген күрделі құжатты AI түсінетін тілге айналдырады.")

# 3. PRICING БЕТІ
if selected == "Pricing":
    st.markdown("<h2 style='text-align: center;'>Простые и прозрачные тарифы</h2>", unsafe_allow_html=True)
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown('<div style="border:1px solid #30363D; padding:20px; border-radius:15px; text-align:center;"><h3>Free</h3><h2>0 ₸</h2><p>3 files/day</p></div>', unsafe_allow_html=True)
    with p_col2:
        st.markdown('<div style="border:2px solid #AB68FF; padding:20px; border-radius:15px; text-align:center;"><h3>Plus</h3><h2>4 900 ₸</h2><p>Unlimited access</p></div>', unsafe_allow_html=True)
        st.link_button("Upgrade to Plus", f"https://t.me/AlmagmurSupport_bot")

# 4. SUPPORT БЕТІ
if selected == "Support":
    st.header("🎧 Қолдау орталығы")
    st.write("Сұрақтарыңыз болса немесе тех-ақау шықса, ботқа жазыңыз.")
    st.link_button("✈️ Telegram Support Bot", "https://t.me/AlmagmurSupport_bot")




