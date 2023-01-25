from VarFile import VarFile
from AzureKeyVault import AzureKeyVault
from EnvironmentService import EnvironmentService
from AppServiceProperties import AppServiceProperties
from AzureProfile import AzureProfile

def delete_var(environment, module, var_name):
    print(f"Deleting variable '{var_name}' from {module} in {environment}...")

    app_services_property_exists = get_list_of_app_services_a_property_exists(environment, var_name)
    if len(app_services_property_exists) > 0:
        user_has_confirmed_deletion = prompt_deletion_confirmation(app_services_property_exists)

    if len(app_services_property_exists) == 0 or user_has_confirmed_deletion:
        variable = get_variable(environment, module, var_name)
        
        if variable["sensitive"]:
            secret_id = variable["value"]
            soft_delete_variable_from_key_vault(environment, secret_id)

            print(f"'{secret_id}' successfully deleted from KeyVault.")
            print("ℹ️ This variable has been soft-deleted. Use the Azure CLI's `az keyvault secret purge` command to permanently delete it. Learn more here: https://learn.microsoft.com/en-us/cli/azure/keyvault/secret?view=azure-cli-latest#az-keyvault-secret-purge")

        remove_variable_from_file(environment, module, var_name)
        print(f"✅ '{var_name}' deleted from variables file.")
    else:
        print("Deletion of variable has been cancelled")

def prompt_deletion_confirmation(app_services_list):
    print("This variable is currently being used in these app services: " + ", ".join(app_services_list))
    user_answer = input("Are you sure you'd like to delete this variable? (Can only accept 'yes') ")
    return user_answer == "yes"

def get_list_of_app_services_a_property_exists(environment, property_name):
    azure_profile = AzureProfile()
    environment_data = EnvironmentService()

    environment_data = environment_data.get_environment(environment)
    modules = environment_data["modules"]

    apps_property_exists = []

    for module_name in modules.keys():
        app_service_name = modules[module_name]
        app_service_properties = AppServiceProperties(azure_profile.get_subscription_id(environment), environment_data["resourceGroup"], app_service_name)

        if app_service_properties.property_exists_in_app_service(property_name):
            apps_property_exists.append(app_service_name)

    return apps_property_exists

def get_variable(environment, module, var_name):
    file = VarFile(environment, module)
    variable = file.get_variable(var_name)
    return variable

def soft_delete_variable_from_key_vault(environment, secret_id):
    environment_service = EnvironmentService()
    key_vault = AzureKeyVault(environment_service.get_environment(environment)["vault"])
    key_vault.delete_secret(secret_id)

def remove_variable_from_file(environment, module, var_name):
    file = VarFile(environment, module)
    file.delete_variable(var_name)
    