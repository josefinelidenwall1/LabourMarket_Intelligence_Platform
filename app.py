# Import Streamlit library
import streamlit as st


# Configure the page (must be the first Streamlit command)
st.set_page_config(
    page_title="Sweden Labour Market Intelligence Platform",  # Browser tab title
    page_icon="📊",  # Icon shown in the tab
    layout="wide"  # Use full-width layout for dashboard feel
)

# Custom CSS to style the app.
# This lets us apply a visual theme inspired by your slide colors.
custom_css = """
<style>
    /* Main app background */
    .stApp {
        background-color: #7FA79A;
        color: #F7E9DC;
    }

    /* Top header */
    header[data-testid="stHeader"] {
        background-color: #7FA79A;
    }

    div[data-testid="stToolbar"] {
        background-color: #7FA79A;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #355C46;
        border-right: 3px solid #E6C3A5;
        padding-top: 20px;
    }

    section[data-testid="stSidebar"] * {
        color: #F7E9DC;
    }

    /* ALL text elements */
    h1, h2, h3, h4, h5, h6,
    p, div, span, label {
        color: #F7E9DC;
    }

    /* Caption override (Streamlit dims captions by default) */
    .stCaption {
        color: #F7E9DC !important;
        opacity: 0.95;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: rgba(230, 195, 165, 0.15);
        border: 1px solid rgba(247, 233, 220, 0.25);
        padding: 15px;
        border-radius: 14px;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #E6C3A5;
        color: #355C46;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #F0D2B9;
        color: #2E4E3C;
    }

    /* Insight cards */
    .insight-card {
        background-color: rgba(230, 195, 165, 0.15);
        border: 1px solid rgba(247, 233, 220, 0.25);
        border-radius: 16px;
        padding: 18px;
        margin-top: 10px;
    }

    .insight-title {
        font-size: 18px;
        font-weight: 700;
        color: #E6C3A5;  /* keep accent for titles */
        margin-bottom: 8px;
    }

    .insight-text {
        font-size: 15px;
        color: #F7E9DC;
    }
</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar branding (acts like app header)
st.sidebar.markdown(
    """
    <div style="
        font-size: 22px;
        font-weight: 700;
        color: color: #f7e9dc;
        margin-bottom: 40px;
    ">
        Sweden Labour Market Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)


# Sidebar navigation menu
# This allows switching between pages
menu = st.sidebar.radio(
    "Navigation",  # Title of the sidebar section
    ["Labour Market Analytics", "AI Planning Assistant"]  # Page options
)

st.caption("Supporting university program planning through real-time labour market intelligence")

# Page routing logic
# Based on what user selects in sidebar, show different content

if menu == "Labour Market Analytics":
    # This is the Analytics page
    st.header("Labour Market Analytics")

elif menu == "AI Planning Assistant":
    # This is the AI Assistant page
    st.header("AI Planning Assistant")