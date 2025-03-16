import streamlit as st
import requests
import pickle 
import pandas as pd
import lzma
import urllib.parse
from datetime import datetime
import numpy as np

# Define mood categories and their associated genres
MOODS = {
    "Happy 😊": {
        "genres": ["Comedy", "Animation", "Family"],
        "description": "Light-hearted, fun movies to boost your mood",
        "min_rating": 6.5,
        "years": (1990, datetime.now().year)
    },
    "Thoughtful 🤔": {
        "genres": ["Drama", "Documentary", "History"],
        "description": "Thought-provoking films that make you reflect",
        "min_rating": 7.0,
        "years": (1970, datetime.now().year)
    },
    "Excited 🎬": {
        "genres": ["Action", "Adventure", "Science Fiction"],
        "description": "High-energy, thrilling entertainment",
        "min_rating": 6.5,
        "years": (1990, datetime.now().year)
    },
    "Romantic 💕": {
        "genres": ["Romance", "Drama"],
        "description": "Love stories that warm your heart",
        "min_rating": 6.5,
        "years": (1980, datetime.now().year)
    },
    "Thrilled 😱": {
        "genres": ["Horror", "Thriller", "Mystery"],
        "description": "Suspenseful films that keep you on the edge",
        "min_rating": 6.0,
        "years": (1980, datetime.now().year)
    },
    "Relaxed 😌": {
        "genres": ["Music", "Documentary", "Family"],
        "description": "Calm, easy-watching content",
        "min_rating": 6.5,
        "years": (1990, datetime.now().year)
    }
}

# Configure the page
st.set_page_config(
    page_title="Movizz - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add this after the page config
st.markdown("""
<style>
/* Modern color scheme */
:root {
    --primary-color: #6366F1;  /* Modern indigo */
    --secondary-color: #10B981;  /* Emerald green */
    --background-color: #F3F4F6;  /* Light gray */
    --text-color: #1F2937;  /* Dark gray */
    --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --hover-color: #4F46E5;  /* Darker indigo for hover */
    --accent-color: #EC4899;  /* Pink for accents */
    --success-color: #059669;  /* Green for success messages */
    --warning-color: #F59E0B;  /* Amber for warnings */
    --error-color: #EF4444;  /* Red for errors */
}

/* General styling */
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

/* Movie card styling */
.movie-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: var(--card-shadow);
    height: 100%;
    border: 1px solid rgba(99, 102, 241, 0.1);
}

.movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.movie-poster {
    position: relative;
    overflow: hidden;
}

.movie-poster img {
    width: 100%;
    border-radius: 15px 15px 0 0;
}

.movie-info {
    padding: 1rem;
}

.movie-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0.5rem 0;
    text-align: center;
}

/* Rating badge */
.rating-badge {
    background: var(--primary-color);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
}

/* Buttons */
.stButton button {
    background: var(--primary-color) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 500 !important;
    border: none !important;
    transition: all 0.3s ease !important;
}

.stButton button:hover {
    background: var(--hover-color) !important;
    transform: translateY(-2px);
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background: linear-gradient(180deg, var(--primary-color), var(--hover-color));
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: white !important;
    border-radius: 10px !important;
}

/* Movie details view */
.movie-details-large {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: var(--card-shadow);
}

.genre-tag {
    background: #e9ecef;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    margin: 0.2rem;
    display: inline-block;
    font-size: 0.9rem;
}

/* Custom header */
.app-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, var(--primary-color), var(--hover-color));
    color: white;
    border-radius: 0 0 20px 20px;
    margin-bottom: 2rem;
    box-shadow: var(--card-shadow);
}

/* Search bar */
.search-container {
    background: white;
    padding: 1rem;
    border-radius: 15px;
    box-shadow: var(--card-shadow);
    margin: 1rem 0;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
    background: white;
    border-radius: 15px 15px 0 0;
}

/* Select box styling */
.stSelectbox > div > div {
    background-color: var(--card-bg);
    border-radius: 12px;
    border: 1px solid rgba(108,99,255,0.2);
    color: var(--text-color) !important;  /* Make text visible */
}

/* Style for the selected option */
.stSelectbox [data-baseweb="select"] span {
    color: var(--text-color) !important;
    font-weight: 500;
}

/* Style for the dropdown options */
div[data-baseweb="select"] ul {
    background-color: white;
    color: var(--text-color);
}

div[data-baseweb="select"] ul li {
    color: var(--text-color) !important;
}

/* Style for the select box when focused */
.stSelectbox > div > div:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 1px var(--primary-color);
}

/* Make sure the text is visible in all states */
.stSelectbox div[data-baseweb="select"] div {
    color: var(--text-color) !important;
}

/* Style for the placeholder text */
.stSelectbox [data-baseweb="select"] div[aria-selected="false"] {
    color: #666666 !important;
}

/* Sidebar styling */
.sidebar-header {
    text-align: center;
    padding: 1rem 0;
    margin-bottom: 1rem;
    border-bottom: 2px solid var(--primary-color);
}

.sidebar-header h2 {
    color: white !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin: 0;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: white !important;
    border-radius: 10px !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    padding: 0.5rem 1rem !important;
}

.streamlit-expanderHeader:hover {
    background-color: #f8f9fa !important;
    border-color: var(--primary-color) !important;
}

/* Filter group styling */
.filter-group {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Slider styling */
.stSlider > div > div > div {
    background-color: var(--primary-color) !important;
}

/* Multiselect styling */
.stMultiSelect > div > div {
    background-color: white;
    border-radius: 8px;
    border: 1px solid rgba(108,99,255,0.2);
}

.stMultiSelect > div > div:hover {
    border-color: var(--primary-color);
}

/* Help text styling */
.stMarkdown div.stMarkdown {
    font-size: 0.9rem;
    color: #666;
}

/* Download button styling */
.stDownloadButton button {
    background: var(--secondary-color) !important;
}

.stDownloadButton button:hover {
    background: var(--success-color) !important;
}

/* Preview checkbox styling */
.stCheckbox label {
    color: var(--text-color) !important;
    font-size: 0.9rem !important;
}

.stCheckbox label:hover {
    color: var(--primary-color) !important;
}

/* DataFrame styling */
.stDataFrame {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: var(--card-shadow);
}

/* Export section styling */
[data-testid="stExpander"] {
    background: white;
    border-radius: 10px;
    border: 1px solid rgba(108,99,255,0.1);
    margin-bottom: 1rem;
}

/* Welcome section styling */
.welcome-section {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: var(--card-shadow);
    margin: 1rem 0 2rem 0;
    border-left: 4px solid var(--primary-color);
}

.welcome-section h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.welcome-section ol {
    margin: 1rem 0;
    padding-left: 1.5rem;
}

.welcome-section li {
    margin: 0.5rem 0;
    color: var(--text-color);
}

.tip-box {
    background: #f8f9fa;
    padding: 1rem;
    border-left: 4px solid var(--primary-color);
    border-radius: 0 10px 10px 0;
    margin-top: 1rem;
}

.tip-box p {
    margin: 0;
    color: var(--text-color);
}

/* Sidebar text and input styling */
.sidebar .stSelectbox label,
.sidebar .stSlider label,
.sidebar .stMultiSelect label,
.sidebar .stNumberInput label {
    color: var(--text-color) !important;
    font-weight: 500 !important;
}

/* Sidebar expander styling */
.sidebar [data-testid="stExpander"] {
    background-color: white !important;
    border-radius: 10px !important;
    margin-bottom: 1rem !important;
}

.sidebar [data-testid="stExpander"] > div[role="button"] {
    color: var(--text-color) !important;
    font-weight: 500 !important;
}

/* Sidebar multiselect dropdown */
.sidebar .stMultiSelect > div > div {
    background-color: white !important;
    color: var(--text-color) !important;
}

/* Sidebar slider */
.sidebar .stSlider label {
    color: var(--text-color) !important;
}

.sidebar .stSlider [data-testid="stTickBar"] {
    color: var(--text-color) !important;
}

/* Sidebar number input */
.sidebar .stNumberInput label {
    color: var(--text-color) !important;
}

.sidebar .stNumberInput input {
    color: var(--text-color) !important;
    background-color: white !important;
}

/* Sidebar section headers */
.sidebar [data-testid="stMarkdown"] h3 {
    color: white !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    margin: 1rem 0 !important;
    padding: 0.5rem 0 !important;
    border-bottom: 2px solid rgba(255,255,255,0.1) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
}

/* Sidebar help text */
.sidebar .stMarkdown div {
    color: white !important;
}

/* Sidebar toggle button */
.sidebar [data-testid="baseButton-secondary"] {
    color: var(--text-color) !important;
    background-color: white !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
}

.sidebar [data-testid="baseButton-secondary"]:hover {
    border-color: var(--primary-color) !important;
    color: var(--primary-color) !important;
}

/* Sidebar divider */
.sidebar hr {
    margin: 1.5rem 0 !important;
    border-color: rgba(255,255,255,0.2) !important;
}

/* Sidebar selected values */
.sidebar .stMultiSelect [data-baseweb="tag"] {
    background-color: var(--primary-color) !important;
    color: white !important;
}

/* Sidebar dropdown options */
.sidebar [role="listbox"] {
    background-color: white !important;
}

.sidebar [role="option"] {
    color: var(--text-color) !important;
}

.sidebar [role="option"]:hover {
    background-color: rgba(108,99,255,0.1) !important;
}

/* Sidebar header styling */
.sidebar-header h2 {
    color: white !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
}

/* Sidebar text general styling */
.sidebar .stMarkdown {
    color: blue;
}

/* Display Options header and slider label */
.sidebar [data-testid="stMarkdown"] h3,
.sidebar .stSlider label {
    color: white !important;
}

/* Main sidebar headers (white) */
.sidebar-header h2,
.sidebar > [data-testid="stMarkdown"] h3 {
    color: white !important;
}

/* Advanced filter labels (black) */
.sidebar .stExpander label,
.sidebar .stExpander [data-testid="stMarkdown"] div {
    color: #2C3E50 !important;  /* Dark color for better readability */
    font-weight: 500 !important;
}

/* Keep basic genre filter label white */
.sidebar > .stMultiSelect label {
    color: white !important;
}

/* Keep number of recommendations label white */
.sidebar > .stSlider label {
    color: white !important;
}

/* Sort Results header in advanced filters should be black */
.sidebar .stExpander h3 {
    color: #2C3E50 !important;
}

/* Make text inside expanders black */
.sidebar .stExpander .streamlit-expanderContent label,
.sidebar .stExpander .streamlit-expanderContent p,
.sidebar .stExpander .streamlit-expanderContent span,
.sidebar .stExpander .streamlit-expanderContent div {
    color: #2C3E50 !important;  /* Dark color for better readability */
}

/* Make expander headers black */
.sidebar .stExpander [data-testid="stExpander"] > div[role="button"] {
    color: #2C3E50 !important;
}

/* Keep main headers white */
.sidebar-header h2,
.sidebar > [data-testid="stMarkdown"] h3,
.sidebar > .stMultiSelect label,
.sidebar > .stSlider label {
    color: white !important;
}

/* Make Sort Results text black inside expander */
.sidebar .stExpander [data-testid="stMarkdown"] h3 {
    color: #2C3E50 !important;
}

/* Make dropdown text black */
.sidebar .stExpander .stSelectbox label {
    color: #2C3E50 !important;
}

/* Make labels inside expanders dark */
.sidebar .stExpander .streamlit-expanderContent .stMultiSelect label,
.sidebar .stExpander .streamlit-expanderContent .stSelectbox label,
.sidebar .stExpander .streamlit-expanderContent .stSlider label,
.sidebar .stExpander .streamlit-expanderContent .stNumberInput label {
    color: #2C3E50 !important;  /* Dark color */
    font-weight: 500 !important;
}

/* Keep main headers white */
.sidebar-header h2,
.sidebar > [data-testid="stMarkdown"] h3,
.sidebar > .stMultiSelect label,
.sidebar > .stSlider label {
    color: white !important;
}

/* Make expander titles (like "Detailed Genre Preferences") dark */
.sidebar .stExpander [data-testid="stExpander"] {
    color: #2C3E50 !important;
}

/* Sidebar text colors */
/* Main headers in sidebar */
.sidebar-header h2 {
    color: white !important;
}

.sidebar > .stMultiSelect label,
.sidebar > .stSlider label {
    color: white !important;
}

/* Advanced filters section */
.sidebar .stExpander label,
.sidebar .stExpander p,
.sidebar .stExpander span,
.sidebar .stExpander div {
    color: var(--text-color) !important;
}

/* Expander headers */
.sidebar .stExpander [data-testid="stExpander"] {
    color: var(--text-color) !important;
}

/* Main content text colors */
.movie-title {
    color: var(--text-color) !important;
    font-weight: 600 !important;
}

.movie-details p {
    color: var(--text-color) !important;
}

/* Expander content */
.streamlit-expanderContent {
    color: var(--text-color) !important;
}

/* Slider text */
.stSlider [data-testid="stTickBar"] {
    color: var(--text-color) !important;
}

/* Multiselect options */
.stMultiSelect [data-baseweb="tag"] {
    color: white !important;
    background-color: var(--primary-color) !important;
}

/* Select box text */
.stSelectbox label {
    color: var(--text-color) !important;
}

/* Checkbox label */
.stCheckbox label {
    color: var(--text-color) !important;
}

/* Help text */
.stMarkdown div small {
    color: rgba(49, 51, 63, 0.6) !important;
}

/* Footer text */
.footer {
    color: var(--text-color) !important;
}

/* Success/warning messages */
.stSuccess {
    color: var(--success-color) !important;
}

.stWarning {
    color: var(--warning-color) !important;
}

/* Debug info text */
.sidebar pre {
    color: var(--text-color) !important;
}

/* Search box label */
.stTextInput label {
    color: var(--text-color) !important;
}

/* Watchlist items */
.watchlist-item {
    color: var(--text-color) !important;
}

/* Main sidebar labels (white) */
.sidebar > div > .stMarkdown h2,
.sidebar > div > .stMarkdown h3,
.sidebar > div > .stMultiSelect label,
.sidebar > div > .stSlider label {
    color: white !important;
}

/* Advanced filters section (black text on white background) */
.sidebar .stExpander {
    background-color: white !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

/* All text inside expanders should be dark */
.sidebar .stExpander label,
.sidebar .stExpander .stMarkdown p,
.sidebar .stExpander .stMarkdown h3,
.sidebar .stExpander .stSelectbox label,
.sidebar .stExpander .stMultiSelect label,
.sidebar .stExpander .stSlider label,
.sidebar .stExpander .stNumberInput label {
    color: #1F2937 !important;  /* Dark gray for better readability */
}

/* Expander header text */
.sidebar .stExpander [data-testid="stExpander"] > div[role="button"] {
    color: #1F2937 !important;
    font-weight: 500 !important;
}

/* Sort Results header inside advanced filters */
.sidebar .stExpander .stMarkdown h3 {
    color: #1F2937 !important;
    font-weight: 600 !important;
    margin-top: 1rem !important;
}

/* Help text color */
.sidebar .stExpander [data-testid="stTooltipIcon"] {
    color: #6B7280 !important;
}

/* Select/Multiselect dropdown text */
.sidebar .stExpander [data-baseweb="select"] {
    color: #1F2937 !important;
}

/* Selected values in multiselect */
.sidebar .stExpander [data-baseweb="tag"] {
    background-color: var(--primary-color) !important;
    color: white !important;
}

/* Slider values and ticks */
.sidebar .stExpander [data-testid="stTickBarMin"],
.sidebar .stExpander [data-testid="stTickBarMax"] {
    color: #1F2937 !important;
}

/* Main sidebar labels (white) */
.sidebar .element-container label {
    color: white !important;
}

/* Select Genres label (white) */
.sidebar > div > .stMultiSelect > label {
    color: white !important;
}

/* Dropdown text color (black) */
.sidebar [data-baseweb="select"] span {
    color: #1F2937 !important;
}

/* Placeholder text color */
.sidebar [data-baseweb="select"] [aria-selected="false"] {
    color: #6B7280 !important;
}

/* Selected option text color */
.sidebar [data-baseweb="select"] [aria-selected="true"] {
    color: #1F2937 !important;
}

/* Dropdown options text color */
.sidebar [role="listbox"] [role="option"] {
    color: #1F2937 !important;
}

/* Advanced filters section */
.sidebar .stExpander {
    background-color: white !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

/* All text inside expanders */
.sidebar .stExpander label,
.sidebar .stExpander span,
.sidebar .stExpander [data-baseweb="select"] span,
.sidebar .stExpander .stMarkdown p,
.sidebar .stExpander .stMarkdown h3 {
    color: #1F2937 !important;
}

/* Expander header */
.sidebar .stExpander > div[role="button"] {
    color: #1F2937 !important;
    font-weight: 500 !important;
}

/* Display Options header (white) */
.sidebar > div > .stMarkdown h3 {
    color: white !important;
}

/* Number of Recommendations label (white) */
.sidebar > div > .stSlider > label {
    color: white !important;
}

/* Sidebar text colors */
/* Main labels and headers */
.sidebar label,
.sidebar .stMarkdown p,
.sidebar .stMarkdown h3 {
    color: rgba(255, 255, 255, 0.87) !important;  /* Slightly transparent white */
}

/* Slider text and values */
.sidebar .stSlider [data-testid="stTickBarMin"],
.sidebar .stSlider [data-testid="stTickBarMax"] {
    color: white !important;
}

/* Multiselect labels and text */
.sidebar > div > .stMultiSelect > label,
.sidebar > div > .stMultiSelect [data-baseweb="select"] span {
    color: white !important;
}

/* Toggle button text */
.sidebar .stButton button {
    color: white !important;
}

/* Debug checkbox text */
.sidebar .stCheckbox label {
    color: white !important;
}

/* Number input text */
.sidebar .stNumberInput label,
.sidebar .stNumberInput input {
    color: white !important;
}

/* Advanced filters section (white background) */
.sidebar .stExpander {
    background-color: white !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

/* Text inside expanders (dark text) */
.sidebar .stExpander label,
.sidebar .stExpander p,
.sidebar .stExpander span,
.sidebar .stExpander div {
    color: #1F2937 !important;
}

/* Selected values in multiselect */
.sidebar [data-baseweb="tag"] {
    background-color: rgba(255, 255, 255, 0.2) !important;
    color: white !important;
}

/* Dropdown options */
.sidebar [role="listbox"] [role="option"] {
    color: #1F2937 !important;
}

/* Help tooltip icon */
.sidebar [data-testid="stTooltipIcon"] {
    color: rgba(255, 255, 255, 0.6) !important;
}

/* Mood-based discovery section */
.mood-section {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}

.mood-section h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

/* Recommendations section */
.recommendations-section {
    margin: 2rem 0;
    text-align: center;
}

/* Mood cards styling */
.mood-card {
    background: white;
    border-radius: 10px;
    padding: 0.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.mood-card:hover {
    transform: translateY(-5px);
}

.mood-card .movie-info {
    padding: 0.5rem;
}

.mood-card .movie-title {
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.mood-card .movie-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #666;
}

/* Mood selector styling */
.stSlider [data-baseweb="slider"] {
    margin-top: 1rem;
}

/* Movie card details */
.mood-card .movie-details {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #eee;
}

.mood-card .movie-details div {
    margin: 0.2rem 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.mood-card .director,
.mood-card .cast,
.mood-card .genres {
    font-size: 0.75rem;
    line-height: 1.2;
}

/* Enhance movie meta section */
.mood-card .movie-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0.3rem 0;
}

.mood-card .rating {
    color: #f1c40f;
    font-weight: 600;
}

.mood-card .year {
    color: #7f8c8d;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {}
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = set()
if 'preferences' not in st.session_state:
    st.session_state.preferences = {
        'favorite_genres': [],
        'exclude_genres': [],
        'min_year': 1990,
        'min_rating': 6.0
    }
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'main'
if 'selected_detail_movie' not in st.session_state:
    st.session_state.selected_detail_movie = None
if 'expanded_movie' not in st.session_state:
    st.session_state.expanded_movie = None
if 'current_recommendations' not in st.session_state:
    st.session_state.current_recommendations = {
        'movies': [],
        'details': []
    }
if 'show_advanced_filters' not in st.session_state:
    st.session_state.show_advanced_filters = False

# Load data and prepare genres
@st.cache_data
def load_data():
    try:
        # Load movie data
        with open("movie_dict.pickle","rb") as file:
            movies_dict = pickle.load(file)
            movies_df = pd.DataFrame(movies_dict)

        try:
            # Load similarity matrix
            with lzma.open("similarity3.xz", "rb") as file:
                similarity = pickle.load(file)
        except Exception as e:
            st.error(f"Error loading similarity matrix: {str(e)}")
            similarity = np.eye(len(movies_df))
        
        # Extract genres
        all_genres = set()
        for genres in movies_df['genres']:
            if isinstance(genres, list):
                all_genres.update(genres)
        all_genres = sorted(list(all_genres))
        
        return movies_df, similarity, all_genres
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(), np.array([]), []

movies, similarity, all_genres = load_data()

# Update the sidebar section
st.sidebar.markdown("""
<div class='sidebar-header'>
    <h2 style='color: white;'>🎯 Customize Your Recommendations</h2>
</div>
""", unsafe_allow_html=True)

# Update the basic genre filter
st.sidebar.markdown("<p class='main-label'>🎭 Select Genres</p>", unsafe_allow_html=True)
selected_genres = st.sidebar.multiselect(
    label="Select Genres",  # Add a proper label
    options=all_genres,
    help="Filter movies by genre",
    label_visibility="collapsed"  # Hide the label since we're using custom HTML
)

# Toggle for advanced filters
show_advanced = st.sidebar.toggle("Show Advanced Filters 🛠️", value=st.session_state.show_advanced_filters)
st.session_state.show_advanced_filters = show_advanced

# Advanced filters section
if st.session_state.show_advanced_filters:
    st.sidebar.markdown("---")
    
    # Genre Preferences
    with st.sidebar.expander("🎭 Detailed Genre Preferences", expanded=True):
        st.markdown("<p class='filter-label'>Must Include</p>", unsafe_allow_html=True)
        include_genres = st.multiselect(
            label="Must Include Genres",  # Add a proper label
            options=all_genres,
            help="Movies must have at least one of these genres",
            key="include_genres",
            label_visibility="collapsed"  # Hide the label
        )
        
        st.markdown("<p class='filter-label'>Must Exclude</p>", unsafe_allow_html=True)
        exclude_genres = st.multiselect(
            label="Must Exclude Genres",  # Add a proper label
            options=all_genres,
            help="Movies must not have these genres",
            key="exclude_genres",
            label_visibility="collapsed"  # Hide the label
        )

    # Release Year & Rating
    with st.sidebar.expander("📅 Release Year & Rating", expanded=True):
        year_min, year_max = st.select_slider(
            "Release Year Range",
            options=list(range(1950, datetime.now().year + 1)),
            value=(1990, datetime.now().year),
            help="Select the range of movie release years"
        )
        
        min_rating = st.slider(
            "Minimum Rating",
            min_value=0.0,
            max_value=10.0,
            value=6.0,
            step=0.5,
            help="Filter movies by minimum rating"
        )
        
        min_votes = st.number_input(
            "Minimum Number of Votes",
            min_value=0,
            max_value=10000,
            value=100,
            step=50,
            help="Filter movies by minimum number of votes"
        )

    # Additional Filters
    with st.sidebar.expander("🎬 Additional Filters", expanded=False):
        max_runtime = st.slider(
            "Maximum Runtime (minutes)",
            min_value=60,
            max_value=240,
            value=180,
            step=15,
            help="Filter movies by maximum runtime"
        )
        
        language_filter = st.multiselect(
            "Language",
            ["EN", "ES", "FR", "DE", "IT", "JA", "KO", "ZH"],
            default=["EN"],
            help="Select preferred languages"
        )

    # Fine-tune Results
    with st.sidebar.expander("🎯 Fine-tune Results", expanded=False):
        similarity_weight = st.slider(
            "Similarity Impact",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values favor similarity to selected movie, lower values favor matching filters"
        )

    # Sorting options
    st.sidebar.markdown("### 🔄 Sort Results")
    sort_col1, sort_col2 = st.sidebar.columns(2)
    with sort_col1:
        sort_by = st.selectbox(
            "Sort By",
            ["Similarity", "Rating", "Year", "Title", "Runtime"],
            index=0
        )
    with sort_col2:
        sort_order = st.selectbox(
            "Order",
            ["Descending", "Ascending"],
            index=0
        )

else:
    # Default values for when advanced filters are off
    include_genres = selected_genres
    exclude_genres = []
    year_min, year_max = 1990, datetime.now().year
    min_rating = 6.0
    min_votes = 100
    max_runtime = 240
    language_filter = ["EN"]
    similarity_weight = 0.7
    sort_by = "Similarity"
    sort_order = "Descending"

# Number of recommendations (always visible)
st.sidebar.markdown("<h3 style='color: white;'>📊 Display Options</h3>", unsafe_allow_html=True)
rec_count = st.sidebar.slider(
    "Number of Recommendations",
    min_value=5,
    max_value=20,
    value=10,
    step=5,
    help="Choose how many movies to display"
)

# Add this before the recommendation button
if st.sidebar.checkbox("Show Debug Info", False):
    st.sidebar.write("Current Filters:")
    st.sidebar.json({
        "include_genres": include_genres,
        "exclude_genres": exclude_genres,
        "year_range": [year_min, year_max],
        "min_rating": min_rating,
        "min_votes": min_votes,
        "max_runtime": max_runtime,
        "language_filter": language_filter,
        "sort_by": sort_by,
        "sort_order": sort_order
    })

# Enhanced movie details fetching
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7179d8558db0ffd107a6329fbecee361&language=en-US"
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=7179d8558db0ffd107a6329fbecee361"
    
    try:
        data = requests.get(url).json()
        credits_data = requests.get(credits_url).json()
        
        # Get director
        director = next((crew['name'] for crew in credits_data.get('crew', []) if crew['job'] == 'Director'), 'N/A')
        # Get top cast
        cast = [actor['name'] for actor in credits_data.get('cast', [])[:3]]
        
        return {
            'poster_path': f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get('poster_path') else None,
            'rating': round(data.get('vote_average', 0), 1),
            'year': data.get('release_date', '')[:4],
            'runtime': data.get('runtime'),
            'overview': data.get('overview'),
            'genres': [genre['name'] for genre in data.get('genres', [])],
            'director': director,
            'cast': cast,
            'vote_count': data.get('vote_count', 0),
            'language': data.get('original_language', 'N/A').upper()
        }
    except:
        return None

def get_movie_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=7179d8558db0ffd107a6329fbecee361"
    try:
        data = requests.get(url).json()
        for video in data['results']:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                return f"https://www.youtube.com/watch?v={video['key']}"
    except:
        pass
    return None

# First, add this helper function to check genres
def check_genres(movie_genres, include_genres, exclude_genres):
    movie_genres = set(movie_genres)
    # If include_genres is specified, movie must have at least one of them
    if include_genres and not set(include_genres) & movie_genres:
        return False
    # If exclude_genres is specified, movie must not have any of them
    if exclude_genres and set(exclude_genres) & movie_genres:
        return False
    return True

# Update the meets_criteria function
def meets_criteria(details, movie_data, include_genres, exclude_genres,
                  year_min, year_max, min_rating, min_votes,
                  max_runtime, language_filter):
    try:
        # Year filter
        movie_year = int(details['year']) if details['year'].isdigit() else 0
        if not (year_min <= movie_year <= year_max):
            return False
        
        # Rating and votes filter
        if details['rating'] < min_rating:
            return False
        if details['vote_count'] < min_votes:
            return False
        
        # Runtime filter
        if details.get('runtime', 0) and details['runtime'] > max_runtime:
            return False
        
        # Language filter
        if language_filter and details['language'] not in language_filter:
            return False
        
        # Genre filtering using movie_data's genres
        if not check_genres(movie_data['genres'], include_genres, exclude_genres):
            return False
        
        return True
    except Exception as e:
        st.sidebar.warning(f"Error checking criteria: {str(e)}")
        return False

# Update the recommend function to use these filters
def recommend(movie, include_genres=None, exclude_genres=None):
    try:
        # Get the selected movie's index and similarity scores
        movie_index = movies[movies["title"]==movie].index[0]
        distances = similarity[movie_index]
        
        # Get more initial recommendations to allow for filtering
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:100]  # Increased from 50
        
        # Get the selected movie's genres for better recommendations
        selected_movie_data = movies.iloc[movie_index]
        selected_movie_genres = set(selected_movie_data['genres'])
        
        recommended_movies = []
        recommended_movies_details = []
        similarity_scores = []
        
        for i, sim_score in movie_list:
            movie_data = movies.iloc[i]
            movie_id = movie_data['id']
            details = fetch_movie_details(movie_id)
            
            if details:
                try:
                    # Apply all filters
                    if not meets_criteria(details, movie_data,
                                       include_genres, exclude_genres,
                                       year_min, year_max,
                                       min_rating, min_votes,
                                       max_runtime, language_filter):
                        continue
                    
                    # Calculate a combined score based on similarity and genre overlap
                    movie_genres = set(movie_data['genres'])
                    genre_overlap = len(selected_movie_genres & movie_genres) / len(selected_movie_genres | movie_genres)
                    combined_score = (sim_score * similarity_weight) + (genre_overlap * (1 - similarity_weight))
                    
                    recommended_movies.append(movie_data['title'])
                    recommended_movies_details.append(details)
                    similarity_scores.append(combined_score)
                    
                    if len(recommended_movies) >= rec_count:
                        break
                        
                except Exception as e:
                    st.sidebar.warning(f"Error processing movie {movie_data['title']}: {str(e)}")
                    continue
        
        # Sort by combined score before applying other sorts
        if sort_by == "Similarity":
            # Sort by combined similarity score
            sorted_indices = sorted(range(len(similarity_scores)), 
                                 key=lambda k: similarity_scores[k],
                                 reverse=True)
            recommended_movies = [recommended_movies[i] for i in sorted_indices]
            recommended_movies_details = [recommended_movies_details[i] for i in sorted_indices]
        else:
            # Apply other sorting criteria
            recommended_movies, recommended_movies_details = sort_recommendations(
                recommended_movies, 
                recommended_movies_details, 
                sort_by, 
                sort_order == "Ascending"
            )
        
        return recommended_movies, recommended_movies_details
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return [], []

# Add this after the recommend function
def sort_recommendations(movies_list, details_list, sort_by, ascending=False):
    if not movies_list or not details_list:
        return movies_list, details_list
        
    sorted_indices = []
    if sort_by == "Rating":
        sorted_indices = sorted(range(len(details_list)), 
                              key=lambda k: details_list[k]['rating'],
                              reverse=not ascending)
    elif sort_by == "Year":
        sorted_indices = sorted(range(len(details_list)), 
                              key=lambda k: int(details_list[k]['year']) if details_list[k]['year'].isdigit() else 0,
                              reverse=not ascending)
    elif sort_by == "Title":
        sorted_indices = sorted(range(len(movies_list)), 
                              key=lambda k: movies_list[k],
                              reverse=not ascending)
    elif sort_by == "Runtime":
        sorted_indices = sorted(range(len(details_list)), 
                              key=lambda k: details_list[k].get('runtime', 0),
                              reverse=not ascending)
    else:  # Similarity - already sorted by default
        return movies_list, details_list
    
    return ([movies_list[i] for i in sorted_indices], 
            [details_list[i] for i in sorted_indices])

# Main content
st.markdown("""
    <style>
    /* Modern color palette and overall theme */
    :root {
        --primary-color: #6366F1;      /* Modern indigo */
        --accent-color: #FF6B6B;       /* Coral */
        --bg-color: #F8F9FD;           /* Light background */
        --text-color: #1F2937;         /* Dark gray */
        --card-bg: #FFFFFF;            /* White */
        --hover-color: #4F46E5;        /* Darker indigo for hover */
    }

    /* Page background */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
    }

    /* Override Streamlit's default header colors */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-color) !important;
    }

    .big-font {
        font-size: 3.2rem !important;
        font-weight: 800;
        background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
        margin-bottom: 2rem;
    }

    .movie-title {
        font-size: 1rem;
        font-weight: 600;
        text-align: center;
        padding: 15px 10px;
        color: var(--text-color);
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        line-height: 1.4;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    .movie-container {
        background-color: var(--card-bg);
        padding: 15px 25px;
        border-radius: 16px;
        margin: 10px 5px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        width: 100%;
        margin-left: auto;
        margin-right: auto;
        border: 1px solid rgba(0,0,0,0.05);
    }

    .movie-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(108,99,255,0.1);
        border-color: var(--primary-color);
    }

    /* Style for select box container */
    .select-container {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background: var(--card-bg);
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }

    /* Modern button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, var(--primary-color), var(--hover-color));
        color: white;
        font-weight: 600;
        padding: 12px 20px;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(108,99,255,0.2);
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: var(--card-bg);
        border-radius: 12px;
        border: 1px solid rgba(108,99,255,0.2);
    }

    .stSelectbox > div > div:hover {
        border-color: var(--primary-color);
    }

    /* Spinner styling */
    .stSpinner > div {
        border-color: var(--primary-color) !important;
    }

    /* Recommendations header styling */
    h3 {
        font-size: 1.5rem !important;
        color: var(--text-color) !important;
        font-weight: 700 !important;
        text-align: center;
        margin: 2rem 0;
    }

    /* Select box label color */
    .stSelectbox label {
        color: var(--text-color) !important;
        font-weight: 600;
    }

    /* Footer styling */
    footer, footer p {
        color: var(--text-color) !important;
    }

    /* Adjust column gaps */
    .row-widget.stHorizontal {
        gap: 1rem;
    }

    /* Increase width of select box */
    .stSelectbox {
        width: 100%;
    }

    div[data-baseweb="select"] {
        width: 100%;
    }

    .movie-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    .rating-badge {
        background: #6366F1;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.9rem;
    }

    .movie-meta {
        font-size: 0.9rem;
        color: #666;
        margin: 0.5rem 0;
    }

    .stExpander {
        border: none;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Add a custom header
st.markdown("""
<div class="app-header">
    <h1>🎬 Movie Recommendation System</h1>
    <p>Discover your next favorite movie</p>
</div>
""", unsafe_allow_html=True)

# Add after the header and before the search section
st.markdown("""
<div class="welcome-section">
    <h3>👋 Welcome to Your Personal Movie Guide!</h3>
    <p>Here's how to get started:</p>
    <ol>
        <li>🔍 Search and select a movie you love</li>
        <li>🎭 Optionally, use filters to refine your recommendations</li>
        <li>✨ Click "Show Me Recommendations" to discover similar movies</li>
    </ol>
    <div class="tip-box">
        <p>💡 <strong>Pro Tip:</strong> Toggle "Advanced Filters" for more precise recommendations based on genres, ratings, and more!</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Search section with better styling
st.markdown("""
<div class="search-container">
    <h3>🔍 Find Movies</h3>
</div>
""", unsafe_allow_html=True)

# Search functionality
search_term = st.text_input("Search for a movie by title", key="search_input")
if search_term:
    filtered_movies = movies[movies['title'].str.contains(search_term, case=False, na=False)]
    if not filtered_movies.empty:
        st.write(f"Found {len(filtered_movies)} matches")
        selected_movie = st.selectbox(
            "Select a Movie You Love 💝", 
            filtered_movies["title"].values,
            key="filtered_movie_select",
            format_func=lambda x: x  # Ensure proper text formatting
        )
    else:
        st.warning("No movies found matching your search.")
else:
    if not movies.empty:
        selected_movie = st.selectbox(
            "Select a Movie You Love 💝", 
            movies["title"].values,
            key="all_movies_select",
            format_func=lambda x: x  # Ensure proper text formatting
        )
    else:
        st.error("No movie data available. Please check the data files.")
        st.stop()

# Main content section - Add this after the search functionality
if st.session_state.current_view == 'detail' and st.session_state.selected_detail_movie:
    # Show detail page
    show_movie_detail_page(
        st.session_state.selected_detail_movie['title'],
        st.session_state.selected_detail_movie['details']
    )
else:
    # Show main view with recommendations
    if st.button("Show Me Recommendations ✨", key="main_recommend_button"):
        with st.spinner('Finding movies you might love...'):
            recommended_movies, movie_details = recommend(
                movie=selected_movie,
                include_genres=include_genres,
                exclude_genres=exclude_genres
            )
            
            if not recommended_movies:
                st.warning("No movies found matching your criteria. Try adjusting your filters.")
            else:
                # Save recommendations to session state
                st.session_state.current_recommendations['movies'] = recommended_movies
                st.session_state.current_recommendations['details'] = movie_details
                
                # Display recommendations
                st.markdown("### 🌟 Here are your personalized recommendations")
                
                # Create columns for movie cards
                cols = st.columns(5)
                for idx, (movie, details) in enumerate(zip(recommended_movies, movie_details)):
                    with cols[idx % 5]:
                        with st.container():
                            st.markdown("""
                            <div class="movie-card">
                                <div class="movie-poster">
                            """, unsafe_allow_html=True)
                            
                            if details['poster_path']:
                                st.image(details['poster_path'], use_container_width=True)
                            
                            st.markdown(f"""
                                </div>
                                <div class="movie-info">
                                    <div class="movie-title">{movie}</div>
                                    <div style="text-align: center">
                                        <span class="rating-badge">⭐ {details['rating']}</span>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show movie details in expander
                            with st.expander("Show Details 🎬"):
                                st.markdown(f"""
                                <div class='movie-details'>
                                    <div class='rating-section'>
                                        <span class='rating-badge'>⭐ {details['rating']}</span>
                                        <span class='vote-count'>({details['vote_count']} votes)</span>
                                    </div>
                                    <div class='movie-meta'>
                                        🎬 {details['year']} | ⏱️ {details.get('runtime', 'N/A')} min | 🌍 {details['language']}
                                    </div>
                                    <div class='movie-info'>
                                        <p><strong>Overview:</strong><br>{details['overview']}</p>
                                        <p><strong>Genres:</strong><br>{", ".join(details['genres'])}</p>
                                        <p><strong>Director:</strong><br>{details['director']}</p>
                                        <p><strong>Cast:</strong><br>{", ".join(details['cast'])}</p>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Trailer
                                movie_id = movies[movies['title'] == movie]['id'].iloc[0]
                                if trailer_url := get_movie_trailer(movie_id):
                                    st.video(trailer_url)
                                
                                # User interactions
                                rating = st.select_slider(
                                    "Rate this movie",
                                    options=[1, 2, 3, 4, 5],
                                    value=st.session_state.user_ratings.get(movie, 3),
                                    key=f"rating_{movie}"
                                )
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("Save Rating", key=f"save_{movie}"):
                                        st.session_state.user_ratings[movie] = rating
                                        st.success("Rating saved!")
                                
                                with col2:
                                    if movie in st.session_state.watchlist:
                                        if st.button("❌ Remove", key=f"watchlist_{movie}"):
                                            st.session_state.watchlist.remove(movie)
                                            st.success("Removed!")
                                    else:
                                        if st.button("➕ Watchlist", key=f"watchlist_{movie}"):
                                            st.session_state.watchlist.add(movie)
                                            st.success("Added!")

# Display watchlist
if st.session_state.watchlist:
    st.markdown("### 📋 Your Watchlist")
    for movie in st.session_state.watchlist:
        st.write(f"- {movie}")

# Export recommendations
if st.session_state.current_recommendations['movies']:
    with st.container():
        st.markdown("### 📥 Export Recommendations")
        
        # Create DataFrame with detailed information
        export_data = []
        for movie, details in zip(st.session_state.current_recommendations['movies'],
                                st.session_state.current_recommendations['details']):
            export_data.append({
                'Title': movie,
                'Rating': details['rating'],
                'Year': details['year'],
                'Runtime': details.get('runtime', 'N/A'),
                'Language': details['language'],
                'Director': details['director'],
                'Cast': ', '.join(details['cast']),
                'Genres': ', '.join(details['genres']),
                'Vote Count': details['vote_count']
            })
        
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False).encode('utf-8')
        
        col1, col2 = st.columns([2, 1])
        with col1:
            # Download button
            st.download_button(
                label="📥 Download Recommendations as CSV",
                data=csv,
                file_name=f"movie_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Download your personalized movie recommendations"
            )
        
        with col2:
            show_preview = st.checkbox("View CSV here", False)
        
        if show_preview:
            st.markdown("#### CSV Preview")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ for movie lovers</p>
        <p>Data provided by <a href="https://www.themoviedb.org/">TMDb</a></p>
    </div>
""", unsafe_allow_html=True)

# Add this function near the top
def show_movie_detail_page(movie, details):
    # Back button
    if st.button("← Back to Recommendations", key="back_button"):
        reset_view()
        st.rerun()
    
    # Movie detail layout
    st.title(movie)
    
    # Movie info section
    poster_col, info_col = st.columns([1, 2])
    
    with poster_col:
        if details['poster_path']:
            st.image(details['poster_path'], use_container_width=True)
    
    with info_col:
        st.markdown(f"""
        <div class='movie-details-full'>
            <div class='rating-section-large'>
                <span class='rating-badge-large'>⭐ {details['rating']}</span>
                <span class='vote-count'>({details['vote_count']} votes)</span>
            </div>
            <div class='movie-meta-large'>
                🎬 {details['year']} | ⏱️ {details.get('runtime', 'N/A')} min | 🌍 {details['language']}
            </div>
            <div class='genre-tags'>
                {" ".join([f'<span class="genre-tag">{genre}</span>' for genre in details['genres']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Overview section
    st.markdown("### Overview")
    st.write(details['overview'])
    
    # Cast and Director
    st.markdown("### Cast & Crew")
    st.write(f"**Director:** {details['director']}")
    st.write(f"**Cast:** {', '.join(details['cast'])}")
    
    # Trailer section
    st.markdown("### Trailer")
    movie_id = movies[movies['title'] == movie]['id'].iloc[0]
    if trailer_url := get_movie_trailer(movie_id):
        st.video(trailer_url)
    else:
        st.info("No trailer available")
    
    # User interaction section
    st.markdown("### Rate & Save")
    rating = st.select_slider(
        "Rate this movie",
        options=[1, 2, 3, 4, 5],
        value=st.session_state.user_ratings.get(movie, 3),
        key=f"rating_detail_{movie}"
    )
    
    # Rating and Watchlist buttons
    rate_col, watch_col = st.columns(2)
    with rate_col:
        if st.button("Save Rating", key=f"save_detail_{movie}"):
            st.session_state.user_ratings[movie] = rating
            st.success("Rating saved!")
    
    with watch_col:
        if movie in st.session_state.watchlist:
            if st.button("❌ Remove from Watchlist", key=f"watchlist_detail_{movie}"):
                st.session_state.watchlist.remove(movie)
                st.success("Removed from watchlist!")
        else:
            if st.button("➕ Add to Watchlist", key=f"watchlist_detail_{movie}"):
                st.session_state.watchlist.add(movie)
                st.success("Added to watchlist!")

# Add this function
def reset_view():
    st.session_state.current_view = 'main'
    st.session_state.selected_detail_movie = None

# Add the expanded view using Streamlit dialog
if st.session_state.expanded_movie:
    movie = st.session_state.expanded_movie['movie']
    details = st.session_state.expanded_movie['details']
    
    with st.container():
        # Close button
        if st.button("← Back", key="close_expanded"):
            st.session_state.expanded_movie = None
            st.rerun()
        
        # Movie details in two columns
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(details['poster_path'], use_container_width=True, caption="")
        
        with col2:
            st.markdown(f"<h1 class='movie-title-large'>{movie}</h1>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='movie-details-large'>
                <div style='margin-bottom: 1rem'>
                    <span class='rating-badge-large'>⭐ {details['rating']}</span>
                    <span style='margin-left: 1rem'>({details['vote_count']} votes)</span>
                </div>
                <div style='margin-bottom: 1rem'>
                    🎬 {details['year']} | ⏱️ {details.get('runtime', 'N/A')} min | 🌍 {details['language']}
                </div>
                <p><strong>Overview</strong><br>{details['overview']}</p>
                <p><strong>Genres</strong><br>{", ".join(details['genres'])}</p>
                <p><strong>Director</strong><br>{details['director']}</p>
                <p><strong>Cast</strong><br>{", ".join(details['cast'])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Trailer
            movie_id = movies[movies['title'] == movie]['id'].iloc[0]
            if trailer_url := get_movie_trailer(movie_id):
                st.video(trailer_url)
            
            # User interactions
            col1, col2 = st.columns(2)
            with col1:
                rating = st.select_slider(
                    "Rate this movie",
                    options=[1, 2, 3, 4, 5],
                    value=st.session_state.user_ratings.get(movie, 3),
                    key=f"rating_expanded_{movie}"
                )
                if st.button("Save Rating", key=f"save_expanded_{movie}"):
                    st.session_state.user_ratings[movie] = rating
                    st.success("Rating saved!")
            
            with col2:
                if movie in st.session_state.watchlist:
                    if st.button("❌ Remove from Watchlist", key=f"watchlist_expanded_{movie}"):
                        st.session_state.watchlist.remove(movie)
                        st.success("Removed from watchlist!")
                else:
                    if st.button("➕ Add to Watchlist", key=f"watchlist_expanded_{movie}"):
                        st.session_state.watchlist.add(movie)
                        st.success("Added to watchlist!")

# Add these cache decorators and functions at the beginning of your file, after imports
@st.cache_data(ttl=3600)
def fetch_movie_details_cached(movie_id):
    return fetch_movie_details(movie_id)

@st.cache_data(ttl=3600)
def get_mood_based_movies(mood_settings, filtered_movies, limit=10):
    recommendations = []
    
    for _, movie in filtered_movies.iterrows():
        details = fetch_movie_details_cached(movie['id'])
        if details:
            try:
                year = int(details['year'])
                if (details['rating'] >= mood_settings['min_rating'] and
                    mood_settings['years'][0] <= year <= mood_settings['years'][1]):
                    recommendations.append((movie['title'], details))
                    
                    if len(recommendations) >= limit:
                        break
            except ValueError:
                continue
    
    # Sort by rating
    recommendations.sort(key=lambda x: x[1]['rating'], reverse=True)
    return recommendations

# Update the mood-based discovery section
with st.expander("🎭 Mood-Based Discovery", expanded=False):
    # Use a container for full width
    with st.container():
        # Header section with gradient background
        st.markdown("""
            <div class='mood-section'>
                <h2>Find Movies Based on Your Mood</h2>
                <p>Let us suggest movies that match how you're feeling right now!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Mood selector section
        st.markdown("""
            <div class='mood-selector-section'>
                <h3>How are you feeling today?</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for mood selection
        col1, col2 = st.columns([3, 2])
        
        with col1:
            selected_mood = st.select_slider(
                "",  # Remove label since we have it in the header
                options=list(MOODS.keys()),
                value=list(MOODS.keys())[0]
            )
            
            # Show mood description below slider
            st.markdown(f"""
                <div class='mood-description'>
                    <p>{MOODS[selected_mood]["description"]}</p>
                    <div class='mood-genres'>
                        Suggested genres: {', '.join(MOODS[selected_mood]["genres"])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write("")  # Add some spacing
            st.write("")
            if st.button("Find Movies ✨", use_container_width=True, type="primary"):
                with st.spinner('Finding the perfect movies for your mood...'):
                    # Get recommendations using cached function
                    filtered_movies = movies[
                        movies['genres'].apply(lambda x: any(genre in x for genre in MOODS[selected_mood]["genres"]))
                    ]
                    recommendations = get_mood_based_movies(MOODS[selected_mood], filtered_movies)
                    
                    if recommendations:
                        # Results section
                        st.markdown("""
                        <div class='recommendations-header'>
                            <h3>🎬 Your Mood-Based Recommendations</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display movies in a grid
                        movie_cols = st.columns(3)  # Reduce to 3 columns for bigger cards
                        for idx, (movie, details) in enumerate(recommendations):
                            with movie_cols[idx % 3]:
                                # Movie card
                                st.markdown(f"""
                                <div class="mood-movie-card">
                                    <div class="movie-poster">
                                        <img src="{details['poster_path']}" alt="{movie}">
                                    </div>
                                    <div class="movie-content">
                                        <h4>{movie}</h4>
                                        <div class="movie-meta">
                                            <span class="rating">⭐ {details['rating']}</span>
                                            <span class="year">{details['year']}</span>
                                        </div>
                                        <div class="movie-details">
                                            <p class="director">🎬 {details['director']}</p>
                                            <p class="cast">👥 {', '.join(details['cast'][:2])}</p>
                                            <p class="genres">{', '.join(details['genres'][:3])}</p>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning("No movies found matching your mood criteria. Try adjusting the mood!")

    
