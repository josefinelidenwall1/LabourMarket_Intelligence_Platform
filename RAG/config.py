import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def load_environment_variables() -> dict:
    load_dotenv()
    return {
        "db_host": os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        "db_path": os.getenv("DATABRICKS_HTTP_PATH"),
        "db_token": os.getenv("DATABRICKS_TOKEN"),
        "oai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "oai_key": os.getenv("AZURE_OPENAI_KEY"),
        "oai_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        "oai_embedding": os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
        "oai_api_version": os.getenv("AZURE_API_VERSION")
    }

def get_llm_client(config: dict) -> AzureOpenAI:
    return AzureOpenAI(
        api_key=config["oai_key"],
        api_version=config["oai_api_version"],
        azure_endpoint=config["oai_endpoint"]
    )