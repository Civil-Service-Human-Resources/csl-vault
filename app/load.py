from AppServiceProperties import AppServiceProperties
from AzureProfile import AzureProfile
from EnvironmentService import EnvironmentService
from VarFile import VarFile
from AzureKeyVault import AzureKeyVault

def load(environment, module, name):
    
    key_vault = get_key_vault_for_environment(environment)

    variable_from_file = get_variable_from_file(environment, module, name)

    var_value = variable_from_file["value"]

    property_value = key_vault.get_secret_key_vault_reference(var_value) if variable_from_file["sensitive"] else var_value

    update_property_in_app_service(environment, module, name, property_value)
    
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