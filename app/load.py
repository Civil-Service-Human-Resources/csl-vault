from AppServiceProperties import AppServiceProperties
from AzureProfile import AzureProfile
from EnvironmentService import EnvironmentService
from VarFile import VarFile
from AzureKeyVault import AzureKeyVault

def load(environment, module, name):
    
    key_vault = get_key_vault_for_environment(environment)

    variable_from_file = get_variable_from_file(environment, module, name)
    property_value = __extract_value_from_variable(key_vault, variable_from_file)

    update_property_in_app_service(environment, module, name, property_value)

def __extract_value_from_variable(key_vault: AzureKeyVault, variable):
    var_value = variable["value"]
    sensitive = variable["sensitive"]
    use_keyvault_reference = variable["use_keyvault_reference"] or False

    if sensitive:
        if use_keyvault_reference:
            return key_vault.get_secret_key_vault_reference(var_value)
        else:
            return key_vault.get_secret(var_value)
    else:
        return var_value

def update_property_in_app_service(environment, module, name, value):
    app_service_properties = get_app_service_properties(environment, module)
    app_service_properties.update_property(name, value)
    app_service_properties.push_updates_to_app_service()

def get_app_service_properties(environment, module):
    azure_profile = AzureProfile()

    environment_data = get_environment_data(environment)

    subscription_id = azure_profile.get_subscription_id(environment)
    resource_group = environment_data["resourceGroup"]
    app_service_name = environment_data["modules"][module]

    return AppServiceProperties(subscription_id, resource_group, app_service_name)

def get_key_vault_for_environment(environment):
    environment_data = get_environment_data(environment)
    return AzureKeyVault(environment_data["vault"])

def get_variable_from_file(environment, module, var_name):
    var_file = VarFile(environment, module)
    return var_file.get_variable(var_name)


def get_environment_data(environment):
    environment_service = EnvironmentService()
    return environment_service.get_environment(environment)