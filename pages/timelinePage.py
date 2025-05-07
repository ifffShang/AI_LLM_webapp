#timelinePage.py
import streamlit as st
st.set_page_config(page_title="Answer", layout="centered", initial_sidebar_state="collapsed")
from utils.qa_chain import setup_chain  # or repeat the setup_chain code here
from style.style import apply_custom_styles
apply_custom_styles()
from utils.query_cache import get_cached_answer  # Import the caching utility
import re
import urllib.parse # Keep this if you use it for PDF links or other URLs

def display_gatsby_profile():
    st.markdown("""
    <div style="background-color: white; border-radius: 12px; padding: 20px; margin-bottom: 30px; display: flex; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #e9e1ff; display: flex; justify-content: center; align-items: center; color: #7752e6; font-weight: bold; margin-right: 15px;">
            JG
        </div>
        <div>
            <h2 style="margin: 0; padding: 0; font-size: 18px; font-weight: 600;">Jay Gatsby</h2>
            <p style="margin: 5px 0 12px 0; font-size: 14px; color: #666;">
                Mysterious millionaire with a complicated past and an idealistic dream
            </p>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span style="background-color: #f4f4f8; color: #666; padding: 4px 10px; border-radius: 12px; font-size: 12px;">Ambitious</span>
                <span style="background-color: #f4f4f8; color: #666; padding: 4px 10px; border-radius: 12px; font-size: 12px;">Optimistic</span>
                <span style="background-color: #f4f4f8; color: #666; padding: 4px 10px; border-radius: 12px; font-size: 12px;">Romantic</span>
                <span style="background-color: #f4f4f8; color: #666; padding: 4px 10px; border-radius: 12px; font-size: 12px;">Deceptive</span>
                <span style="background-color: #f4f4f8; color: #666; padding: 4px 10px; border-radius: 12px; font-size: 12px;">Lonely</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
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
{query}

### **Beginning**
- **Overview:** [Brief summary of Gatsby's early background and character motivation]  

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
        process_timeline = process_timeline_text(result)
        display_gatsby_profile()
        display_text(process_timeline[0])
        display_vertical_timeline(process_timeline[1:-1])
        display_text(process_timeline[-1])
    # Parse the result into structured timeline events
#         result = """
#         ### **Early Life (Late 1890s - 1910s)**
# - **Birth:** Born as **James Gatz** in **North Dakota** to poor farmers.  
# - **Youth:** Works as a janitor and fisherman on Lake Superior.  
# - **Name Change (Age 17):** Rebrands himself as **Jay Gatsby** to escape his humble origins.  

# ### **Meeting Dan Cody (1910)**
# - **1910:** While working on Lake Superior, meets **Dan Cody**, a wealthy copper tycoon.  
# - **Employment:** Becomes Cody's personal assistant and travels with him for five years.  
# - **Inheritance (1915):** Cody dies, leaving Gatsby a small inheritance, which is later stolen by Cody's mistress.  

# ### **Military Service & Meeting Daisy (1917-1918)**
# - **1917:** Joins the **U.S. Army** during World War I.  
# - **1918 (Fall):** Stationed at **Camp Taylor, Louisville, Kentucky**, where he meets **Daisy Fay**.  
# - **Romance:** Falls in love with Daisy, who is from a wealthy family.  
# - **1919 (Spring):** Promised to Daisy but is sent to **Oxford** (post-war) before they can marry.  

# ### **Post-War & Rise to Wealth (1920-1922)**
# - **1920-1922:** After Daisy marries **Tom Buchanan**, Gatsby dedicates himself to becoming wealthy to win her back.  
# - **Bootlegging & Organized Crime:** Accumulates wealth through illegal activities.  
# - **1922:** Buys a mansion in **West Egg**, across the bay from Daisy's home in **East Egg**.  

# ### **Summer 1922 (Events in the Novel)**
# - **Parties:** Hosts extravagant parties hoping Daisy will appear.  
# - **Reunion with Daisy:** Reconnects with Daisy through **Nick Carraway**.  
# - **Affair:** Begins an affair with Daisy.  
# - **Death of Myrtle Wilson:** Daisy, driving Gatsby's car, hits Myrtle.  
# - **Gatsby's Death:** **George Wilson** kills Gatsby, thinking he was Myrtle's lover and killer.

# ### **Aftermath**
# - **Funeral:** Few attend, including Nick.  
# - **Legacy:** Gatsby's dream dies with him.  

# ### **Final Reflection**
# - Nick reflects on Gatsby's belief in the **green light** and ends with:  
# *"So we beat on, boats against the current, borne back ceaselessly into the past."*
#         """


            
    
        query = st.text_input("Ask a question about the book...", placeholder="Type here and press Enter")

        if st.button("Answer") and query:
            st.session_state["user_query"] = query
            # if "time" in query:
            st.switch_page("pages/timelinePage.py")
            # else:
            # st.switch_page("pages/answerPage.py")

        st.markdown("### 🧠 Answer")
        st.success(result)
        
        page_numbers = []
        for doc in source_docs:
            page_num = doc.metadata.get('page', None)
            if page_num is not None:
                page_numbers.append(page_num)
        
        # Print page numbers for debugging
        print("Source document pages:", page_numbers)
        
    except Exception as e:
        st.error(f"⚠️ {str(e)}")