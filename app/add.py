from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
from EnvironmentService import EnvironmentService
import Utils

def add_var(environment, module, var_name, var_value, is_secret, use_keyvault_reference):
    print(f"Adding variable '{var_name}' to {module} in {environment}...")

    value_added_to_variable = var_value

    if is_secret:
        print("This variable is a secret. Adding it to the key vault...")
        secret_details = insert_variable_to_keyvault(environment, module, var_name, var_value)
        value_added_to_variable = secret_details["secret_id"]

        print(f"Variable added to key vault as '{value_added_to_variable}'")

    add_variable_to_file(environment, module, var_name, value_added_to_variable, is_secret=is_secret, use_keyvault_reference=use_keyvault_reference)
    print(f"✅ '{var_name}' added to the variables file.")

def insert_variable_to_keyvault(environment, module, variable_name, secret_value):
    key_vault = get_keyvault_for_environment(environment)
    keyvault_secret_id = Utils.get_keyvault_secret_id_from_variable_name(module, variable_name)
    key_vault.insert_secret(keyvault_secret_id, secret_value)

    return {
        "secret_id": keyvault_secret_id
    }

def get_keyvault_for_environment(environment_name):
    environment_service = EnvironmentService()
    key_vault_uri = environment_service.get_environment(environment_name)["vault"]
    return AzureKeyVault(key_vault_uri)

def add_variable_to_file(environment, module, var_name, var_value, is_secret, use_keyvault_reference):
    var_file = VarFile(environment, module)
    var_file.insert_variable(var_name, var_value, is_secret, use_keyvault_reference)