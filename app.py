from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

@app.route("/")
def home():
    try:
        # Managed Identity credential
        credential = DefaultAzureCredential()

        # Connect to Key Vault
        key_vault_name = "kv-appservice-poc"   # CHANGE THIS
        kv_url = f"https://{key_vault_name}.vault.azure.net/"
        secret_client = SecretClient(vault_url=kv_url, credential=credential)

        # Get secrets
        storage_account = secret_client.get_secret("storageaccountname").value
        container_name = secret_client.get_secret("containername").value

        # Connect to Blob Storage
        blob_service = BlobServiceClient(
            account_url=f"https://{storage_account}.blob.core.windows.net",
            credential=credential
        )

        container_client = blob_service.get_container_client(container_name)

        # Create dummy content
        content = "This is a dummy text file uploaded from Azure App Service using Managed Identity."

        blob_client = container_client.get_blob_client("dummy.txt")
        blob_client.upload_blob(content, overwrite=True)

        return "Dummy file uploaded successfully to Blob Storage!"

    except Exception as e:
        return f"Error occurred: {str(e)}"
