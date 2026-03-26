"""
schema_dictionary.py
====================
Authoritative table/schema dictionary for the labour_market_platform Gold layer.
Drop this string directly into the system prompt of the SQL-generation agent.

Two schemas are defined:
  - labour_market_platform.gold_analysis  ->  structured analytical tables (star schema)
  - labour_market_platform.gold_rag       ->  job-ad documents for vector / RAG retrieval

Usage:
    from schema_dictionary import TABLE_SCHEMA_PROMPT
    # paste TABLE_SCHEMA_PROMPT into the system prompt of generate_sql_query()
"""

TABLE_SCHEMA_PROMPT = """
=======================================================================
DATABASE SCHEMA  -  labour_market_platform  (Databricks Delta Lake)
=======================================================================
ALWAYS qualify EVERY table name with its full three-part identifier:
  <catalog>.<schema>.<table>
  e.g.  labour_market_platform.gold_analysis.fact_wages

Two schemas exist:
  - gold_analysis  - star-schema tables for quantitative analysis
  - gold_rag       - document tables for semantic / vector retrieval

-----------------------------------------------------------------------
SCHEMA: gold_analysis
-----------------------------------------------------------------------
Purpose: Swedish labour-market analytics built from AF (Arbetsförmedlingen),
        SCB (Statistics Sweden), and UKÄ/YH (higher education) sources.
Dialect: Databricks SQL (Delta Lake). Date keys are DATE type.

── DIMENSION TABLES ────────────────────────────────────────────────────

TABLE: labour_market_platform.gold_analysis.dim_occupation
  Purpose : Maps individual SSYK 2012 occupation codes to job-tech labels.
            Use this table when the question targets a SPECIFIC occupation
            code (4-digit SSYK) rather than a broad major group.
  Grain   : One row per unique SSYK occupation code.
  Columns :
    occupation_id             STRING  - surrogate primary key
    ssyk_code                 STRING  - 4-digit SSYK 2012 occupation code
                                        (e.g. '2512' for Software Developers)
    ssyk_name                 STRING  - Swedish occupation name
                                        (e.g. 'Systemutvecklare och programmerare')
    jobtech_occupation_group_label STRING - Arbetsförmedlingen group label used
                                          to join with fact_job_postings
  Join hints:
    -> fact_wages          ON occupation_id = fact_wages.occupation_id
    -> fact_job_postings   ON occupation_id = fact_job_postings.occupation_id
  NOTE: dim_occupation and dim_occupation_major_group serve DIFFERENT
    fact tables. Do NOT mix them.

TABLE: labour_market_platform.gold_analysis.dim_occupation_major_group
  Purpose : Broad SSYK major groups (1-digit). Used exclusively with
            fact_employment (SCB AKU data).
  Grain   : One row per major group.
  Columns :
    occupation_major_group_id   INT     - surrogate primary key
    occupation_code             STRING  - 1-digit SSYK major-group code
                                          or special code ('0000', '0002')
    occupation_group_name       STRING  - English label for the major group
  VALID VALUES for occupation_group_name:
    'armed forces'                    (code '0')
    'managers'                        (code '1')
    'advanced higher education'       (code '2')  <- use for "professionals / major group 2"
    'higher education'                (code '3')
    'administration and customer service' (code '4')
    'service, care and sales'         (code '5')
    'agricultural and forestry'       (code '6')
    'building and manufacturing'      (code '7')
    'mechanical manufacturing and transport' (code '8')
    'elementary occupations'          (code '9')
    'all occupations'                 (code '0000')
    'unidentifiable'                  (code '0002')
  Join hints:
    -> fact_employment  ON occupation_major_group_id = fact_employment.occupation_major_group_id
  NOTE: This table does NOT join to fact_wages or fact_job_postings.

TABLE: labour_market_platform.gold_analysis.dim_date
  Purpose : Calendar dimension. Date keys are stored as DATE (YYYY-MM-DD).
            Wage and employment rows use the first day of the year
            (e.g. '2022-01-01'). Job-posting rows use the exact publication date.
  Grain   : One row per calendar day.
  Columns :
    date_id       DATE    - primary key  (e.g. DATE '2022-01-01')
    year          INT     - calendar year
    month         INT     - calendar month (1-12)
    quarter       INT     - calendar quarter (1-4)
    week          INT     - ISO week number
    day_of_week   STRING  - full weekday name (e.g. 'Monday')
  Usage pattern:
    For yearly aggregations: GROUP BY d.year
    For monthly:             GROUP BY d.year, d.month
  NOTE: All fact tables contain MULTIPLE years of historical data.
    NEVER SUM across all years when computing a "current" total.
    Always filter to MAX(year) or a specific year.

TABLE: labour_market_platform.gold_analysis.dim_location
  Purpose : Geographic dimension combining municipality and county (region/län).
            Source: job-posting municipality codes + education region names.
  Grain   : One row per unique (municipality_code, region_name) combination.
            Rows sourced from education data may have NULL municipality fields.
  Columns :
    location_id        INT     - surrogate primary key
    municipality_name  STRING  - Swedish municipality name (e.g. 'Stockholm')
                                NULL for education-only location rows
    municipality_code  STRING  - 4-digit SCB municipality code (e.g. '0180')
                                NULL for education-only location rows
    region_name        STRING  - Swedish county / region name (e.g. 'Stockholms län')
  Join hints:
    -> fact_job_postings        ON location_id = fact_job_postings.location_id
    -> fact_education_graduates ON location_id = fact_education_graduates.location_id
  GUARDRAIL: fact_wages contains NATIONAL averages only.
    NEVER join dim_location to fact_wages.
    NEVER filter fact_wages by city, municipality, or county.

TABLE: labour_market_platform.gold_analysis.dim_gender
  Purpose : Gender / demographic dimension.
  Grain   : One row per gender value.
  Columns :
    gender_id         INT     - surrogate primary key
    gender_name       STRING  - gender label (see valid values below)
    is_actual_gender  BOOLEAN - TRUE for 'men'/'women', FALSE for 'total'
  VALID VALUES for gender_name:
    'men'     (gender_id = 1)
    'women'   (gender_id = 2)
    'total'   (gender_id = 3)  <- aggregate row; see aggregation rules below
  AGGREGATION RULE: Do NOT filter gender_name = 'total' to get an
    overall figure. That row may be unreliable or absent. To get an
    overall total or average across all people, OMIT dim_gender from
    the query entirely and let SQL aggregate naturally with SUM()/AVG().

── FACT TABLES ─────────────────────────────────────────────────────────

TABLE: labour_market_platform.gold_analysis.fact_wages
  Purpose : Annual average wages by occupation, gender, and sector.
            Source: SCB wages survey.
  Grain   : One row per (year x occupation x gender x sector).
            Date key maps each year to YYYY-01-01.
  Columns :
    date_id             DATE    - FK -> dim_date.date_id
    occupation_id       STRING  - FK -> dim_occupation.occupation_id
                                  (maps through dim_occupation SSYK codes)
    gender_id           INT     - FK -> dim_gender.gender_id
    sector              STRING  - sector label (stored as plain string, not FK)
  VALID VALUES for sector:
    'Statlig'    - central government
    'Kommunal'   - municipal government
    'Region'     - regional government (healthcare/county councils)
    'Privat'     - private sector
    monthly_salary_avg  DOUBLE  - average gross monthly salary (SEK)
  GUARDRAILS:
    1. NATIONAL averages only. NEVER join to dim_location or filter by geography.
    2. Contains multiple years. Filter to the most recent year when asking for
      "current" salaries: use MAX(d.year) subquery or explicit year filter.
    3. When comparing genders, join dim_gender and filter gender_name IN ('men','women').
  Example question -> pattern:
    "Average salary for software developers"
    -> JOIN dim_occupation ON ssyk_code = '2512'
    -> filter to MAX(year)
    -> AVG(monthly_salary_avg)

TABLE: labour_market_platform.gold_analysis.fact_employment
  Purpose : Annual employment headcounts by broad occupation group and gender.
            Source: SCB AKU (Labour Force Survey).
  Grain   : One row per (year x occupation_major_group x gender).
            Date key maps each year to YYYY-01-01.
  Columns :
    date_id                   DATE   - FK -> dim_date.date_id
    occupation_major_group_id INT    - FK -> dim_occupation_major_group.occupation_major_group_id
    gender_id                 INT    - FK -> dim_gender.gender_id
    employed_thousands        DOUBLE - number of employed people in thousands
  GUARDRAILS:
    1. Uses dim_occupation_major_group, NOT dim_occupation or dim_location.
    2. Contains multiple years. Filter to MAX(year) for "current" employment.
    3. Do not sum across all years.

TABLE: labour_market_platform.gold_analysis.fact_job_postings
  Purpose : Individual job-ad postings with occupational and geographic detail.
            Source: Arbetsförmedlingen (AF) Jobtech API.
  Grain   : One row per job posting.
  Columns :
    job_id                STRING  - natural primary key (unique per posting)
    occupation_id         STRING  - FK -> dim_occupation.occupation_id
    location_id           INT     - FK -> dim_location.location_id
    date_id               DATE    - FK -> dim_date.date_id (publication date)
    number_of_vacancies   INT     - number of open positions in the ad
    scope_of_work_min     INT     - minimum work scope % (e.g. 50)
    scope_of_work_max     INT     - maximum work scope % (e.g. 100)
    application_deadline  TIMESTAMP
    employment_type_label STRING  - e.g. 'Vanlig anställning'
    duration_label        STRING  - e.g. 'Tillsvidareanställning', 'Tillfällig anställning'
    working_hours_type_label STRING - e.g. 'Heltid', 'Deltid'
  Useful for: demand trends by occupation/location, time-series of postings,
              full-time vs part-time split, geographic demand hotspots.

TABLE: labour_market_platform.gold_analysis.fact_education_graduates
  Purpose : Graduate / student counts from university (UKÄ) and
            vocational higher education (YH) programmes.
  Grain   : One row per (year x institution x subject x gender x location).
  Columns :
    date_id              DATE    - FK -> dim_date.date_id (YYYY-01-01)
    institution          STRING  - university or YH school name
    subject              STRING  - study subject or programme direction
    gender_id            INT     - FK -> dim_gender.gender_id
    location_id          INT     - FK -> dim_location.location_id (region level)
    student_count        INT     - number of students / graduates
    program_not_offered  BOOLEAN - TRUE if the programme was not offered that year (YH rows)
  Useful for: talent pipeline analysis, supply-side education trends,
              gender balance in study programmes.

-----------------------------------------------------------------------
SCHEMA: gold_rag
-----------------------------------------------------------------------
Purpose : Job-advertisement documents prepared for RAG retrieval.
          Used by the pipeline to retrieve qualitative job-ad context.

TABLE: labour_market_platform.gold_rag.job_ads_documents
  Purpose : Base cleaned job ads extracted from silver layer.
  Grain   : One row per unique job posting (job_id).
  Columns :
    job_id                       STRING
    job_title                    STRING
    employer_name                STRING
    occupation_label             STRING  - fine-grained occupation
    occupation_field_label       STRING  - broad occupation field
    occupation_group_label       STRING  - occupation group
    municipality_code            STRING
    city                         STRING
    publication_date             TIMESTAMP
    last_publication_date        TIMESTAMP
    application_deadline         TIMESTAMP
    removed_date                 TIMESTAMP
    employment_type_label        STRING
    duration_label               STRING
    working_hours_type_label     STRING
    salary_type_label            STRING
    scope_of_work_min            INT
    scope_of_work_max            INT
    number_of_vacancies          INT
    removed                      BOOLEAN
    webpage_url                  STRING
    record_source                STRING
    description_text             STRING  - main job description
    description_requirements     STRING  - required qualifications
    description_conditions       STRING  - working conditions
    description_company_information STRING - employer background
    description_needs            STRING  - what the employer needs

TABLE: labour_market_platform.gold_rag.job_ads_documents_enriched
  Purpose : Enriched version with a single concatenated document_text field.
            Inherits all columns from job_ads_documents plus the derived field below.
  Additional column :
    document_text  STRING  - concatenated plain-text document combining job title,
                            employer, occupation, location, employment details, and
                            all description sub-fields.

=======================================================================
CROSS-SCHEMA RELATIONSHIP SUMMARY
=======================================================================
dim_occupation           <-->  fact_wages           (occupation_id)
dim_occupation           <-->  fact_job_postings    (occupation_id)
dim_occupation_major_group <--> fact_employment      (occupation_major_group_id)
dim_date                 <-->  ALL fact tables       (date_id)
dim_location             <-->  fact_job_postings     (location_id)
dim_location             <-->  fact_education_graduates (location_id)
dim_gender               <-->  fact_wages            (gender_id)
dim_gender               <-->  fact_employment       (gender_id)
dim_gender               <-->  fact_education_graduates (gender_id)
gold_rag tables are STANDALONE - no foreign keys to gold_analysis.

=======================================================================
GLOBAL QUERY RULES (apply to every generated SQL statement)
=======================================================================
1. CATALOG PREFIX    : Every table reference must be fully qualified:
                      labour_market_platform.<schema>.<table>

2. TIME-SERIES GUARD : All fact tables span multiple years. Never SUM
                      across all years for "current" totals. Always
                      dynamically determine the most recent year:
                        WHERE d.year = (SELECT MAX(year) FROM
                          labour_market_platform.gold_analysis.dim_date
                          WHERE date_id IN (SELECT date_id FROM <fact_table>))

3. GEOGRAPHY GUARD   : fact_wages = national data only.
                      Never join fact_wages to dim_location.
                      Never filter fact_wages by city/municipality/county.

4. GENDER AGGREGATION: To get an overall total/average across all genders,
                      OMIT dim_gender from the query. Do not rely on
                      gender_name = 'total'.

5. OCCUPATION ROUTING:
                      - Specific SSYK code question -> use dim_occupation
                      - Broad major-group question   -> use dim_occupation_major_group
                      - Job postings / demand        -> use dim_occupation + fact_job_postings

6. DML FORBIDDEN     : Generate SELECT statements only. Never produce
                      DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE,
                      GRANT, REVOKE, REPLACE, MERGE, or CREATE.

7. DIALECT           : Databricks SQL. Use standard ANSI SQL functions.

8. HYBRID RAG (TEXT SAMPLES & SKILLS): When the user asks for qualitative data (skills, requirements, descriptions) to design educational programs:
  - You MUST query `labour_market_platform.gold_rag.job_ads_documents_enriched`.
  - NEVER filter by English occupation names in string columns. The database labels are in SWEDISH.
  - Translate the English occupation to Swedish (e.g. "software developer" -> "systemutvecklare" or "programmerare") and search the `document_text` column using `ILIKE`.
  - Select the `job_title`, `employer_name`, `city`, and `document_text`.
  - ALWAYS append `LIMIT 10` to prevent massive data payloads. 
  Example pattern:
  SELECT 
    job_title, employer_name, city, document_text 
  FROM labour_market_platform.gold_rag.job_ads_documents_enriched 
  WHERE document_text ILIKE '%systemutvecklare%' AND city = 'Stockholm'
  LIMIT 10;
=======================================================================
"""

if __name__ == "__main__":
    print(TABLE_SCHEMA_PROMPT)
    print(f"\n--- Schema prompt length: {len(TABLE_SCHEMA_PROMPT)} characters ---")