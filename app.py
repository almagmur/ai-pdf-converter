import streamlit as st
import pymupdf4llm
import tempfile
import os

# 1. Тілдер сөздігі (Multi-file үшін мәтіндер қосылды)
languages = {
    "KZ": {
        "title": "🤖 AI-ready Multi-Converter",
        "desc": "Бірнеше PDF-ті бірден Markdown-ға айналдырыңыз.",
        "upload_label": "PDF файлдарды таңдаңыз (бірнешеу болады)",
        "spinner": "Файлдар өңделуде...",
        "success": "Барлық файлдар дайын!",
        "result_label": "Markdown нәтижесі:",
        "download_btn": "Markdown файлды жүктеп алу",
        "footer": "Жасалған: Almagmur"
    },
    "RU": {
        "title": "🤖 AI-ready Multi-Converter",
        "desc": "Превращайте несколько PDF в Markdown за один раз.",
        "upload_label": "Выберите PDF файлы (можно несколько)",
        "spinner": "Идет обработка файлов...",
        "success": "Все файлы готовы!",
        "result_label": "Результат Markdown:",
        "download_btn": "Скачать Markdown файл",
        "footer": "Создано: Almagmur"
    },
    "EN": {
        "title": "🤖 AI-ready Multi-Converter",
        "desc": "Convert multiple PDFs into Markdown instantly.",
        "upload_label": "Choose PDF files (multiple allowed)",
        "spinner": "Processing files...",
        "success": "All files done!",
        "result_label": "Markdown Result:",
        "download_btn": "Download Markdown file",
        "footer": "Created by: Almagmur"
    }
}

# 2. CSS стильдері
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background-color: #FF4B4B; color: white; font-weight: bold; }
    .custom-footer { text-align: center; color: #808495; padding: 20px; font-size: 14px; margin-top: 50px; border-top: 1px solid #e6e9ef; }
    </style>
    """, unsafe_allow_html=True)

# 3. Тіл таңдау
col1, col2 = st.columns([4, 1])
with col2:
    lang_choice = st.selectbox("🌐", ["KZ", "RU", "EN"], label_visibility="collapsed")
t = languages[lang_choice]

# 4. Интерфейс
st.title(t["title"])
st.write(t["desc"])

# accept_multiple_files=True — осы жерде сиқыр басталады!
uploaded_files = st.file_uploader(t["upload_label"], type="pdf", accept_multiple_files=True)

if uploaded_files:
    all_md_text = "" # Барлық файлдың мәтіні осында жиналады
    
    with st.spinner(t["spinner"]):
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            try:
                # Әр файлдың атын тақырып ретінде қосамыз
                all_md_text += f"\n\n# FILE: {uploaded_file.name}\n"
                all_md_text += pymupdf4llm.to_markdown(tmp_path)
            except Exception as e:
                st.error(f"Error in {uploaded_file.name}: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        st.success(t["success"])
        st.text_area(t["result_label"], all_md_text, height=400)

        st.download_button(
            label=t["download_btn"],
            data=all_md_text,
            file_name="all_converted_data.md",
            mime="text/markdown"
        )

# 5. Footer
st.markdown(f'<div class="custom-footer">© 2026 AI Converter | {t["footer"]}</div>', unsafe_allow_html=True)
