import streamlit as st
import os
import tempfile
import time
import json
from pathlib import Path
from modules.pipeline import MedicalReportPipeline

# Page configuration
st.set_page_config(
    page_title="Medical Report Bot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .report-section {
        background-color: #000000;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: white;
    }
    .answer-box {
        background-color: #000000;
        padding: 15px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
        color: white;
    }
    .error-box {
        background-color: #000000;
        padding: 15px;
        border-left: 4px solid #d32f2f;
        margin: 10px 0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = MedicalReportPipeline()

if 'report_loaded' not in st.session_state:
    st.session_state.report_loaded = False

if 'current_summary' not in st.session_state:
    st.session_state.current_summary = ""

# Title and description
st.markdown('<h1 class="main-header">🏥 Medical Report Summarizer & Q&A Bot</h1>', unsafe_allow_html=True)

st.markdown("""
This app helps you understand medical reports in plain English. 
**Upload a PDF or image of your medical report**, and:
- Get a plain-English summary
- Ask follow-up questions
- Understand medical terminology
""")

# Sidebar
with st.sidebar:
    st.header("📋 Document Upload")
    
    uploaded_file = st.file_uploader(
        "Upload your medical report",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="PDF (text or scanned) or image format"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        
        # Process button
        if st.button("📖 Process Document", key="process_btn", use_container_width=True):
            with st.spinner("Processing your document..."):
                # Simulate progress for ~3 seconds
                for i in range(5):
                    time.sleep(0.6)
                    st.progress((i+1)*20)
                text, summary, error = st.session_state.pipeline.process_document(tmp_path)
            
            if error:
                st.error(f"Error: {error}")
            else:
                st.session_state.report_loaded = True
                st.session_state.current_summary = summary
                st.success("✅ Document processed successfully!")
        
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass
    
    st.divider()
    
    # Session info
    if st.session_state.report_loaded:
        st.subheader("📊 Session Info")
        history = st.session_state.pipeline.get_conversation_history()
        st.metric("Questions Asked", len(history))
        
        # Clear session button
        if st.button("🗑️ Clear Session", key="clear_btn", use_container_width=True):
            st.session_state.pipeline.clear_session()
            st.session_state.report_loaded = False
            st.session_state.current_summary = ""
            st.rerun()
    
    st.divider()
    st.markdown("""
    ### How to use:
    1. Upload a medical PDF or image
    2. Click "Process Document"
    3. Read the summary
    4. Ask questions below
    
    ### Note:
    This tool explains what your report says—it's not medical advice. 
    Always consult your doctor for medical decisions.
    """)

# Main content
if st.session_state.report_loaded:
    # Summary section
    st.header("📄 Report Summary")
    st.markdown(
        f'<div class="report-section">{st.session_state.current_summary.replace("\n", "<br>")}</div>', 
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Q&A section
    st.header("❓ Ask Questions")
    st.markdown("Ask follow-up questions about your report. The AI will answer based on the information provided.")
    
    # ✅ Chat interface aligned properly
    with st.form(key="qa_form"):
        cols = st.columns([5, 1])  # wider input, narrower button
        with cols[0]:
            user_question = st.text_input(
                "Your question:",
                placeholder="e.g., Is my hemoglobin level normal for my age?",
                label_visibility="collapsed"
            )
        with cols[1]:
            send_button = st.form_submit_button("Send")

    if send_button and user_question.strip():
        with st.spinner("Generating answer..."):
            answer = st.session_state.pipeline.ask_question(user_question)
        
        st.markdown(
            f'<div class="answer-box"><strong>Q:</strong> {user_question}<br><br><strong>A:</strong> {answer}</div>', 
            unsafe_allow_html=True
        )
    
    # Conversation history
    st.subheader("📝 Conversation History")
    history = st.session_state.pipeline.get_conversation_history()
    
    if history:
        for idx, turn in enumerate(history, 1):
            with st.expander(f"Turn {idx}: {turn['question'][:50]}..."):
                st.markdown(f"**Q:** {turn['question']}")
                st.markdown(f"**A:** {turn['answer']}")
        
        # Download conversation
        st.markdown("---")
        if st.button("💾 Download Conversation"):
            conversation_data = {
                "summary": st.session_state.current_summary,
                "q_and_a": history
            }
            json_str = json.dumps(conversation_data, indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_str,
                file_name="medical_report_qa.json",
                mime="application/json"
            )
    else:
        st.info("No questions asked yet. Start by asking a question above!")

else:
    st.info("👈 Please upload a medical report to get started!")
    st.markdown("""
    ### Example Questions You Can Ask:
    - Is my [test name] result normal?
    - What does [abbreviation] mean?
    - What do these numbers tell me?
    - Should I be concerned about this result?
    - What's the difference between my result and the normal range?
    """)

# Footer
st.divider()
st.markdown("""
<small>
**Disclaimer:** This tool is for educational purposes only. It helps explain what your medical report says, 
but it is NOT a substitute for medical advice from a qualified healthcare professional. 
Always consult your doctor with questions about your health.
</small>
""", unsafe_allow_html=True)
