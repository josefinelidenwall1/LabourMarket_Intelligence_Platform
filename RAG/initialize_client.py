import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def initialize_client():
    """Load environment variables and initialise azure OpenAI client"""
    load_dotenv()
    api_key = os.getenv("AZURE_API_KEY")
    api_version = os.getenv("AZURE_API_VERSION")
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    deployment = os.getenv("AZURE_DEPLOYMENT")
    deployment_embed = os.getenv("EMBEDDING_DEPLOYMENT")

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint
    )
    return client, deployment, deployment_embed