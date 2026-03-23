from initialize_client import initialize_client
from chat_loop import chat_loop

def main():
    """Main execution block"""
    client, deployment, deployment_embed = initialize_client()
    try:
        chat_loop(client, deployment, deployment_embed)
    finally:
        client.close

if __name__ == "__Main__":
    main()