from EnvironmentService import EnvironmentService
from VarFile import VarFile
from AzureProfile import AzureProfile
from AppServiceProperties import AppServiceProperties
from AzureKeyVault import AzureKeyVault

def bulk_load(environment):
    environment_service = EnvironmentService()
    azure_profile = AzureProfile()

    environment_data = environment_service.get_environment(environment)
    environment_modules = environment_data["modules"]

    subscription_id = azure_profile.get_subscription_id(environment)

    for module_name in environment_modules.keys():
        print("====== " + module_name + " ========")

        app_service_name = environment_modules[module_name]
        app_service_properties = AppServiceProperties(subscription_id, environment_data["resourceGroup"], app_service_name)

        var_file = VarFile(environment, module_name)
        all_variables = var_file.get_all_variables()

        for variable in all_variables:

            if variable["sensitive"]:
                azure_key_vault = AzureKeyVault(environment_data["vault"])
                app_service_properties.update_property(variable["name"], azure_key_vault.get_secret_key_vault_reference(variable["value"]))
            if not variable["sensitive"]:
                print(variable["name"] + ": " + variable["value"])
                properties = app_service_properties.get_app_properties()
                if variable["name"] in properties:
                    app_service_property_value = properties[variable["name"]]
                    print("In app service: " + app_service_property_value)
                    if variable["value"] == app_service_property_value:
                        print("✅ Variable in sync. No change required.")
                    else:
                        print("🔼 Variable is not in sync.")
                        app_service_properties.update_property(variable["name"], variable["value"])
                else:
                    print(f"🔵 Variable not in '{app_service_name}'. It will be added.")
                    app_service_properties.update_property(variable["name"], variable["value"])

            print()
            
        app_service_properties.push_updates_to_app_service()
        print(f"☁️ All variable updates pushed to app service '{app_service_name}'.")

        print()
