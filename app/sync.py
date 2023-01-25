from AppServiceProperties import AppServiceProperties
from EnvironmentService import EnvironmentService
from AzureProfile import AzureProfile
from VarFile import VarFile

def sync(environment, module_name, variable_name):
    environment_service = EnvironmentService()
    environment_data = environment_service.get_environment(environment)
    azure_profile = AzureProfile()

    subscription_id = azure_profile.get_subscription_id(environment)
    resource_group = environment_data["resourceGroup"]
    app_service_name = environment_data["modules"][module_name]
    app_service_properties = AppServiceProperties(subscription_id, resource_group, app_service_name)

    property_value = app_service_properties.get_property_value(variable_name)

    var_file = VarFile(environment, module_name)
    variable = var_file.get_variable(variable_name)

    if variable["sensitive"]:
        print("`vault` can only sync non-secret variables")
    else:
        var_file.update_variable(variable_name, property_value)
        print("✅ Variable updated locally.")

    print(variable)