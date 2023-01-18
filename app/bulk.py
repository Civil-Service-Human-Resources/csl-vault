import json
from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
from EnvironmentService import EnvironmentService
import Utils

def add(file_path):
    bulk_variables = get_variables_from_bulk_file(file_path)

    for module in bulk_variables:
            environment = module["environment"]
            module_name = module["module"]
            values = module["values"]

            for value in values:
                var_name = value["name"]
                var_value = value["value"]
                is_secret = value["secret"]

                value_added_to_file = var_value

                if is_secret:
                    secret_details = add_variable_to_key_vault(environment, module_name, var_name, var_value)
                    value_added_to_file = secret_details["secret_id"]
                    print("🔑 Inserted secret '" + secret_details["secret_id"] + "' to the Key Vault")

                add_variable_to_variables_file(environment, module_name, var_name, value_added_to_file, is_secret=is_secret)
                print(f"✅ {var_name} inserted variable in variables file")

def get_variables_from_bulk_file(file_path):
    json.loads(open(file_path, "r").read())

def add_variable_to_key_vault(environment, module, var_name, var_value):
    key_vault = get_key_vault_for_environment(environment)
    key_vault_secret_id = Utils.get_keyvault_secret_id_from_variable_name(module, var_name)
    key_vault.insert_secret(key_vault_secret_id, var_value)
    return {
        "secret_id": key_vault_secret_id
    }

def get_key_vault_for_environment(environment):
    environment_service = EnvironmentService()
    key_vault_uri = environment_service.get_environment(environment)["vault"]
    return AzureKeyVault(key_vault_uri)

def add_variable_to_variables_file(environment, module, var_name, var_value, is_secret):
    var_file = VarFile(environment, module)
    var_file.insert_variable(var_name, var_value, is_secret)