#home.py
import streamlit as st
st.set_page_config(page_title="BookBuddy - Gatsby Q&A", layout="centered", initial_sidebar_state="collapsed")
from style.style import apply_custom_styles
apply_custom_styles()
from utils.query_cache import get_cached_answer, clear_cache

st.markdown("""
<h1 style='text-align: center; color: #6c5ce7;'>BookBuddy</h1>
<h2 style='text-align: center;'>Ask me about "The Great Gatsby"</h2>
<p style='text-align: center; color: gray;'>Type a question about characters, symbols, or plot points from the novel</p>
<div style='display: flex; justify-content: center;'>
    <div class='question-btn'>Try asking about:<br><em>"Tell me about Gatsby's life and experiences"</em></div>
    <div class='question-btn'>Try asking about:<br><em>"Tell me about the women characters in the book"</em></div>
    <div class='question-btn'>Try asking about:<br><em>"What are the major symbols in The Great Gatsby?"</em></div>
</div>
            
""", unsafe_allow_html=True)

query = st.text_input("Ask a question about the book...", placeholder="Type here and press Enter")

if st.button("Answer") and query:
    st.session_state["user_query"] = query
    if "time" in query:
        st.switch_page("pages/timelinePage.py")
    else:
        st.switch_page("pages/answerPage.py")


    


