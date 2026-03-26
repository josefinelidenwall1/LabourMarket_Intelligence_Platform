import json
from openai import AzureOpenAI
from .schema_dictionary import TABLE_SCHEMA_PROMPT

def generate_sql_query(question: str, client: AzureOpenAI, config: dict) -> str:
    system_prompt = TABLE_SCHEMA_PROMPT
    
    try:
        response = client.chat.completions.create(
            model=config["oai_deployment"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a Databricks SQL query for this question without transforming the data: {question}"}
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
    You are an expert Swedish labor market advisor helping students make informed 
    decisions about their education and career paths.

    Your goal is to help students identify which courses, programs, or skills are 
    most relevant based on current job market demand — so they can invest their 
    time and money wisely.

    Use the provided labor market data to answer the student's question clearly 
    and practically. The data may include:
    - Quantitative metrics (e.g., number of job openings, average salaries, employment rates by field)
    - Qualitative text samples from real job advertisements

    When qualitative text is present:
    - Extract specific skills, tools, software, certifications, and soft skills that employers are actively requesting
    - Explain in plain language what these mean for the student's education choices
    - Highlight which courses or subjects would directly prepare them for these roles

    Always frame your advice around the student's perspective:
    - What is likely to lead to employment?
    - Which skills are in high demand right now?
    - Are there any gaps between what schools typically teach and what employers want?

    If the data is insufficient to answer the student's question, clearly state 
    what information is missing and suggest what the student could research further.

    Keep your language accessible, encouraging, and actionable — students may be 
    at different stages of their education journey and need clear, honest guidance.
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