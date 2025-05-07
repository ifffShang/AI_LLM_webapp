import streamlit as st
def apply_custom_styles():
    st.markdown("""
<style>

body {
    background-color: #f0f2f6;
}
header, .st-emotion-cache-18ni7ap, .st-emotion-cache-1dp5vir {
    background: linear-gradient(90deg, #8e44ad, #6c5ce7);
    color: white;
}
.stButton > button {
    background-color: #8e44ad;
    color: white;
    border-radius: 8px;
    padding: 0.75em 1.5em;
    font-weight: 600;
}

.question-btn {
    background-color: white;
    border: 2px solid #8e44ad;
    border-radius: 12px;
    padding: 1em;
    font-weight: bold;
    margin: 0.5em;
    text-align: center;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
.question-btn:hover {
    background-color: #eee;
    cursor: pointer;
}
.cards-container {
    border: 2px solid #7e57c2;
    display: flex;
    flex-wrap: wrap;
    gap: 50px;
    padding: 50px;
    border-radius: 12px;
    margin_top: 10px;
    backgrounf-color: #7e57c2


}


.card-section {
    margin-bottom: 30px;
    background-color: white;
    border: 3px solid #d9c3f0;  /* Light purple border */
    border-radius: 12px;
    padding: 20px;
    box-shadow: 2px 4px 10px rgba(108, 92, 231, 0.1);
}
.card-section-first {
    color: #6c5ce7;
    font-weight: bold;
    font-size: 1.5em;
    margin-bottom: 30px;
    background-color: white;
    border: 3px solid #d9c3f0;  /* Light purple border */
    border-radius: 12px;
    padding: 20px;
    box-shadow: 2px 4px 10px rgba(108, 92, 231, 0.1);
}
.cards-container-timeline {
    width: 100%;
    background-color: white;
    border: 3px solid #d9c3f0;  /* Light purple border */
    border-radius: 12px;
    padding: 10px;
    box-shadow: 2px 4px 10px rgba(108, 92, 231, 0.1);
}

    .cards-line {
    position: relative; 
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    margin-top: 50px; 
    padding: 20px; 
}

.cards-line::before {
    content: '';
    position: absolute;
    top: 150px; /* Start from the top of cards-line padding */
    bottom: 50px; /* Extend to the bottom of cards-line padding */
    width: 8px; /* Line thickness */
    background-color: #6c5ce7; /* Purple color */
    z-index: 0; /* Ensure line is behind card content if they overlap */
}

    .card-section:hover,
    .card-section-middle:hover,
    .card-section-right:hover,
    .card-section-left:hover {
        box-shadow: 4px 6px 15px rgba(0,0,0,0.1);
    }

    .card-section h4,
    .card-section-middle h4,
    .card-section-right h4,
    .card-section-left h4 {
        margin: 0 0 0.5em 0;
        color: #6c5ce7;
        font-weight: 700;
    }

    .card-section p,
    .card-section-right p,
    .card-section-left p {
        margin: 0;
        color: #333;
        font-size: 0.95rem;
        line-height: 1.5;
    }
.card-section-left {
    position: relative;
    width: 50%;
    margin-left: 0;  
    margin-right: auto;
    background-color: white;
    border: 5px solid #d9c3f0;  /* Light purple border */
    border-radius: 12px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 2px 4px 10px rgba(108, 92, 231, 0.1);
}
.card-section-left::after {
    content: '';
    position: absolute;
    top: 80px; /* Adjust vertically as needed */
    right: 20px; /* Positions the circle just outside the right edge */
    width: 16px;
    height: 16px;
    background-color: #7e57c2; /* Purple color */
    border-radius: 50%;
    border: 3px solid white;
    box-shadow: 0 0 0 2px #7e57c2; /* Outer purple ring */
    z-index: 2;
}

    .card-section-right {
    position:relative;
    width: 50%;
    margin-left: auto;  /* pushes to right */
    margin-right: 0;
    background-color: white;
    border: 5px solid #d9c3f0;  /* Light purple border */
    border-radius: 12px;
    margin-top:20px;
    padding: 20px;
    box-shadow: 2px 4px 10px rgba(108, 92, 231, 0.1);
}
.card-section-right::after {
    content: '';
    position: absolute;
    top: 80px; /* Adjust vertically as needed */
    left: 20px; /* Positions the circle just outside the right edge */
    width: 16px;
    height: 16px;
    background-color: #7e57c2; /* Purple color */
    border-radius: 50%;
    border: 3px solid white;
    box-shadow: 0 0 0 2px #7e57c2; /* Outer purple ring */
    z-index: 2;
}   
.card-section-middle {
    position: relative;
    background-color: white;
    border: 5px solid #d9c3f0;  /* Light purple border */
    border-radius: 12px;
    padding: 20px;
    margin-top: 50px;
    box-shadow: 2px 4px 10px rgba(108, 92, 231, 0.1);
    background-color: #f0f2f6;
}
    
</style>
""", unsafe_allow_html=True)