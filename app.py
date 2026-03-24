# Import Streamlit library
import streamlit as st


# Configure the page (must be the first Streamlit command)
st.set_page_config(
    page_title="Sweden Labour Market Intelligence Platform",  # Browser tab title
    page_icon="📊",  # Icon shown in the tab
    layout="wide"  # Use full-width layout for dashboard feel
)


# Main title of the app
st.title("Sweden Labour Market Intelligence Platform")

# Short description under the title
st.caption(
    "Supporting university program planning through real-time labour market intelligence"
)


# Sidebar navigation menu
# This allows switching between pages
menu = st.sidebar.radio(
    "Navigation",  # Title of the sidebar section
    ["Labour Market Analytics", "AI Planning Assistant"]  # Page options
)


# Page routing logic
# Based on what user selects in sidebar, show different content

if menu == "Labour Market Analytics":
    # This is the Analytics page
    st.header("Labour Market Analytics")

elif menu == "AI Planning Assistant":
    # This is the AI Assistant page
    st.header("AI Planning Assistant")