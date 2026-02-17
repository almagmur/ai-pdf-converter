import streamlit as st
import pymupdf4llm
import tempfile
import os

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