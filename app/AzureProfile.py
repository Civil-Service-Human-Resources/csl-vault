import json
import os
from EnvironmentService import EnvironmentService

class AzureProfile:
    def get_subscription_id(self, environment):
        environment_service = EnvironmentService()
        environment_data = environment_service.get_environment(environment)
        az_profile = json.loads(open(os.environ["HOME"] + "/.azure/azureProfile.json", encoding="utf-8-sig").read())
        profile_subscriptions = az_profile["subscriptions"]
        subscription_id = next(subscription for subscription in profile_subscriptions if subscription["name"] == environment_data["subscription"])["id"]
        return subscription_id