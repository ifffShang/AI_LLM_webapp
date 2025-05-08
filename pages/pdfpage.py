import streamlit as st
import base64
import os

def view_pdf_with_navigation(pdf_path, idx):
    """
    Display a PDF with page navigation
    """
    # Check if file exists
    if not os.path.exists(pdf_path):
        st.error(f"PDF file not found: {pdf_path}")
        return False
    
    # Read the PDF file
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Create the PDF viewer HTML
    pdf_display = f"""
    <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="margin-bottom: 10px;">
        </div>
        <iframe id="pdf-iframe" src="data:application/pdf;base64,{base64_pdf}#page={idx}" width=200% height=900px type="application/pdf">
        </iframe>
    </div>
    
    <script>
    function changePage(offset) {{
        var iframe = document.getElementById('pdf-iframe');
        var currentHash = iframe.contentWindow.location.hash;
        var currentPage = 1;
        
        if (currentHash) {{
            var match = currentHash.match(/page=(\d+)/);
            if (match) {{
                currentPage = parseInt(match[1]) + offset;
                currentPage = Math.max(1, currentPage);  // Ensure page isn't less than 1
            }}
        }} else {{
            currentPage = 1 + offset;
        }}
        
        document.getElementById('current-page').textContent = 'Page: ' + currentPage;
        iframe.contentWindow.location.hash = 'page=' + currentPage;
    }}
    </script>
    """
    
    # Display the PDF
    st.markdown(pdf_display, unsafe_allow_html=True)
    return True

# Main page with reference cards
def main():
    st.title("The Great Gatsby - Study Guide")
    
    # Custom CSS for the reference cards
    st.markdown("""
    <style>
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Reference card content
    cards = [
        {"title": "Beginning", "page": 1},
        {"title": "Symbols in *The Great Gatsby*", "page": 2},
        {"title": "Key Events in the Novel", "page": 3},
        {"title": "Final Summary", "page": 4}
    ]
    
    # Initialize session state to store the current PDF and page
    if 'show_pdf' not in st.session_state:
        st.session_state.show_pdf = False
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    
    # Create two sections - one for reference cards, one for PDF
    if not st.session_state.show_pdf:
        # Show reference cards
        cols = st.columns(len(cards))
        
        for i, card in enumerate(cards):
            with cols[i]:
                # Create card as a button
                if st.button(card["title"], key=f"card_{i}", use_container_width=True):
                    st.session_state.current_page = card["page"]
                    st.session_state.show_pdf = True
                    st.rerun()
                
                # Add book icon and page link text below button
                st.markdown(f"📖 Page {card['page']}")
    else:
        # Show PDF viewer with back button
        if st.button("← Back to Reference Cards"):
            st.session_state.show_pdf = False
            st.rerun()
        
        # Display the page number
        st.write(f"**Viewing Page {st.session_state.current_page}**")
        
        # View the PDF
        pdf_path = "static/the-great-gatsby.pdf"
        view_pdf_with_navigation(pdf_path, idx=st.session_state.current_page)


    
    # Custom CSS to match the design in the image
    st.markdown("""
    <style>
    .card-container {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 25px;
    }
    .reference-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        width: 100%;
        min-height: 150px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 500;
        color: #343a40;
        margin-bottom: 20px;
    }
    .page-link {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        color: #0d6efd;
        text-decoration: none;
        font-weight: 500;
    }
    .book-icon {
        font-size: 1.25rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Reference card content matching the image
    cards = [
        {"title": "Beginning", "page": 1},
        {"title": "Symbols in *The Great Gatsby*", "page": 2},
        {"title": "Key Events in the Novel", "page": 3},
        {"title": "Final Summary", "page": 4}
    ]
    
    # Create columns for the cards
    cols = st.columns(len(cards))
    
    # Generate HTML for the cards
    for i, card in enumerate(cards):
        with cols[i]:
            st.markdown(f"""
            <div class="reference-card">
                <div class="card-title">{card["title"]}</div>
                <a href="pages/pdfpage?page={card["page"]}" class="page-link">
                    <span class="book-icon">📖</span> Go to page {card["page"]}
                </a>
            </div>
            """, unsafe_allow_html=True)

# PDF viewer page
def pdf_page():
    # Get the page parameter from query parameters
    query_params = st.query_params
    page = int(query_params.get("page", 1))
    
    # Back button
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <a href="/" style="display: inline-flex; align-items: center; gap: 8px; 
                          text-decoration: none; color: #0d6efd; font-weight: 500;">
            ← Back to Reference Cards
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Path to your PDF file
    pdf_path = "static/the-great-gatsby.pdf"
    
    # View the PDF at the specified page
    if not view_pdf_with_navigation(pdf_path, page=page):
        st.error(f"Failed to load PDF. Please check if '{pdf_path}' exists.")

# For deployment in a Streamlit multi-page app
if __name__ == "__main__":
    # Toggle between these for testing
    main()  # For reference cards page
    # pdf_page()  # For PDF viewer page