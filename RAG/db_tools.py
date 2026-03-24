import re
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

def is_safe_sql_query(sql_query: str) -> bool:
    """Security Layer 2: Python Middleware Sanitization to block DML/DDL."""
    query_lower = sql_query.lower()
    
    # Deny sql queries with transforming actions 
    forbidden_keywords = [
        r"\bdrop\b", r"\bdelete\b", r"\bupdate\b", r"\binsert\b", 
        r"\balter\b", r"\btruncate\b", r"\bgrant\b", r"\brevoke\b", 
        r"\breplace\b", r"\bmerge\b", r"\bcreate\b"
    ]
    
    for keyword in forbidden_keywords:
        if re.search(keyword, query_lower):
            print(f"SECURITY ALERT: Blocked unauthorized SQL keyword: {keyword}")
            return False
            
    if not query_lower.strip().startswith("select"):
        print("SECURITY ALERT: Query does not start with SELECT.")
        return False
        
    return True

def execute_databricks_sql(query: str, config: dict) -> list:
    """Executes validated SQL against the Databricks SQL warehouse using OAuth M2M."""
    if not is_safe_sql_query(query):
        return [{"error": "Query rejected due to security constraints. Only SELECT is allowed."}]

    def get_credential_provider():
        cfg = Config(
            host=f"https://{config['db_host']}",
            client_id=config['db_client_id'].strip(),
            client_secret=config['db_client_secret'].strip()
        )
        return oauth_service_principal(cfg)

    try:
        with sql.connect(
            server_hostname=config["db_host"],
            http_path=config["db_path"],
            credentials_provider=get_credential_provider
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return [row.asDict() for row in result]
    except Exception as e:
        print(f"SQL Execution Error: {e}")
        return [{"error": str(e)}]

def retrieve_job_ad_text_context(question: str, llm_client, config: dict) -> str:
    """Retrieves qualitative text from the new Gold RAG table using Keyword Search."""
    
    # Ask the LLM to extract the best search term from the user's question
    keyword_prompt = f"Extract a single, broad Swedish keyword or occupation from this question for a database text search: '{question}'. Return ONLY the keyword, nothing else."
    
    try:
        response = llm_client.chat.completions.create(
            model=config["oai_deployment"],
            messages=[{"role": "user", "content": keyword_prompt}],
            temperature=0
        )
        search_keyword = response.choices[0].message.content.strip().replace("'", "")
        print(f"DEBUG - Extracted Search Keyword: {search_keyword}")
    except Exception as e:
        print(f"Keyword Extraction Error: {e}")
        return "Qualitative job data unavailable."

    # Construct the SQL Full-Text Search
    text_query = f"""
        SELECT job_title, employer_name, city, document_text 
        FROM gold_rag.job_ads_documents_enriched
        WHERE document_text ILIKE '%{search_keyword}%'
        LIMIT 3
    """
    
    # Execute and format the results
    results = execute_databricks_sql(text_query, config)
    
    if results and "error" not in results[0]:
        context_docs = []
        for row in results:
            # Truncate the document_text to 1000 characters so we don't blow up the LLM context window
            doc_snippet = str(row.get("document_text", ""))[:1000]
            context_docs.append(
                f"Job: {row.get('job_title')} at {row.get('employer_name')} in {row.get('city')}\n"
                f"Details: {doc_snippet}..."
            )
        return "\n\n".join(context_docs)
    else:
        print(f"Text Retrieval Error: {results[0].get('error') if results else 'None'}")
        return "Qualitative job data unavailable."