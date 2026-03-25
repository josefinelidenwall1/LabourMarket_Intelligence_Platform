import json
from openai import AzureOpenAI
from schema_dictionary import TABLE_SCHEMA_PROMPT

def generate_sql_query(question: str, client: AzureOpenAI, config: dict) -> str:
    system_prompt = TABLE_SCHEMA_PROMPT
    
    try:
        response = client.chat.completions.create(
            model=config["oai_deployment"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a Databricks SQL query for this question: {question}"}
            ],
            temperature=0
        )
        
        raw_sql = response.choices[0].message.content.strip()
        if raw_sql.startswith("```sql"):
            raw_sql = raw_sql[6:]
        if raw_sql.endswith("```"):
            raw_sql = raw_sql[:-3]
            
        return raw_sql.strip()
    except Exception as e:
        print(f"LLM SQL Generation Error: {e}")
        return ""

def generate_final_synthesis(question: str, sql_data: list, client: AzureOpenAI, config: dict) -> str:
    system_prompt = """
    You are an expert Swedish labor market advisor assisting education leaders and program directors.
    Your goal is to help them design educational programs that match current market demand.
    
    Use the provided Databricks SQL data to answer the user's question comprehensively. 
    The data may contain quantitative metrics (e.g., employment counts, average salaries) AND qualitative text samples from real job advertisements.
    
    When qualitative text is present, extract and highlight specific skills, software, certifications, and soft skills that employers are requesting. Translate these into actionable curriculum advice.
    If data is insufficient, state what is missing.
    """
    
    user_message = f"""
    User Question: {question}
    
    Databricks Database Results (Metrics & Sample Job Ads):
    {json.dumps(sql_data, indent=2)}
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
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Final Synthesis Error: {e}")
        return "I am currently unable to synthesize the final answer."