from . import config
from . import db_tools
from . import ai_agents

def run_hybrid_rag_pipeline(user_question: str) -> dict:
    app_config = config.load_environment_variables()
    llm_client = config.get_llm_client(app_config)
    
    # SQL to Databricks
    sql_query = ai_agents.generate_sql_query(user_question, llm_client, app_config)
    sql_results = db_tools.execute_databricks_sql(sql_query, app_config)
    
    if sql_results and "error" in sql_results[0]:
        return {
            "sql_query": sql_query,
            "final_answer": f"I encountered a database error: {sql_results[0]['error']}"
        }
        
    # Vector/Keyword Search
    text_results = db_tools.retrieve_job_ad_text_context(user_question, llm_client, app_config)
    
    # LLM combination
    final_answer = ai_agents.generate_final_synthesis(
        question=user_question,
        sql_data=sql_results,
        text_context=text_results,
        client=llm_client,
        config=app_config
    )
    
    return {
        "sql_query": sql_query,
        "sql_data_preview": sql_results[:5],
        "final_answer": final_answer
    }