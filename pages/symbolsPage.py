#timelinePage.py
import streamlit as st
st.set_page_config(page_title="Answer", layout="centered", initial_sidebar_state="collapsed")
from utils.qa_chain import setup_chain  # or repeat the setup_chain code here
from style.style import apply_custom_styles
apply_custom_styles()
from utils.query_cache import get_cached_answer  # Import the caching utility
import re
import urllib.parse # Keep this if you use it for PDF links or other URLs

def display_text(section_data):
    section_title = section_data.get('title', 'Beginning') 
    content_lines_list = section_data.get('content_lines', [])
    content_html_paragraph = ""

    if content_lines_list:
        html_formatted_content = "<br>".join(content_lines_list)
        content_html_paragraph = f"<p>{html_formatted_content}</p>"
    else:
        content_html_paragraph = "<p>No details provided for this section.</p>"
    begin_html = f"""
    <div class='card-section-middle' style='margin-top: 20px; margin-bottom: 30px;'>
        <h4>{section_title}</h4>
        {content_html_paragraph}
    </div>
    """
    st.markdown(begin_html, unsafe_allow_html=True)
def process_timeline_text(timeline_text):
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
    
        content_detail_lines = [line.strip() for line in lines if line.strip()] # Get non-empty, stripped lines
    
        if card_main_title: # Add section if it has a title
            processed_sections.append({
                "title": card_main_title,
                "content_lines": content_detail_lines 
            })
    
    if not processed_sections:
        st.warning("No timeline sections found in the expected format. The LLM output might not match the prompt's requested structure.")
        return
    return processed_sections
def display_vertical_timeline(processed_sections):
   
    # ---- HTML Generation ----
    html_parts = [
        "<div class='cards-container-timeline'>",
        "<div class='cards-line'>", # This div has the ::before pseudo-element for the vertical line
        "<h2 style='text-align: left; width:100%; padding-left:10px; margin-bottom:20px;'>Timeline</h2>",

    ]
    
    for idx, section_data in enumerate(processed_sections):
        section_html_content = ""
        current_card_title = section_data.get('title', 'Untitled Section')
        content_lines_list = section_data.get('content_lines', [])

        # Add title for the card
        section_html_content += f"<h4>{current_card_title}</h4>"
        
        # Add content, joining lines with <br> for HTML display
        if content_lines_list:
            html_formatted_content = "<br>".join(content_lines_list)
            section_html_content += f"<p>{html_formatted_content}</p>"
        else:
            section_html_content += "<p>No details provided for this section.</p>"


        pdf_page_num = idx + 1 

        pdf_link_html = f"""
        <div style="text-align: right; margin-top: 10px;">
            <a href="the-great-gatsby.pdf#page={pdf_page_num}" target="_blank" style="display: inline-block; background-color: #5d4ba1; color: white; 
                       padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 12px;">
                       📖 Ref Source {pdf_page_num}</a>
        </div>
        """
        section_html_content += pdf_link_html

        card_class = ''
        if idx % 2 == 0:  
            card_class = 'card-section-left'
        else:  
            card_class = 'card-section-right'
        
        html_parts.append(f"<div class='{card_class}'>{section_html_content}</div>")
    html_parts.append("</div></div>") # Close .cards-line and .cards-container-timeline
    final_html = "".join(html_parts)
    st.markdown(final_html, unsafe_allow_html=True)

    
      
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
        
        # timeline_query = "Create a detailed timeline of Jay Gatsby's life with key events in chronological order"
            result, source_docs, from_cache = get_cached_answer(prompt, qa_chain)

        print(result)

#---------html layout---------
        # process_timeline = process_timeline_text(result)
        # display_text(process_timeline[0])
        # display_vertical_timeline(process_timeline[1:-1])
        # display_text(process_timeline[-1])
              
    
        query = st.text_input("Ask a question about the book...", placeholder="Type here and press Enter")

        if st.button("Answer") and query:
            st.session_state["user_query"] = query
            # if "time" in query:
            # st.switch_page("pages/timelinePage.py")
            # else:
            # st.switch_page("pages/answerPage.py")
            st.switch_page("pages/symbolsPage.py")

        st.markdown("### 🧠 Answer")
        st.success(result)
        
        # page_numbers = []
        # for doc in source_docs:
        #     page_num = doc.metadata.get('page', None)
        #     if page_num is not None:
        #         page_numbers.append(page_num)
        
        # print("Source document pages:", page_numbers)
        
    except Exception as e:
        st.error(f"⚠️ {str(e)}")