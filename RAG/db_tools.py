import re
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

def is_safe_sql_query(sql_query: str) -> bool:
    query_lower = sql_query.lower()
    
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
    if not is_safe_sql_query(query):
        return [{"error": "Query rejected due to security constraints. Only SELECT is allowed."}]

    try:
        def get_credentials():
            cfg = Config(
                host=f"https://{config['db_host']}",
                client_id=config['db_client_id'].strip(),
                client_secret=config['db_client_secret'].strip()
            )
            return oauth_service_principal(cfg)

        with sql.connect(
            server_hostname=config["db_host"],
            http_path=config["db_path"],
            credentials_provider=get_credentials
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                result_list = [dict(zip(columns, row)) for row in rows]
                return result_list if result_list else [{"message": "Query executed successfully, but returned no data."}]
                
    except Exception as e:
        print(f"SQL Execution Error: {e}")
        return [{"error": str(e)}]