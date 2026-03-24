import streamlit as st

st.set_page_config(
    page_title="Sweden Labour Market Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# COLORS
# -------------------------
PAGE_BG = "#89AAA0"
SIDEBAR_BG = "#355C46"
DROPDOWN_BORDER = "#E6C3A5"
TEXT_COLOR = "#F7E9DC"

# -------------------------
# CUSTOM CSS
# -------------------------
custom_css = f"""
<style>
    .stApp {{
        background-color: {PAGE_BG};
        color: {TEXT_COLOR};
    }}

    header[data-testid="stHeader"] {{
        background-color: {PAGE_BG};
    }}

    div[data-testid="stToolbar"] {{
        background-color: {PAGE_BG};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG};
        border-right: 5px solid {DROPDOWN_BORDER};
        padding-top: 20px;
    }}

    section[data-testid="stSidebar"] * {{
        color: {TEXT_COLOR};
    }}

    h1, h2, h3, h4, h5, h6,
    p, div, span, label {{
        color: {TEXT_COLOR};
    }}

    .stCaption {{
        color: {TEXT_COLOR} !important;
        opacity: 0.95;
    }}

    /* Buttons */
    div.stButton > button {{
        background-color: {SIDEBAR_BG} !important;
        color: {DROPDOWN_BORDER} !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }}

    div.stButton > button:hover,
    div.stButton > button:hover p,
    div.stButton > button:hover span {{
        background-color: {TEXT_COLOR} !important;
        color: {SIDEBAR_BG} !important;
        cursor: pointer;
    }}

    /* Text area */
    textarea {{
        background-color: {TEXT_COLOR} !important;
        color: {SIDEBAR_BG} !important;
        border: 2px solid {SIDEBAR_BG} !important;
        border-radius: 0 !important;
    }}

    /* Response container */
    .response-box {{
        background-color: {TEXT_COLOR};
        border: 2px solid {SIDEBAR_BG};
        border-radius: 0;
        padding: 20px;
        margin-top: 10px;
    }}

    .response-box,
    .response-box p,
    .response-box div,
    .response-box span {{
        color: {SIDEBAR_BG} !important;
    }}

    .response-text {{
        font-size: 15px;
        line-height: 1.6;
        color: {SIDEBAR_BG} !important;
    }}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.markdown(
    """
    <div style="
        font-size: 40px;
        font-weight: 700;
        color: #F7E9DC;
        margin-bottom: 40px;
    ">
        Sweden Labour Market Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# MAIN PAGE
# -------------------------
st.header("AI Planning Assistant")
st.caption(
    "Ask strategic questions about labour market trends and receive data-driven insights for university planning."
)

user_question = st.text_area(
    "Ask a question about labour market trends",
    height=140,
    placeholder="Example: Where in Sweden is IT demand growing the fastest, and which regions show emerging skill gaps universities should respond to?"
)

# -------------------------
# GENERATE RESPONSE
# -------------------------
if st.button("Generate Insight"):
    with st.spinner("Analyzing labour market data..."):
        response = """
**Key Insights**
- Labour demand appears concentrated in major urban regions, especially in technical and digital occupations.
- Some regions show sustained demand patterns that may indicate future skills shortages.
- These signals can help universities identify where capacity expansion or program updates may be most relevant.

**Implications for Universities**
- Review current program capacity in regions with strong employer demand.
- Consider expanding technical and engineering-related programs where labour demand remains high.
- Strengthen collaboration with employers to validate whether these demand patterns are sustained over time.
"""
        st.markdown(
            f"""
            <div class="response-box">
                <div class="response-text">{response.replace(chr(10), '<br>')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )