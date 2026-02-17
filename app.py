import streamlit as st
import pymupdf4llm
import tempfile
import os

import streamlit as st
import pymupdf4llm
import tempfile
import os

# 1. Тілдер сөздігін баптау
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

# 2. Тіл таңдау мәзірі (Sidebar-да)
lang_choice = st.sidebar.selectbox("Language / Тіл / Язык", ["KZ", "RU", "EN"])
t = languages[lang_choice]

# 3. Сайттың интерфейсі
st.title(t["title"])
st.write(t["desc"])

# Файл жүктеу батырмасы
uploaded_file = st.file_uploader(t["upload_label"], type="pdf")

if uploaded_file is not None:
    with st.spinner(t["spinner"]):
        # Уақытша файл жасау
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # Конвертация жасау
            md_text = pymupdf4llm.to_markdown(tmp_path)
            
            st.success(t["success"])

            # Нәтижені сайтта көрсету
            st.text_area(t["result_label"], md_text, height=300)

            # Жүктеп алу батырмасы
            st.download_button(
                label=t["download_btn"],
                data=md_text,
                file_name="converted_data.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"Error / Қате: {e}")
        finally:
            # Уақытша файлды өшіру
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

# Сайттың тақырыбы
st.title("📄 AI-ready Data Converter")
st.write("PDF файлды AI түсінетін Markdown форматына тез арада айналдырыңыз.")

# Файл жүктеу батырмасы
uploaded_file = st.file_uploader("PDF файлды таңдаңыз", type="pdf")

if uploaded_file is not None:
    with st.spinner('Өңдеу жүріп жатыр...'):
        # Уақытша файл жасау
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # Конвертация жасау
            md_text = pymupdf4llm.to_markdown(tmp_path)
            
            st.success("Дайын!")
            
            # Нәтижені сайтта көрсету
            st.text_area("Markdown нәтижесі:", md_text, height=300)
            
            # Жүктеп алу батырмасы
            st.download_button(
                label="Markdown файлды жүктеп алу",
                data=md_text,
                file_name="converted_data.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"Қате орын алды: {e}")
        finally:
            os.remove(tmp_path)