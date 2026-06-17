# LabourMarket Intelligence Platform

## 👥 Project Team
* **Context:** Final project at `</Salt>`
* **Team Members:** Josefine Lidenwall, Fariba Kamani and Juaquin Rehnberg

---

## 🎯 What the Platform Does (Business Value)
We built this platform to answer two questions for Swedish universities and educational planners:
1. **Market Trends:** Which fields of study match real labor market growth, and which ones risk producing too many graduates for shrinking industries?
2. **The Talent Gap:** Where are the exact mismatches between what universities teach and what employers actually look for?

---

## 🏗️ Data Engineering & Architecture

### 1. Data Sources
We integrated official datasets from three primary national sources:
* **Job Postings:** Active and historical vacancies and hiring data from **Arbetsförmedlingen**.
* **Labor Market Baseline:** Employment rates and average salary data from **SCB** (Statistics Sweden).
* **Education Pipelines:** Graduate volumes and university metrics from **UKÄ** (Swedish Higher Education Authority).

### 2. The Data Pipeline 
We processed the data using an ELT workflow structured around a **Medallion Architecture** (Bronze → Silver → Gold). This pipeline creates two distinct Gold layers to serve our downstream applications:

* **Orchestration:** **Azure Data Factory (ADF)** manages the entire end-to-end workflow, triggering **Databricks Notebooks** to run the heavy data transformations.
* **The Analytics Gold Layer:** A clean star-schema model engineered specifically to power the Power BI report.
* **The AI Gold Layer:** Structured data optimized for a **RAG (Retrieval-Augmented Generation) AI engine**. This allows users to ask questions in plain text through a custom **Streamlit** frontend, which translates the input into SQL queries against the database and returns the answer in natural language.

---

## 💾 Data Modeling Challenges
To allow our education and job posting tables to cross-reference accurately, we designed a unified Star Schema that addresses several data integration hurdles:

* **The Problems:**
  * **Unstructured Job Titles:** Job ads rely on free-text, non-standardized titles, whereas SCB and Arbetsförmedlingen use strict occupational codes at varying levels of granularity (broad groups vs. specific occupations).
  * **Mismatched Education Frameworks:** Education data uses completely different subject categories depending on whether it comes from traditional universities or **Yrkeshögskolan** (higher vocational education), making direct comparisons difficult.
  * **Geographic Discrepancies:** Location data from Arbetsförmedlingen and UKÄ mapped to different regional levels—some recorded at the municipality (*kommun*) level and others at the county (*län*) level.
* **Our Solution:**
  * We separated aggregate employment data into a higher-level table (`dim_occupation_major_group`) while maintaining granular job posting details in a specific occupational dimension (`dim_occupation_ssyk`). 
  * We built a geographic mapping table to normalize municipalities into their respective counties. This standardizes the location data across the board, enabling clean labor market and education comparisons for every *län* in Sweden.

---

## 📊 Dashboard & Analytics Overview
The Power BI report breaks down the insights into three core pages:

* **Page 1: National Market Overview:** Shows the big picture of the Swedish economy, overall vacancy numbers, and which sectors have the most hiring momentum.
* **Page 2: Regional Demand & Wage Dynamics:** Highlights how local economies differ (like comparing Stockholm to the industrial boom in northern Sweden). It features an interactive map tied directly to a "Top Regions" summary table underneath it.
* **Page 3: The Talent Gap (Market Mirror):** Uses a split-screen design that places university graduate numbers directly opposite active job vacancies. By comparing percentages (like a sector's share of graduates vs. its share of jobs) rather than raw totals, we can spotlight market mismatches even though the tables aren't directly joined on the backend.

---

## 🛡️ Security & Automation

| Pillar | How It's Set Up |
| :--- | :--- |
| **Security** | • **RBAC:** Role-Based Access Control keeps data access restricted and secure.<br>• **Managed Identity & Service Principals:** No dangerous, long-lived passwords saved in the code across Azure and Databricks.<br>• **Environment Variables:** Keeps sensitive keys and connection strings safely hidden away. |
| **Automation** | • **Sunday at 10:00:** Automated pipeline pulls in fresh job ads.<br>• **Every 4 Weeks:** Deep historical data updates are pulled.<br>• **Daily at 16:00:** Azure Data Factory triggers Databricks notebooks to clean and transform the data into the Gold layer.<br>• **Daily at 18:00:** The Power BI Service automatically refreshes the semantic model right after the data pipeline finishes running. |

---

## 🚀 Future Improvements
1. **Predictive Analysis:** Build machine learning models to forecast what skills will be missing 3 to 5 years from now.
2. **More Job Data:** Connect to extra job sources (like the LinkedIn API) to capture tech and corporate hiring trends.
3. **Better Data for the AI:** Refine the Gold layer structure to support advanced text embeddings for cleaner RAG chatbot answers.
4. **All-in-One App:** Embed the interactive Power BI dashboard directly into our Streamlit web app interface.
