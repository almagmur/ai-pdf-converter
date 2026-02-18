import streamlit as st
import pymupdf4llm
import tempfile
import os

# 1. Тілдер сөздігі (Үтірлер қойылды және footer қосылды)
languages = {
    "KZ": {
        "title": "🤖 AI-ready Мәлімет Конвертері",
        "desc": "PDF файлды AI түсінетін Markdown форматына тез арада айналдырыңыз.",
        "upload_label": "PDF файлды таңдаңыз",
        "spinner": "Өңдеу жүріп жатыр...",
        "success": "Дайын!",
        "result_label": "Markdown нәтижесі:",
        "download_btn": "Markdown файлды жүктеп алу",
        "footer": "Жасалған: Almagmur"
    },
    "RU": {
        "title": "🤖 Конвертер данных для ИИ",
        "desc": "Превратите ваш PDF в Markdown формат, который идеально понимает ИИ.",
        "upload_label": "Выберите PDF файл",
        "spinner": "Идет обработка...",
        "success": "Готово!",
        "result_label": "Результат Markdown:",
        "download_btn": "Скачать Markdown файл",
        "footer": "Создано: Almagmur"
    },
    "EN": {
        "title": "🤖 AI-ready Data Converter",
        "desc": "Convert your PDF into AI-friendly Markdown format instantly.",
        "upload_label": "Choose a PDF file",
        "spinner": "Processing...",
        "success": "Done!",
        "result_label": "Markdown Result:",
        "download_btn": "Download Markdown file",
        "footer": "Created by: Almagmur"
    }
}

# 2. CSS стильдері (Дизайнды жақсарту)
st.markdown("""
    <style>
    /* Батырманы әдемілеу */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
        color: white;
    }
    /* Төменгі жақтағы авторлық жазу стилі */
    .custom-footer {
        text-align: center;
        color: #808495;
        padding: 20px;
        font-size: 14px;
        margin-top: 50px;
        border-top: 1px solid #e6e9ef;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Тіл таңдау (Оң жақ жоғары бұрышта)
col1, col2 = st.columns([4, 1])
with col2:
    lang_choice = st.selectbox("🌐", ["KZ", "RU", "EN"], label_visibility="collapsed")

t = languages[lang_choice]

# 4. Негізгі интерфейс
st.title(t["title"])
st.write(t["desc"])

uploaded_file = st.file_uploader(t["upload_label"], type="pdf")

if uploaded_file is not None:
    with st.spinner(t["spinner"]):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            md_text = pymupdf4llm.to_markdown(tmp_path)
            st.success(t["success"])
            st.text_area(t["result_label"], md_text, height=300)

            st.download_button(
                label=t["download_btn"],
                data=md_text,
                file_name="converted_data.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

# 5. Footer (Авторлық қолтаңба)
st.markdown(f'<div class="custom-footer">© 2026 AI Converter | {t["footer"]}</div>', unsafe_allow_html=True)
