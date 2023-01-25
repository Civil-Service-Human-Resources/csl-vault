from azure.mgmt.web import WebSiteManagementClient 
from azure.identity import DefaultAzureCredential

class AppServiceProperties:
    def __init__(self, subscription_id, resource_group, app_service_name):
        self.resource_group = resource_group
        self.app_service_name = app_service_name
        
        self.web_client = self.get_web_client(subscription_id)
        self.app_settings = self.get_application_settings()

    def get_app_properties(self):
        return self.app_settings.properties

    def get_property_value(self, property_name):
        return self.get_app_properties()[property_name]

    def property_exists_in_app_service(self, property_name):
        return property_name in self.get_app_properties().keys()

    def update_property(self, property_name, property_value):
        self.app_settings.properties.update({ property_name: property_value })

    def push_updates_to_app_service(self):
        self.web_client.web_apps.update_application_settings(
            self.resource_group, 
            self.app_service_name, 
            app_settings=self.app_settings
        )

    def get_web_client(self, subscription_id):
        credential = DefaultAzureCredential()
        return WebSiteManagementClient(credential=credential, subscription_id=subscription_id)

    def get_application_settings(self):
         return self.web_client.web_apps.list_application_settings(self.resource_group, self.app_service_name)