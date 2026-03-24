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

    /* Selectbox container */
    div[data-baseweb="select"] > div {
    background-color: #355C46 !important;
    border: 1px solid #E6C3A5 !important;
    border-radius: 10px;
    }

    /* Selected value text */
    div[data-baseweb="select"] span {
    color: #F7E9DC !important;
    }

    /* Dropdown arrow */
    div[data-baseweb="select"] svg {
    fill: #F7E9DC !important;
    }

    /* Dropdown menu (when opened) */
    ul[role="listbox"] {
    background-color: #355C46 !important;
    border: 1px solid #E6C3A5 !important;
    }

    /* Dropdown options */
    li[role="option"] {
    color: #F7E9DC !important;
    }

    /* Hover effect on options */
    li[role="option"]:hover {
    background-color: rgba(127, 167, 154, 0.2) !important;
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

    /* =========================
    SELECTBOX (Dropdown)
    ========================= */

    /* Main selectbox container */
    div[data-baseweb="select"] > div {
    background-color: #355C46 !important;
    border: 2px solid #E6C3A5 !important;
    border-radius: 10px;
    cursor: pointer !important;  /* show pointer on hover */
    }

    /* Text inside selectbox */
    div[data-baseweb="select"] span {
    color: #F7E9DC !important;
    }

    /* Arrow icon */
    div[data-baseweb="select"] svg {
    fill: #F7E9DC !important;
    }

    /* Inner input fix */
    div[data-baseweb="select"] input {
    background-color: #355C46 !important;
    color: #F7E9DC !important;
    cursor: pointer !important;  /* pointer over input area too */
    }

    /* Make the whole selectbox area feel clickable */
    div[data-baseweb="select"] * {
    cursor: pointer !important;
    }

    /* =========================
    DROPDOWN MENU (expanded)
    ========================= */

    /* Entire dropdown panel */
    ul[role="listbox"] {
    background-color: #355C46 !important;
    border: 2px solid #E6C3A5 !important;
    border-radius: 10px;
    padding: 5px;
    }

    /* Each option */
    li[role="option"] {
    color: #F7E9DC !important;
    background-color: #355C46 !important;
    border-radius: 0px !important;;
    cursor: pointer !important;
    }

    /* Hover effect removed: keep same appearance */
    li[role="option"]:hover {
    background-color: #355C46 !important;
    color: #F7E9DC !important;
    }

    /* Selected option also keeps same appearance */
    li[aria-selected="true"] {
    background-color: #355C46 !important;
    color: #F7E9DC !important;
    }

    /* =========================
    DROPDOWN OUTER CONTAINER
    ========================= */

    /* BaseWeb popover (this is the outer wrapper causing the grey/white look) */
    div[data-baseweb="popover"] {
    background-color: transparent !important;
    }

    /* Inner container of dropdown */
    div[data-baseweb="popover"] > div {
    background-color: #355C46 !important;
    border: 2px solid #E6C3A5 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
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

# st.caption("Supporting university program planning through real-time labour market intelligence")

# Page routing logic
# Based on what user selects in sidebar, show different content

if menu == "Labour Market Analytics":
    # Page title and short explanation
    st.header("Labour Market Analytics")
    st.caption(
        "Explore regional labour demand patterns to support university planning and program expansion."
    )

    # ---------------------------
    # Filters section
    # ---------------------------
    # These are placeholder filters for now.
    # Later, they can be connected to real data and query logic.
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        region = st.selectbox(
            "Region",
            ["All", "Stockholm", "Västra Götaland", "Skåne"]
        )

    with col2:
        occupation_field = st.selectbox(
            "Occupation Field",
            ["All", "Data/IT", "Healthcare", "Education", "Engineering"]
        )

    with col3:
        occupation_group = st.selectbox(
            "Occupation Group",
            ["All", "Software Developers", "Nurses", "Teachers", "Technicians"]
        )

    with col4:
        year = st.selectbox(
            "Year",
            ["All", "2022", "2023", "2024", "2025"]
        )

    # ---------------------------
    # KPI section
    # ---------------------------
    st.markdown("### Key Indicators")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric("Total Demand Signals", "6.75M")

    with kpi2:
        st.metric("Leading Region", "Stockholm")

    with kpi3:
        st.metric("Top Occupation Group", "Software Developers")

    with kpi4:
        st.metric("Top Occupation Field", "Data/IT")

    # ---------------------------
    # Chart section
    # ---------------------------
    # These are placeholder charts for layout purposes.
    # We will replace them with real data later.
    st.markdown("### Market Signals")

    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("Regional Demand Hotspots")
        st.bar_chart({
            "Demand": [120, 95, 78, 65, 50]
        })

    with chart2:
        st.subheader("Priority Occupation Areas")
        st.bar_chart({
            "Demand": [140, 110, 85, 70, 60]
        })

    # ---------------------------
    # Insight cards section
    # ---------------------------
    st.markdown("### Planning Insights for Universities")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">Region to Watch</div>
                <div class="insight-text">
                    Västra Götaland shows sustained labour demand across technical and industrial roles,
                    indicating strong regional planning relevance.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">Emerging Talent Need</div>
                <div class="insight-text">
                    Data and engineering-related occupations continue to show strong demand signals,
                    suggesting future pressure on regional talent pipelines.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-title">Potential Program Opportunity</div>
                <div class="insight-text">
                    Universities may want to assess whether current program capacity aligns with growing
                    employer demand in IT and engineering fields.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

elif menu == "AI Planning Assistant":
    # This is the AI Assistant page
    st.header("AI Planning Assistant")