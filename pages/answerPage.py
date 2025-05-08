#answerPage.py
import streamlit as st
st.set_page_config(page_title="Answer", layout="centered", initial_sidebar_state="collapsed")
from utils.qa_chain import setup_chain  # or repeat the setup_chain code here
from style.style import apply_custom_styles
apply_custom_styles()
from utils.query_cache import get_cached_answer  # Import the caching utility
import random
import re

def process_text(timeline_text):
    processed_sections = [] # To hold {"title": "Main Section Title", "content_lines": ["- **Bullet...**", ...]}

    raw_major_sections = re.split(r'\n?(?=### \*\*)', timeline_text.strip())

    for section_block_raw in raw_major_sections:
        section_block = section_block_raw.strip()
        if not section_block:  # Skip empty parts from split
            continue

        lines = section_block.split('\n')
        first_line = lines.pop(0).strip() # This should be the "### **Title**" line

        # Extract title from "### **Title**"
        title_match = re.match(r"^### \*\*(.*?)\*\*", first_line)
        if not title_match:
            continue
    
        card_main_title = title_match.group(1).strip()
   
        bullet_points = []
        for line in section_block.split('\n'):
            if line.strip().startswith('- '):
                bullet_points.append(line.strip()[2:])
        
        processed_sections.append({
            "title": card_main_title,
            "bullet_points": bullet_points
        })   

    return processed_sections

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


        # Determine page reference - default to a random page if source_docs not provided
        page_ref = f"Page {random.randint(10, 100)}"
        if source_docs and section_idx < len(source_docs):
            page_num = source_docs[section_idx].metadata.get('page', None)
            if page_num is not None:
                page_ref = f"Page {page_num}"

        with cols[i]:
            st.markdown(f"""
            <div class="card-section">
                <h4 style="color: #6c5ce7;"> {character_entry_string['title']}</h4>
                <p>{character_entry_string['bullet_points']}</p>
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
prompt = f"""
The user is asking about: "{query}"
Based on this, create a detailed timeline with key events in chronological order.
You MUST strictly follow the exact output format provided below. Do not add any introductory or concluding text outside of this format.
Every part of your response must conform to this structure.

### **Beginning**
- **Overview:** [Details]  

### **[Main Section Title]**
- **[Bullet Title]:** [Details]  
- **[Bullet Title]:** [Details]  

### **[Next Section Title]**
- **[Bullet Title]:** [Details]  
- **[Bullet Title]:** [Details]  

### **Final Summary**
- **Reflection:** [Summarize Gatsby's life arc and legacy]  
- **Quote:** *"[Meaningful quote from the novel]*"  
"""

st.markdown(f"""
<h1 style='text-align: center; color: #6c5ce7;'>BookBuddy</h1>
<h2 style='text-align: center;'>{query}</h2>
<p style='text-align: center; color: gray;'>Type a question about characters, symbols, or plot points from the novel</p>

""", unsafe_allow_html=True)

with st.spinner("Thinking..."):
    try:
        result, source_docs,from_cache = get_cached_answer(prompt, qa_chain)
        if from_cache:
            print("from cache")
            st.success("Retrieved from cache")
        else:
            print("not from cache")
        
        # Process the result into sections
        
        answer_data = process_text(result)
        st.markdown(f"""<div class="card-section-first">
                <h4 style="color: #6c5ce7;">{answer_data[0]['title']}</h4>
                <p>{answer_data[0]['bullet_points']}</p>
        """, unsafe_allow_html=True)
        display_items_in_rows(answer_data[1:-1],source_docs)
        st.markdown(f"""<div class="card-section">
                <h4 style="color: #6c5ce7;">{answer_data[-1]['title']}</h4>
                <p>{answer_data[-1]['bullet_points']}</p>
            </div>
        """, unsafe_allow_html=True)

        query = st.text_input("Ask a question about the book...", placeholder="Type here and press Enter")

        if st.button("Answer") and query:
            st.session_state["user_query"] = query
            if "life and experiences" in query:
                st.switch_page("pages/timelinePage.py")
            elif "character" in query:
                st.switch_page("pages/answerPage.py")
            else:
                st.switch_page("pages/symbolsPage.py")

        # st.markdown("### 🧠 Answer")
        # st.success(result)
        # print(result)
        
        page_numbers = []
        for doc in source_docs:
            page_num = doc.metadata.get('page', None)
            if page_num is not None:
                page_numbers.append(page_num)
        
        # Print page numbers for debugging
        print("Source document pages:", page_numbers)
        
    except Exception as e:
        st.error(f"⚠️ {str(e)}")

