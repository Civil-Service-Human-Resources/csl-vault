from EnvironmentService import EnvironmentService
from VarFile import VarFile

class Validation:
    def validate_action(self, action_name):
        actions = ["add", "update", "delete", "bulk-add", "load", "bulk-load", "sync"]
        action_list = ", ".join(actions)
        if action_name not in actions:
            raise ValueError(f"'{action_name}' is not an acceptable action. Must be one of: {action_list}")

    def validate_environment(self, environment_name):
        environment_service = EnvironmentService()
        if not environment_service.environment_exists(environment_name):
            environment_list = ", ".join(environment_service.environments)
            raise ValueError(f"Environment '{environment_name}' doesn't exist. Must be one of: {environment_list}")

    def validate_module(self, environment, module_name):
        environment_service = EnvironmentService()
        environment_data = environment_service.get_environment(environment)
        modules = environment_data["modules"].keys()
        if module_name not in modules:
            module_list = ", ".join(modules)
            raise ValueError(f"Module '{module_name}' doesn't exist. Must be one of: {module_list}")

    def validate_variable(self, action, environment_name, module_name, variable_name):
        self.validate_action(action)
        self.validate_environment(environment_name)
        self.validate_module(environment_name, module_name)

        variable_file = VarFile(environment_name, module_name)

        if action == "add" and variable_file.variable_exists(variable_name):
            raise ValueError(f"'{variable_name}' already exists in module '{module_name}' in '{environment_name}' environment. Use `vault update` if you need to update it")

        elif action in ["update", "delete"] and not variable_file.variable_exists(variable_name):
            raise ValueError(f"'{variable_name}' doesn't  exist in module '{module_name}' in '{environment_name}' environment. Use `vault add` if you need to create it")