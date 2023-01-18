import json
class EnvironmentService:
    def __init__(self):
        environments = self.get_environments_file()
        environments = json.loads(environments)
        self.environments = environments

    def environment_exists(self, environment_name):
        return environment_name in self.environments.keys()

    def get_environment(self, environment_name):
        return self.environments[environment_name]

    def get_environments_file(self):
        return open("data/environments.json", "r", encoding="utf-8-sig").read()