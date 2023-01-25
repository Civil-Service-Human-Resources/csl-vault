from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class AzureKeyVault:
    def __init__(self, vault_url):
        self.vault_url = vault_url
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=credential)

    def insert_secret(self, secret_name, secret_value):
        self.client.set_secret(secret_name, secret_value)

    def delete_secret(self, secret_name):
        self.client.begin_delete_secret(secret_name)

    def get_secret(self, secret_name):
        return self.client.get_secret(secret_name).value

    def get_secret_key_vault_reference(self, secret_name):
        return f"@Microsoft.KeyVault(SecretUri={self.vault_url}/secrets/{secret_name}/)"