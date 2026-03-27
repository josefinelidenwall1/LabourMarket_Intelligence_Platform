import streamlit as st
import RAG.config as rag_config
from RAG.rag_main import run_hybrid_rag_pipeline

# -------------------------
# PAGE CONFIGURATION
# -------------------------
# Sets basic browser tab settings for the Streamlit app.
st.set_page_config(
    page_title="Sweden Labour Market Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# CACHED HELPERS
# -------------------------
# Cache static configuration values loaded from environment variables.
# st.cache_data is suitable here because the function returns serializable data
# that does not need to be recreated on every rerun.
@st.cache_data
def load_app_config():
    return rag_config.load_environment_variables()

# Cache the LLM client instance so it is created only once and then reused.
# st.cache_resource is used for long-lived objects such as database clients,
# API clients, or model connections that should persist across reruns.
@st.cache_resource
def get_llm_client():
    app_config = load_app_config()
    return rag_config.get_llm_client(app_config)

# Cache RAG query results for 10 minutes to avoid repeated expensive processing
# when the same question is asked again within a short time.
# show_spinner=False avoids showing a second spinner from the cache layer.
@st.cache_data(show_spinner=False, ttl=600)
def get_rag_result(user_question: str):
    return run_hybrid_rag_pipeline(user_question)

# Optional warm-up:
# Forces configuration loading and client initialization early when the app starts,
# so the first user interaction feels faster.
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
    /* ------------------------- */
    /* GLOBAL APP STYLING */
    /* ------------------------- */

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

    h1, h2, h3, h4, h5, h6,
    p, div, span, label {{
        color: {TEXT_COLOR};
    }}

    .stCaption {{
        color: {TEXT_COLOR} !important;
        opacity: 0.95;
    }}

    /* ------------------------- */
    /* SIDEBAR */
    /* ------------------------- */

    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG};
        border-right: 5px solid {DROPDOWN_BORDER};
        padding-top: 20px;
    }}

    section[data-testid="stSidebar"] * {{
        color: {TEXT_COLOR};
    }}

    /* ------------------------- */
    /* BUTTONS */
    /* ------------------------- */

    div.stButton > button {{
        background-color: {SIDEBAR_BG} !important;
        color: {TEXT_COLOR} !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
    }}

    div.stButton > button:hover {{
        background-color: {TEXT_COLOR} !important;
        color: {SIDEBAR_BG} !important;
        cursor: pointer !important;
    }}

    div.stButton > button:hover *,
    div.stButton > button:hover span,
    div.stButton > button:hover p {{
        color: {SIDEBAR_BG} !important;
    }}

    /* ------------------------- */
    /* TEXT AREA */
    /* ------------------------- */

    textarea {{
        background-color: {TEXT_COLOR} !important;
        color: {SIDEBAR_BG} !important;
        border: 2px solid {SIDEBAR_BG} !important;
        border-radius: 0 !important;
    }}

    /* ------------------------- */
    /* EXPANDERS / DEBUG DROPDOWNS */
    /* ------------------------- */

    div[data-testid="stExpander"] {{
        border: none !important;
        box-shadow: none !important;
        margin-top: 20px !important;
    }}

    div[data-testid="stExpander"] details {{
        background-color: transparent !important;
        border: none !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }}

    div[data-testid="stExpander"] summary {{
        background-color: {SIDEBAR_BG} !important;
        color: {TEXT_COLOR} !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary svg {{
        color: {TEXT_COLOR} !important;
        fill: {TEXT_COLOR} !important;
    }}

    div[data-testid="stExpander"] summary:hover {{
        background-color: {TEXT_COLOR} !important;
        color: {SIDEBAR_BG} !important;
        cursor: pointer !important;
    }}

    div[data-testid="stExpander"] summary:hover *,
    div[data-testid="stExpander"] summary:hover span,
    div[data-testid="stExpander"] summary:hover p,
    div[data-testid="stExpander"] summary:hover svg {{
        color: {SIDEBAR_BG} !important;
        fill: {SIDEBAR_BG} !important;
    }}

    div[data-testid="stExpander"] details[open] > summary {{
        background-color: {TEXT_COLOR} !important;
        color: {SIDEBAR_BG} !important;
        border-radius: 10px 10px 0 0 !important;
    }}

    div[data-testid="stExpander"] details[open] > summary *,
    div[data-testid="stExpander"] details[open] > summary span,
    div[data-testid="stExpander"] details[open] > summary p,
    div[data-testid="stExpander"] details[open] > summary svg {{
        color: {SIDEBAR_BG} !important;
        fill: {SIDEBAR_BG} !important;
    }}

    div[data-testid="stExpander"] details > div {{
        background-color: {TEXT_COLOR} !important;
        border: 2px solid {TEXT_COLOR} !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1rem !important;
    }}

    /* ------------------------- */
    /* JSON PREVIEW */
    /* ------------------------- */

    div[data-testid="stJson"],
    div[data-testid="stJson"] *,
    div[data-testid="stJson"] div,
    div[data-testid="stJson"] span,
    div[data-testid="stJson"] pre,
    div[data-testid="stJson"] code {{
        background-color: {TEXT_COLOR} !important;
        color: {SIDEBAR_BG} !important;
        border-color: {SIDEBAR_BG} !important;
    }}

    div[data-testid="stJson"] {{
        border: 2px solid {SIDEBAR_BG} !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
    }}

    div[data-testid="stJson"] svg,
    div[data-testid="stJson"] path {{
        fill: {SIDEBAR_BG} !important;
        stroke: {SIDEBAR_BG} !important;
    }}

    /* ------------------------- */
    /* RESPONSE BOX */
    /* ------------------------- */

    .response-box {{
        background-color: {TEXT_COLOR};
        border: 2px solid {SIDEBAR_BG};
        border-radius: 0;
        padding: 20px;
        margin-top: 10px;
        margin-bottom: 20px;
    }}

    .response-box,
    .response-box p,
    .response-box div,
    .response-box span,
    .response-box li,
    .response-box strong {{
        color: {SIDEBAR_BG} !important;
    }}

    .response-text {{
        font-size: 15px;
        line-height: 1.6;
        color: {SIDEBAR_BG} !important;
    }}

    /* ------------------------- */
    /* CUSTOM SQL BOX */
    /* ------------------------- */

    .sql-box {{
        background-color: {TEXT_COLOR} !important;
        border: 2px solid {SIDEBAR_BG} !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin-top: 10px !important;
        overflow-x: auto !important;
    }}

    .sql-box pre {{
        margin: 0 !important;
        background-color: {TEXT_COLOR} !important;
        color: {SIDEBAR_BG} !important;
        font-family: monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }}

    .sql-box,
    .sql-box * {{
        color: {SIDEBAR_BG} !important;
    }}
</style>
"""

# Inject custom CSS into the app.
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------
# Custom HTML is used here for more control over typography and spacing.
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
# MAIN PAGE CONTENT
# -------------------------

st.header("Steve 🤖 : *The AI Education Planning Assistant*")
st.caption(
    "Ask strategic questions about labour market trends and receive data-driven insights for university planning."
)

# Main user input field for natural-language questions.
user_question = st.text_area(
    "Ask a question about labour market trends",
    height=140,
    placeholder="Example: What kind of job descriptions or requirements are employers posting for software developers in Stockholm?"
)

# -------------------------
# GENERATE RESPONSE
# -------------------------
if st.button("Generate Insight"):
    # Prevent empty submissions.
    if not user_question.strip():
        st.warning("Please enter a question first.")
    else:
        # Show a spinner while the RAG pipeline is running.
        with st.spinner("Analyzing labour market data..."):
            try:
                # Run the cached RAG pipeline and collect returned components.
                result = get_rag_result(user_question)

                # Extract expected keys from the result dictionary with fallbacks.
                final_answer = result.get("final_answer", "No answer generated.")
                sql_query = result.get("sql_query", "")
                sql_preview = result.get("sql_data_preview", [])

                # Section heading for the generated answer.
                st.markdown("### Insight")

                # Styled answer box for the final natural-language response.
                st.markdown(
                    f"""
                    <div class="response-box">
                        <div class="response-text">{final_answer}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Debug dropdown showing the SQL query generated by the pipeline.
                with st.expander("Generated SQL"):
                    st.markdown(
                        f"""
                        <div class="sql-box">
                            <pre>{sql_query}</pre>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Debug dropdown showing the returned SQL preview data in JSON format.
                with st.expander("SQL Data Preview"):
                    st.json(sql_preview)

            except Exception as e:
                # Fallback error handling shown in the UI if anything fails.
                st.error(f"Something went wrong: {e}")