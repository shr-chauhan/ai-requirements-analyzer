import os
import streamlit as st
from io import BytesIO
from utils.file_parser import extract_text_from_docx, extract_text_from_pdf
from utils.generator import generate_all
from datetime import datetime
from docx import Document

st.set_page_config(page_title="AI Requirements Analyzer", layout="wide")

st.title("AI Requirements Analyzer — Streamlit")
st.markdown("Paste a business requirement or upload a doc (docx/pdf). The app will generate user stories, ACs, test cases and a mermaid flowchart using an LLM.")

# Read API key from Streamlit secrets or env
OPENAI_KEY = None
try:
    OPENAI_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_KEY:
    st.warning("No OPENAI_API_KEY found. Set OPENAI_API_KEY as an env var or Streamlit secret before using the app.")

uploaded_file = st.file_uploader("Upload .docx or .pdf (optional)", type=["docx", "pdf", "txt"]) 
text_input = st.text_area("Or paste requirement text here:", height=200)

if uploaded_file is not None and text_input.strip() == "":
    # read bytes and detect
    bytes_data = uploaded_file.read()
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            text_input = extract_text_from_docx(bytes_data)
        except Exception as e:
            st.error(f"Error reading docx: {e}")
    elif uploaded_file.type == "application/pdf":
        try:
            text_input = extract_text_from_pdf(bytes_data)
        except Exception as e:
            st.error(f"Error reading pdf: {e}")
    elif uploaded_file.type.startswith("text"):
        try:
            text_input = bytes_data.decode("utf-8")
        except UnicodeDecodeError:
            st.error("Error reading text file: Unable to decode as UTF-8. Please ensure the file is UTF-8 encoded.")
            text_input = ""

col1, col2 = st.columns([3,1])
with col2:
    model_choice = st.selectbox("Model", ["gpt-realtime-mini"], index=0)
    max_tokens = st.slider("Max tokens (per section)", min_value=256, max_value=3000, value=1200, step=128)

if st.button("Generate Requirements"):
    if not text_input.strip():
        st.error("Please paste a requirement or upload a document.")
    elif not OPENAI_KEY:
        st.error("OpenAI API key not found. Set OPENAI_API_KEY in env or Streamlit secrets.")
    else:
        with st.spinner("Generating..."):
            try:
                outputs = generate_all(text_input, prompts_dir="prompts", api_key=OPENAI_KEY, max_tokens=max_tokens)
            except Exception as e:
                st.error(f"Error generating requirements: {e}")
                st.stop()

        st.success("Generation complete")

        st.header("Executive Summary")
        st.markdown(outputs.get('summary',''))

        st.header("Epics & User Stories")
        st.markdown(outputs.get('user_stories',''))

        st.header("Acceptance Criteria")
        st.markdown(outputs.get('acceptance_criteria',''))

        st.header("Test Cases")
        st.markdown(outputs.get('test_cases',''))

        st.header("Mermaid Flowchart")
        mermaid_text = outputs.get('flows','')
        # render mermaid in an HTML component
        mermaid_html = f"""
        <script src=\"https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js\"></script>
        <div class=\"mermaid\">{mermaid_text}</div>
        <script>mermaid.initialize({{startOnLoad:true}});</script>
        """
        st.components.v1.html(mermaid_html, height=300)

        # Create downloadable docx
        doc = Document()
        doc.add_heading('AI Generated Requirements', level=1)
        doc.add_heading('Executive Summary', level=2)
        doc.add_paragraph(outputs.get('summary',''))
        doc.add_heading('Epics & User Stories', level=2)
        doc.add_paragraph(outputs.get('user_stories',''))
        doc.add_heading('Acceptance Criteria', level=2)
        doc.add_paragraph(outputs.get('acceptance_criteria',''))
        doc.add_heading('Test Cases', level=2)
        doc.add_paragraph(outputs.get('test_cases',''))
        doc.add_heading('Mermaid Flowchart', level=2)
        doc.add_paragraph(outputs.get('flows',''))

        # Save to bytes buffer instead of file
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        fname = f"requirements_{int(datetime.now().timestamp())}.docx"
        st.download_button(
            label="Download as Word (.docx)",
            data=buffer.getvalue(),
            file_name=fname,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )