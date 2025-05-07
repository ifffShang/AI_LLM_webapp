#timelinePage.py
import streamlit as st
st.set_page_config(page_title="Answer", layout="centered", initial_sidebar_state="collapsed")
from utils.qa_chain import setup_chain  # or repeat the setup_chain code here
from style.style import apply_custom_styles
apply_custom_styles()
from utils.query_cache import get_cached_answer  # Import the caching utility
import re

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

import re
import streamlit as st

def display_vertical_timeline(timeline_text):
    # Regex to find sections: captures title and content block
    pattern = r'### \*\*(.*?)\*\*(.*?)(?=### \*\*|$)'
    matches = re.findall(pattern, timeline_text, re.DOTALL)

    processed_sections = []
    for title, content_block in matches:
        cleaned_title = title.strip()
        points = []
        # Process the content block for bullet points
        for line in content_block.strip().split('\n'):
            stripped_line = line.strip()
            if stripped_line.startswith('-'):
                point = stripped_line[1:].strip()
                points.append(point)
        
        if cleaned_title or points: # Keep section if it has a title or points
            processed_sections.append({"title": cleaned_title, "points": points})
    
    # Guarding the debug print statement
    if processed_sections:
        print(processed_sections[0])     

    html_parts = ["<div class='cards-container-timeline'><div class='cards-line'><h2 style='text-align: center; color: #6c5ce7;'>Gatsby's Timeline</h2>"]
    for idx, section_data in enumerate(processed_sections):
        section_html_content = ""
        current_title = section_data.get('title', '') 

        # Only display the <h4> title if the title string exists and contains numbers
        if current_title:
            title_has_numbers = any(char.isdigit() for char in current_title)
            if title_has_numbers:
                section_html_content += f"<h4>{current_title}</h4>"
            # If title does not have numbers, the <h4> tag for the title is skipped.
        
        if section_data.get('points'): # Check if 'points' key exists and has items
            section_html_content += "<ul>"
            for point in section_data['points']:
                section_html_content += f"<li>{point}</li>"
            section_html_content += "</ul>"

        # Add the card to HTML parts only if there's actual content generated for it
        if section_html_content.strip(): 
            if idx % 2 == 0:
                html_parts.append(f"<div class='card-section-left'>{section_html_content}</div>")
            else:
                html_parts.append(f"<div class='card-section-right'>{section_html_content}</div>")
            
    html_parts.append("</div></div>")
    final_html = "".join(html_parts)
    st.markdown(final_html, unsafe_allow_html=True)   

    



# Main page content
st.markdown("""
<h1 style='text-align: center; color: #6c5ce7;'>Gatsby's Timeline</h1>
<p style='text-align: center; color: gray;'>Key events in Jay Gatsby's life from "The Great Gatsby"</p>
""", unsafe_allow_html=True)
        
    
if "user_query" not in st.session_state:
    st.warning("Please ask a question first.")
    st.stop()

qa_chain = setup_chain()
query = st.session_state["user_query"]
prompt = f"""
{query}

Please respond in the following exact format:

### **[Section Title]**
- **[Bullet Title]:** [Details]  
- **[Bullet Title]:** [Details]  

### **[Another Section]**
- **[Bullet Title]:** [Details]  
...
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
        display_gatsby_profile()
        print(result)
        
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
        display_vertical_timeline(result)

            
    
        query = st.text_input("Ask a question about the book...", placeholder="Type here and press Enter")

        if st.button("Answer") and query:
            st.session_state["user_query"] = query
            if "time" in query:
                st.switch_page("pages/timelinePage.py")
            else:
                st.switch_page("pages/answerPage.py")

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

def parse_structured_timeline(timeline_text):
    """
    Parses a timeline text with main headings, numbered items, and sub-bullets.
    Returns a list of dictionaries, each representing a part of the timeline.
    """
    parsed_data = []
    current_item_sub_points = None # To hold sub-points for the current numbered item

    for line in timeline_text.strip().split('\n'):
        line = line.rstrip() # Keep leading spaces for sub-bullets, remove trailing

        # Try to match main heading (e.g., ### **Title**)
        main_heading_match = re.match(r"^### \*\*(.*?)\*\*\s*$", line)
        if main_heading_match:
            if current_item_sub_points is not None: # Finalize previous item if any
                current_item_sub_points = None
            parsed_data.append({
                "type": "main_heading",
                "title": main_heading_match.group(1).strip()
            })
            continue

        # Try to match numbered item (e.g., 1. **Title** – Description)
        # Using a more flexible separator (– or -)
        item_match = re.match(r"^(\d+\.)\s+\*\*(.*?)\*\*\s*[–-]\s*(.*)$", line)
        if item_match:
            if current_item_sub_points is not None: # Finalize previous item
                 current_item_sub_points = None
            item_data = {
                "type": "item",
                "number": item_match.group(1).strip(),
                "title": item_match.group(2).strip(),
                "description": item_match.group(3).strip(),
                "sub_points": []
            }
            parsed_data.append(item_data)
            current_item_sub_points = item_data["sub_points"] # Store ref to add sub-points
            continue

        # Try to match sub-bullet (e.g., - Sub-point text)
        sub_point_match = re.match(r"^\s*-\s+(.*)$", line)
        if sub_point_match and current_item_sub_points is not None:
            current_item_sub_points.append(sub_point_match.group(1).strip())
            continue


    return parsed_data

