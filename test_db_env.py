from dotenv import load_dotenv
import os

load_dotenv()

print("HOST:", os.getenv("DATABRICKS_SERVER_HOSTNAME"))
print("PATH:", os.getenv("DATABRICKS_HTTP_PATH"))
print("CLIENT_ID exists:", os.getenv("DATABRICKS_CLIENT_ID") is not None)
print("CLIENT_SECRET exists:", os.getenv("DATABRICKS_CLIENT_SECRET") is not None)