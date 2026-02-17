import streamlit as st
import pymupdf4llm
import tempfile
import os

# 1. Тілдер сөздігі
languages = {
    "KZ": {
        "title": "🤖 AI-ready Мәлімет Конвертері",
        "desc": "PDF файлды AI түсінетін Markdown форматына тез арада айналдырыңыз.",
        "upload_label": "PDF файлды таңдаңыз",
        "spinner": "Өңдеу жүріп жатыр...",
        "success": "Дайын!",
        "result_label": "Markdown нәтижесі:",
        "download_btn": "Markdown файлды жүктеп алу"
    },
    "RU": {
        "title": "🤖 Конвертер данных для ИИ",
        "desc": "Превратите ваш PDF в Markdown формат, который идеально понимает ИИ.",
        "upload_label": "Выберите PDF файл",
        "spinner": "Идет обработка...",
        "success": "Готово!",
        "result_label": "Результат Markdown:",
        "download_btn": "Скачать Markdown файл"
    },
    "EN": {
        "title": "🤖 AI-ready Data Converter",
        "desc": "Convert your PDF into AI-friendly Markdown format instantly.",
        "upload_label": "Choose a PDF file",
        "spinner": "Processing...",
        "success": "Done!",
        "result_label": "Markdown Result:",
        "download_btn": "Download Markdown file"
    }
}

# 2. Тіл таңдауды басты беттің жоғарғы жағына шығару (Sidebar-сыз)
col1, col2 = st.columns([4, 1]) # Бетті екіге бөлу

with col2:
    lang_choice = st.selectbox("🌐", ["KZ", "RU", "EN"], label_visibility="collapsed")

t = languages[lang_choice]

# 3. Интерфейс
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