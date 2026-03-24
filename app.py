import streamlit as st
import RAG.config as rag_config
from RAG.rag_main import run_hybrid_rag_pipeline

st.set_page_config(
    page_title="Sweden Labour Market Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_app_config():
    return rag_config.load_environment_variables()

@st.cache_resource
def get_llm_client():
    app_config = load_app_config()
    return rag_config.get_llm_client(app_config)

@st.cache_data(show_spinner=False, ttl=600)
def get_rag_result(user_question: str):
    return run_hybrid_rag_pipeline(user_question)

# optional warm-up
load_app_config()
get_llm_client()

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
        font-size: 38px;
        font-weight: 700;
        color: #F7E9DC;
        margin-bottom: 40px;
    ">
        Labour Market Intelligence Platform
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
    if not user_question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Analyzing labour market data..."):
            try:
                result = get_rag_result(user_question)

                final_answer = result.get("final_answer", "No answer generated.")
                sql_query = result.get("sql_query", "")
                sql_preview = result.get("sql_data_preview", [])

                st.markdown("### Insight")
                st.markdown(final_answer)

                with st.expander("Generated SQL"):
                    st.code(sql_query, language="sql")

                with st.expander("SQL Data Preview"):
                    st.json(sql_preview)

            except Exception as e:
                st.error(f"Something went wrong: {e}")