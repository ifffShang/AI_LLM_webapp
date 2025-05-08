#timelinePage.py
import streamlit as st
st.set_page_config(page_title="Symbols", layout="centered", initial_sidebar_state="collapsed")
from utils.qa_chain import setup_chain  # or repeat the setup_chain code here
from utils.query_cache import get_cached_answer  # Import the caching utility
import re
from pages.pdfpage import view_pdf_with_navigation
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

def display_symbol_page(symbol_data):
    
    
    # First, build the list of tab names
    symbol_tabs = []
    
    for i in range(len(symbol_data)):
        symbol_tabs.append(symbol_data[i]["title"])
    if 'selected_tab' not in st.session_state:
        st.session_state.selected_tab = symbol_tabs[0]
    

    cols = st.columns(len(symbol_tabs))
    for i, tab in enumerate(symbol_tabs):
        with cols[i]:
            button_type = "primary" if tab == st.session_state.selected_tab else "secondary"
            if st.button(tab, key=f"tab_{i}", type=button_type, use_container_width=True):
                st.session_state.selected_tab = tab
                st.rerun()
    
    selected_symbol = None
    for symbol in symbol_data:
        if symbol["title"] == st.session_state.selected_tab:
            selected_symbol = symbol
            break

    if selected_symbol:
        for i in range(0, len(selected_symbol["bullet_points"]), 5):
            # Get up to five points for this cycle
            points = []
            for j in range(5):
                if i + j < len(selected_symbol["bullet_points"]):
                    point = selected_symbol["bullet_points"][i + j]
                    match = re.match(r'\*\*(.*?)\*\*(.*)', point)  # Fixed regex to include colon
                    if match:
                        points.append({
                            "title": match.group(1).strip(),
                            "detail": match.group(2).strip()
                        })
                    else:
                        # Handle case where the regex doesn't match
                        points.append({
                            "title": "Point " + str(i + j + 1),
                            "detail": point
                        })
                else:
                    points.append(None)  # Placeholder for missing points

            # First row: 30/70 split
            if points[0] is not None or points[1] is not None:
                row1 = st.container()
                with row1:
                    col1, col2 = st.columns([3, 7])
                    
                    if points[0] is not None:
                        with col1:
                            st.markdown(f"""
                            <div class="card-long">
                                <h3 style="color: #5e29e3; margin-bottom: 15px; word-wrap: break-word;">{points[0]['title']}</h3>
                                <p style="color: #555; flex-grow: 1; overflow-wrap: break-word;">{points[0]['detail']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if points[1] is not None:
                        with col2:
                            st.markdown(f"""
                            <div class="card">
                                <h3 style="color: #a98bf7; margin-bottom: 15px; word-wrap: break-word;">{points[1]['title']}</h3>
                                <p style="color: #555; flex-grow: 1; overflow-wrap: break-word;">{points[1]['detail']}</p>
                            </div>
                            """, unsafe_allow_html=True)
            
            # Second row: 70/30 split
            if points[2] is not None or points[3] is not None:
                row2 = st.container()
                with row2:
                    col1, col2 = st.columns([7, 3])
                    
                    if points[2] is not None:
                        with col1:
                            st.markdown(f"""
                            <div class="card">
                                <h3 style="color: #a98bf7; margin-bottom: 15px; word-wrap: break-word;">{points[2]['title']}</h3>
                                <p style="color: #555; flex-grow: 1; overflow-wrap: break-word;">{points[2]['detail']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if points[3] is not None:
                        with col2:
                            st.markdown(f"""
                            <div class="card-long">
                                <h3 style="color: #5e29e3; margin-bottom: 15px; word-wrap: break-word;">{points[3]['title']}</h3>
                                <p style="color: #555; flex-grow: 1; overflow-wrap: break-word;">{points[3]['detail']}</p>
                            </div>
                            """, unsafe_allow_html=True)
            
            # Third row: Full width
            if points[4] is not None:
                row3 = st.container()
                with row3:
                    st.markdown(f"""
                    <div class="card">
                        <h3 style="color: #a98bf7; margin-bottom: 15px; word-wrap: break-word;">{points[4]['title']}</h3>
                        <p style="color: #555; flex-grow: 1; overflow-wrap: break-word;">{points[4]['detail']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
    # Initialize the HTML string
    references_html = ""

    # Build HTML for reference cards
    for i in range(len(symbol_tabs)):
        references_html += f"""
        <div class="reference-card">
            <p class="reference-text">{symbol_tabs[i]}</p>
            <a href="pages/pdfpage.py" class="page-link">
            <span class="book-icon">📖</span> Go to page {i+1}
        </a>
        </div>
        """

    # Output the complete HTML structure
    st.markdown(f"""
    
        <h3 style="color: #5e29e3; text-align: center; margin-bottom: 15px; word-wrap: break-word;">Page References</h3>
        
        <div class="reference-cards">
            {references_html}
        </div>
    
    """, unsafe_allow_html=True)
                        
#html
    st.markdown("""
<style>
    /* Target buttons with this specific class */
    .st-emotion-cache-3urlvs {
        background-color: #7e57c2 !important;  /* Purple background */
        color: white !important;               /* White text */
        border: none !important;
        height: 50px !important;
    }
    
    /* For hover effects */
    .st-emotion-cache-3urlvs:hover {
        background-color: #6a4db3 !important;  /* Darker purple on hover */
    }
    div.stButton > button {
        height: 50px !important;      /* Fixed height */
        min-height: 50px !important;  /* Minimum height */
        white-space: normal !important; /* Allow text wrapping */
        display: flex !important;     /* Use flexbox for centering */
        align-items: center !important; /* Center content vertically */
        justify-content: center !important; /* Center content horizontally */
        line-height: 1.2 !important;  /* Adjust line height for better text display */
        padding: 10px 15px !important; /* Consistent padding */
        width: 100% !important;       /* Full width of container */
    },
    div.stButton > button[data-baseweb="button"][kind="primary"]:hover {
        background-color: #8c6fe4 !important; 
        border-color: #8c6fe4 !important;
    },
    div.stButton > button[data-baseweb="button"][kind="secondary"]:hover {
        background-color: #8c6fe4 !important;  
        border-color: #8c6fe4 !important;
    }
    .card {
         
        height: 500px; /* Fixed height for cards */
        min-height: 200px;
        max-height: 300px; /* Maximum height */
        display: flex; 
        flex-direction: column;
        background-color: white; 
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 20px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        overflow-y: auto; /* Add scrolling if content exceeds height */
    }
    .card-long {
        
        height: 500px; 
        min-height: 200px;
        max-height: 300px;
        display: flex; 
        flex-direction: column;
        background-color: #cabee8; 
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 20px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        overflow-y: auto; 
                }
    .reference-cards {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        flex-wrap: wrap;
    }
    
    .reference-card {
        flex: 1;
        width: 30%;
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        min-height: 100px;
        margin-bottom: 10px;
    }
    
    .reference-text {
        color: #555;
        margin-bottom: 15px;
        flex-grow: 1;
    }
    
    .page-button {
        background-color: white;
        color: #a98bf7;
        border: 1px solid #a98bf7;
        border-radius: 5px;
        padding: 8px 10px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        cursor: pointer;
        font-size: 14px;
    }
    
    .book-icon {
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

def display_references(symbol_data):
    st.markdown("## References")
    for symbol in symbol_data:
        st.markdown(f"### {symbol['title']}")
        for point in symbol['bullet_points']:
            st.markdown(f"- {point}")



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

# test= """
#     ### **Beginning**
# - **Overview:** The novel *The Great York Gatsby* by F. Scott Fitzgerald is rich with symbols that represent themes of the American Dream, wealth, and social class. Key symbols include the green light, the Valley of Ashes, and the eyes of Dr. T.J. Eckleburg.

# ### **Symbols in *The Great Gatsby***
# - **The Green Light:** Represents Gatsby's hopes and dreams, particularly his longing for Daisy. It is located at the end of Daisy's dock and is a constant reminder of his unattainable desire.
# - **The Valley of Ashes:** A desolate area between West Egg and New York City, symbolizing the moral and social decay hidden beneath the surface of the wealthy. It is where the working class lives, in stark contrast to the opulence of the Eggs.
# - **The Eyes of Dr. T.J. Eckleburg:** A billboard with the eyes of an optometrist, symbolizing the moral decay of society and the loss of spiritual values. They watch over the Valley of Ashes like a god.

# ### **Key Events in the Novel**
# - **Gatsby's Parties:** Lavish gatherings at Gatsby's mansion, symbolizing the excess and superficiality of the Roaring Twenties. They are designed to attract Daisy's attention.
# - **Gatsby's Reunion with Daisy:** The moment Gatsby and Daisy reconnect, symbolizing his attempt to recapture the past and his belief in the possibility of rewriting history.
# - **Myrtle's Death:** Myrtle is hit by Daisy driving Gatsby's car, symbolizing the destructive power of wealth and the carelessness of the upper class.
# - **Gatsby's Death:** Gatsby is shot by George Wilson, who believes Gatsby is responsible for Myrtle's death. His death symbolizes the end of the American Dream and the emptiness of material success.

# ### **Final Summary**
# - **Reflection:** Gatsby's life is a tragic pursuit of the American Dream, marked by wealth, love, and ultimately, disillusionment. His legacy is one of unfulfilled dreams and the hollowness of the upper class.
# - **Quote:** *"So we beat on, boats against the current, borne back ceaselessly into the past."* This quote encapsulates Gatsby's relentless pursuit of the past and the futility of his dreams.
#        """

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
        symbol_data =  process_text(result)
        print("----")
        print(symbol_data[1]["bullet_points"])
        display_symbol_page(symbol_data)
        


    
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
        
        # page_numbers = []
        # for doc in source_docs:
        #     page_num = doc.metadata.get('page', None)
        #     if page_num is not None:
        #         page_numbers.append(page_num)
        
        # print("Source document pages:", page_numbers)
        
    except Exception as e:
        st.error(f"⚠️ {str(e)}")