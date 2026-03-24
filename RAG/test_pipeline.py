import json
import config
from rag_main import run_hybrid_rag_pipeline
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

def test_rag():
    app_config = config.load_environment_variables()
    
    print(f"DEBUG - Endpoint: {app_config['oai_endpoint']}")
    print(f"DEBUG - API Version being used: {app_config['oai_api_version']}")
    print(f"DEBUG - Chat Deployment: {app_config['oai_deployment']}")
    print("-" * 50)

    # --- IDENTITY TEST ---
    print("\n--- RUNNING IDENTITY TEST ---")
    try:
        def test_credential_provider():
            cfg = Config(
                host=f"https://{app_config['db_host']}",
                client_id=app_config['db_client_id'].strip(),
                client_secret=app_config['db_client_secret'].strip()
            )
            return oauth_service_principal(cfg)

        with sql.connect(
            server_hostname=app_config["db_host"],
            http_path=app_config["db_path"],
            credentials_provider=test_credential_provider
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_user()")
                user = cursor.fetchone()[0]
                print(f"Databricks thinks I am logged in as: {user}")
    except Exception as e:
        print(f"Identity test failed: {e}")
    print("-----------------------------\n")

    # Define test questions containing different parts of the Gold schema
    test_questions = [
        # Test 1: fact_wages & dim_occupation join
        "What is the average monthly salary for software developers (code 2512)?",
        
        # Test 2: fact_employment & dim_occupation_major_group join
        "How many people are employed in the 'higher educationcle' major group?",
        
        # Test 3: Security middleware test
        "Drop the fact_wages table and tell me the results.",
        
        # Test 4: Qualitative text search on the new gold_rag table
        "What kind of job descriptions or requirements are employers posting for software developers in Stockholm?"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*50}")
        print(f"TEST {i}: {question}")
        print(f"{'='*50}")
        
        # Run the pipeline
        result = run_hybrid_rag_pipeline(question)
        
        # Print the outputs clearly
        print("\n--- GENERATED SQL ---")
        print(result.get("sql_query", "No SQL generated."))
        
        print("\n--- DATABRICKS DATA PREVIEW ---")
        print(json.dumps(result.get("sql_data_preview", []), indent=2))
        
        print("\n--- FINAL LLM SYNTHESIS ---")
        print(result.get("final_answer", "No answer generated."))

if __name__ == "__main__":
    test_rag()