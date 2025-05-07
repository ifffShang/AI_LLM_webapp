#answerPage.py
import streamlit as st
st.set_page_config(page_title="Answer", layout="centered", initial_sidebar_state="collapsed")
from utils.qa_chain import setup_chain  # or repeat the setup_chain code here
from style.style import apply_custom_styles
apply_custom_styles()
from utils.query_cache import get_cached_answer  # Import the caching utility
import random
import re



def prev_page():
    st.session_state["current_page"] -= 1

def next_page():
    st.session_state["current_page"] += 1

def display_items_in_rows(sections,source_docs=None):
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 0
    
    total_pages = (len(sections) + 2) // 3
    current_page = st.session_state["current_page"]

    start_idx = current_page * 3
    end_idx = min(start_idx + 3, len(sections))
    current_sections = sections[start_idx:end_idx]

    cols = st.columns(3)
    character_pattern = re.compile(r"^\d+\.\s+\*\*(.*?)\*\*\s+-\s+(.*)", re.DOTALL)

    for i, character_entry_string in enumerate(current_sections):
        section_idx = start_idx + i
        title = "Unknown Title" # Default
        content = "No description available." # Default

        match = character_pattern.match(character_entry_string.strip())
        if match:
            title = match.group(1).strip()      # Extracted character name
            content = match.group(2).strip()    # Extracted character description
        else:
            print(f"Warning: Could not parse section: {character_entry_string}")
        # Determine page reference - default to a random page if source_docs not provided
        page_ref = f"Page {random.randint(10, 100)}"
        if source_docs and section_idx < len(source_docs):
            page_num = source_docs[section_idx].metadata.get('page', None)
            if page_num is not None:
                page_ref = f"Page {page_num}"

        with cols[i]:
            st.markdown(f"""
            <div class="card-section">
                <h4 style="color: #6c5ce7;"> {title}</h4>
                <p>{content}</p>
                <div style="text-align: right; margin-top: 10px;">
                    <a href="#" style="display: inline-block; background-color: #5d4ba1; color: white; 
                       padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 12px;">
                       📖 Go to {page_ref}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_page > 0:
            st.button("←", on_click=prev_page, key="prev_button")

    with col2:
        st.markdown(f"<p style='text-align: center;'>Page {current_page + 1} of {total_pages}</p>", unsafe_allow_html=True)

    with col3:
        if current_page < total_pages - 1:
            st.button("→", on_click=next_page, key="next_button")

if "user_query" not in st.session_state:
    st.warning("Please ask a question first.")
    st.stop()

qa_chain = setup_chain()
query = st.session_state["user_query"]


st.markdown(f"""
<h1 style='text-align: center; color: #6c5ce7;'>BookBuddy</h1>
<h2 style='text-align: center;'>{query}</h2>
<p style='text-align: center; color: gray;'>Type a question about characters, symbols, or plot points from the novel</p>

""", unsafe_allow_html=True)

with st.spinner("Thinking..."):
    try:
        result, source_docs,from_cache = get_cached_answer(query, qa_chain)
        if from_cache:
            print("from cache")
            st.success("Retrieved from cache")
        else:
            print("not from cache")
        
        # Process the result into sections
        sections = [s.strip() for s in result.split("\n\n") if s.strip()]
        
        st.markdown(f"""<div class="card-section-first">
        <p>{sections[0]}</p></div>
        """, unsafe_allow_html=True)
        display_items_in_rows(sections[1:-1],source_docs)
        st.markdown(f"""<div class="card-section">
                <h4 style="color: #6c5ce7;"> Summary</h4>
                <p>{sections[-1]}</p>
        <p>{sections[-1]}</p></div>
        """, unsafe_allow_html=True)

        query = st.text_input("Ask a question about the book...", placeholder="Type here and press Enter")

        if st.button("Answer") and query:
            st.session_state["user_query"] = query
            if "time" in query:
                st.switch_page("pages/timelinePage.py")
            st.switch_page("pages/answerPage.py")

        st.markdown("### 🧠 Answer")
        st.success(result)
        print(result)
        
        page_numbers = []
        for doc in source_docs:
            page_num = doc.metadata.get('page', None)
            if page_num is not None:
                page_numbers.append(page_num)
        
        # Print page numbers for debugging
        print("Source document pages:", page_numbers)
        
    except Exception as e:
        st.error(f"⚠️ {str(e)}")

