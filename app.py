import streamlit as st
import pymupdf4llm
import tempfile
import os
import google.generativeai as genai

# 1. AI Баптаулары (API Key-ді осы жерге қоясың)
# Назар аудар: API кілтті Streamlit secrets-ке салған дұрыс
GOOGLE_API_KEY = "AIzaSyBqjnIpUnBOegklTpoIsLo2suvl2fk3ibg" 
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Тілдер сөздігі (AI үшін мәтіндер)
languages = {
    "KZ": {
        "title": "🤖 AI-ready Converter + Chat",
        "upload_label": "PDF файлды таңдаңыз",
        "chat_header": "📄 Осы файл бойынша сұрақ қойыңыз:",
        "chat_placeholder": "Бұл құжат не туралы?",
        "footer": "Жасалған: Almagmur"
    },
    "RU": {
        "title": "🤖 AI-ready Converter + Chat",
        "upload_label": "Выберите PDF файл",
        "chat_header": "📄 Задайте вопрос по этому файлу:",
        "chat_placeholder": "О чем этот документ?",
        "footer": "Создано: Almagmur"
    },
    "EN": {
        "title": "🤖 AI-ready Converter + Chat",
        "upload_label": "Choose a PDF file",
        "chat_header": "📄 Ask a question about this file:",
        "chat_placeholder": "What is this document about?",
        "footer": "Created by: Almagmur"
    }
}

# (CSS стильдері мен тіл таңдау бұрынғыдай қалады...)
col1, col2 = st.columns([4, 1])
with col2:
    lang_choice = st.selectbox("🌐", ["KZ", "RU", "EN"], label_visibility="collapsed")
t = languages[lang_choice]

st.title(t["title"])

uploaded_file = st.file_uploader(t["upload_label"], type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    md_text = pymupdf4llm.to_markdown(tmp_path)
    os.remove(tmp_path)

    st.success("✅ Файл өңделді!")
    
    # --- AI CHAT БӨЛІМІ ---
    st.markdown("---")
    st.subheader(t["chat_header"])
    
    user_question = st.text_input(t["chat_placeholder"])
    
    if user_question:
        with st.spinner("AI ойланып жатыр..."):
            # Файлдың мәтінін сұрақпен бірге AI-ға жібереміз
            full_prompt = f"Контекст (құжат мәтіні):\n{md_text}\n\nСұрақ: {user_question}"
            response = model.generate_content(full_prompt)
            st.write("🤖 **AI Жауабы:**")
            st.info(response.text)
    # ----------------------

st.markdown(f'<div class="custom-footer">© 2026 AI Converter | {t["footer"]}</div>', unsafe_allow_html=True)
