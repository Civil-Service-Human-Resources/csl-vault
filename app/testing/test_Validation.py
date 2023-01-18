from Validation import Validation
import pytest
import json
def test_validate_action_does_nothing_when_action_is_in_list():
    action = "add"

    validation = Validation()
    validation.validate_action(action)

def test_valication_action_throws_ValueError_if_action_is_not_valid():
    action = "edit"

    validation = Validation()

    with pytest.raises(ValueError):
        validation.validate_action(action)    

def test_validate_environment_does_nothing_when_environment_exists(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    environment = "test"

    validation = Validation()
    validation.validate_environment(environment)

def test_validate_environment_throws_ValueError_if_environment_does_not_exist(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )
    
    environment = "integration"

    validation = Validation()

    with pytest.raises(ValueError):
        validation.validate_environment(environment)

def test_validate_module_does_nothing_if_module_exists(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    environment = "test"
    module = "module1"

    validation = Validation()
    validation.validate_module(environment, module)

def test_validate_module_throws_ValueError_if_module_does_not_exist_in_environment(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    environment = "test"
    module = "non-existent-module"

    validation = Validation()

    with pytest.raises(ValueError):
        validation.validate_module(environment, module)

def test_validate_variable_does_nothing_if_variable_does_not_exist_in_environment_and_module_for_add_action(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    environment = "test"
    module = "test"
    variable_id = "MY_NEW_VAR"

    validation = Validation()
    validation.validate_variable("add", environment, module, variable_id)

def test_validate_variable_throws_ValueError_if_variable_exists_in_environment_and_module_for_add_action(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    environment = "test"
    module = "test"
    variable_id = "MY_VAR1"

    validation = Validation()

    with pytest.raises(ValueError):
        validation.validate_variable("add", environment, module, variable_id)

def test_validate_variable_does_nothing_if_variable_exists_in_environment_and_module_for_update_action(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    environment = "test"
    module = "test"
    variable_id = "MY_VAR1"

    validation = Validation()
    validation.validate_variable("update", environment, module, variable_id)

def test_validate_variable_does_nothing_if_variable_exists_in_environment_and_module_for_delete_action(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    environment = "test"
    module = "test"
    variable_id = "MY_VAR1"

    validation = Validation()
    validation.validate_variable("delete", environment, module, variable_id)

def test_validate_variable_throws_ValueError_if_variable_does_not_exist_in_environment_and_module_for_update_action(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    environment = "test"
    module = "test"
    variable_id = "ANOTHER_VAR"

    validation = Validation()
    with pytest.raises(ValueError):
        validation.validate_variable("update", environment, module, variable_id)

def test_validate_variable_throws_ValueError_if_variable_does_not_exist_in_environment_and_module_for_delete_action(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    environment = "test"
    module = "test"
    variable_id = "ANOTHER_VAR"

    validation = Validation()
    with pytest.raises(ValueError):
        validation.validate_variable("delete", environment, module, variable_id)