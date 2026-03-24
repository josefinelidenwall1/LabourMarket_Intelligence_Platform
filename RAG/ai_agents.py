import json
from openai import AzureOpenAI

def generate_text_embedding(text: str, client: AzureOpenAI, config: dict) -> list[float]:
    """
    Takes a string of text and uses text-embedding-ada-002 to convert it 
    into a mathematical vector array.
    """
    try:
        response = client.embeddings.create(
            input=text,
            model=config["oai_embedding"]
        )
        return response.data[0].embedding
    
    except Exception as e:
        print(f"Embedding Generation Error: {e}")
        return []

def generate_sql_query(question: str, client: AzureOpenAI, config: dict) -> str:
    table_schema = """
    1. dim_occupation
    - Columns: occupation_id (STRING), ssyk_code (STRING), ssyk_name (STRING), jobtech_occupation_group_label (STRING)

    2. dim_date
    - Columns: date_id (STRING), year (INT), month (INT)

    3. dim_location
    - Columns: location_id (STRING), municipality_code (STRING), municipality_name (STRING), county_name (STRING)

    4. dim_occupation_major_group
    - Columns: occupation_major_group_id (STRING), occupation_group_name (STRING)
    - VALID VALUES for occupation_group_name (SSYK 2012): 
        'Chefer', 'Yrkesarbete med krav på fördjupad högskolekompetens' (Use this for Professionals/Major Group 2), 'Yrkesarbete med krav på högskolekompetens eller motsvarande', 'Administrativt och kundtjänstarbete', 'Service-, omsorgs- och försäljningsarbete', 'Arbete inom jordbruk, trädgård, skogsbruk och fiske', 'Hantverksarbete inom byggverksamhet och tillverkning', 'Maskinoperatörs- och monteringsarbete, samt transportarbetare', 'Yrken med krav på kortare utbildning eller introduktion'

    5. dim_gender
    - Columns: gender_id (STRING), gender_name (STRING)
    - VALID VALUES for gender_name: 'Män', 'Kvinnor', 'Totalt'

    6. dim_sector
    - Columns: sector_id (STRING), sector_name (STRING)
    - VALID VALUES for sector_name: 'Statlig', 'Kommunal', 'Region', 'Privat'

    7. fact_wages
    - Columns: date_id, occupation_id, sector_id, gender_id, age_group_id, monthly_salary_avg, women_salary, men_salary
    - GUARDRAILS: 
        * This table contains NATIONAL averages only. 
        * NEVER attempt to join this table to dim_location. 
        * NEVER filter this table by city, municipality, or county.

    8. fact_employment
    - Columns: date_id, occupation_major_group_id, gender_id, employed_thousands
"""
    
    system_prompt = f"""
    You are an expert Databricks SQL developer querying a Swedish labor market database.
    You MUST ALWAYS prepend the catalog and schema to EVERY table name: `labour_market_platform.gold_analysis.[table_name]`.
    
    CRITICAL RULES:
    1. NEVER hallucinate or invent columns. ONLY use the exact columns listed in the schema below.
    2. If a table's schema says it does not support geographic filtering (like fact_wages), DO NOT try to join it to a location table or filter by city.
    3. Use the EXACT Swedish "VALID VALUES" provided in the schema when filtering. Translate English concepts (like "Professionals") to the provided Swedish valid values.
    
    DATA MODELING & AGGREGATION RULES:
    1. Time-Series Double Counting: All fact tables contain multiple years of historical data. If calculating "current" totals, NEVER sum across all years. You must dynamically filter your query to the most recent year that contains actual data for your target metric.
    2. Demographic Aggregation: Do not explicitly filter for `gender_name = 'Totalt'` to get an overall number. That row may not exist. To get an overall total or average across all people, simply OMIT the demographic dimension (e.g., dim_gender) from your query entirely and let SQL naturally aggregate the base rows using SUM() or AVG().
    
    SCHEMA:
    {table_schema}
    
    Return ONLY valid Databricks SQL code. Do not include markdown formatting like ```sql.
    """
    
    try:
        response = client.chat.completions.create(
            model=config["oai_deployment"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a SQL query to answer: {question}"}
            ],
            temperature=0
        )
        # Strip markdown if the LLM ignores the prompt
        raw_sql = response.choices[0].message.content.strip()
        if raw_sql.startswith("```sql"):
            raw_sql = raw_sql[6:]
        if raw_sql.endswith("```"):
            raw_sql = raw_sql[:-3]
        return raw_sql.strip()
    except Exception as e:
        print(f"LLM SQL Generation Error: {e}")
        return ""

def generate_final_synthesis(question: str, sql_data: list, text_context: str, client: AzureOpenAI, config: dict) -> str:
    system_prompt = """
    You are an expert Swedish labor market advisor.
    Use the provided quantitative labor market data (salaries, employment counts) and qualitative job advertisement context (real job ads) to answer the user's question comprehensively. 
    If data is insufficient, state what is missing. Provide an informed, strategic overview.
    """
    
    user_message = f"""
    User Question: {question}
    
    Quantitative Labor Market Data (from SQL query):
    {json.dumps(sql_data, indent=2)}
    
    Qualitative Job Ads Context (from gold_rag table):
    {text_context}
    """
    
    try:
        response = client.chat.completions.create(
            model=config["oai_deployment"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Synthesis Error: {e}")
        return "Sorry, I encountered an error generating the final answer."