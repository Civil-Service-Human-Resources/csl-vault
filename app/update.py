from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
import json
from EnvironmentService import EnvironmentService
import Utils

def update_var(environment, module, var_name, var_value):
    print(f"Updating variable '{var_name}' to {module} in {environment}...")

    value_added_to_variable = var_value

    if variable_is_secret(environment, module, var_name):
        print(f"'{var_name}' is a secret variable. Adding it to the key vault...")
        secret_details = add_variable_to_keyvault(environment, module, var_name, var_value)
        value_added_to_variable = secret_details["secret_id"]

        print(f"'{value_added_to_variable}' successfully updating in KeyVault")

    update_variable_in_var_file(environment, module, var_name, value_added_to_variable)
    print(f"✅ '{var_name}' updated in variables file.")

def add_variable_to_keyvault(environment, module, var_name, var_value):
    key_vault = get_key_vault_for_environment(environment)
    key_vault_secret_id = Utils.get_keyvault_secret_id_from_variable_name(module, var_name)
    key_vault.insert_secret(key_vault_secret_id, var_value)
    return {
        "secret_id": key_vault_secret_id
    }

def variable_is_secret(environment, module, var_name):
    file = VarFile(environment, module)
    variable = file.get_variable(var_name)
    return variable["secret"]

def get_key_vault_for_environment(environment):
    environment_service = EnvironmentService()
    return AzureKeyVault(environment_service.get_environment(environment)["vault"])

def update_variable_in_var_file(environment, module, var_name, var_value):
    file = VarFile(environment, module)
    file.update_variable(var_name, var_value)