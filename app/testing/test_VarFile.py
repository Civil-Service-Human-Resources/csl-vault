from VarFile import VarFile
import json

def test_variable_exists_returns_true_if_variable_is_present(mocker):
    variable_name_to_test = "MY_VAR1"

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    var_file = VarFile("test", "test")

    assert var_file.variable_exists(variable_name_to_test) == True

def test_variable_exists_returns_false_if_variable_is_not_present(mocker):
    variable_name_to_test = "MY_VAR_NON_EXISTENT"

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    var_file = VarFile("test", "test")

    assert var_file.variable_exists(variable_name_to_test) == False

def test_get_variable_returns_correct_variable_details(mocker):

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    variable_id = "MY_VAR1"

    expected_details = {
        "name": "MY_VAR1",
        "sensitive": False,
        "value": "123"
    }

    var_file = VarFile("test", "test")

    variable = var_file.get_variable(variable_id)

    assert variable == expected_details

def test_get_all_variables_returns_all_available_variables(mocker):

    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    variable_id = "MY_VAR1"

    expected_result = [
    {
        "name": "MY_VAR1",
        "sensitive": False,
        "value": "123"
    },
    {
        "name": "MY_VAR2",
        "sensitive": True,
        "value": "test-second-bulk-var-secret"
    },
    {
        "name": "MY_VAR2",
        "sensitive": False,
        "value": "123456"
    }
]

    var_file = VarFile("test", "test")

    all_variables = var_file.get_all_variables()

    assert all_variables == expected_result

def test_insert_variable_inserts_new_variable_in_file(mocker):
    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    mocker.patch(
        'VarFile.VarFile.get_file_to_write',
        return_value=open("/tmp/var-file.json", "w")
    )

    variable_name = "NEW_VAR1"
    variable_value = "12345"
    is_secret = False

    expected_result = [
    {
        "name": "MY_VAR1",
        "sensitive": False,
        "value": "123"
    },
    {
        "name": "MY_VAR2",
        "sensitive": True,
        "value": "test-second-bulk-var-secret"
    },
    {
        "name": "MY_VAR2",
        "sensitive": False,
        "value": "123456"
    },
    {
        "name": "NEW_VAR1",
        "sensitive": False,
        "value": "12345"
    }
]

    var_file = VarFile("test", "test")
    var_file.insert_variable(variable_name, variable_value, is_secret)

    json.loads(open("/tmp/var-file.json", "r").read()) == expected_result

def test_update_variable_updates_variable_in_file_with_new_value(mocker):
    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    mocker.patch(
        'VarFile.VarFile.get_file_to_write',
        return_value=open("/tmp/var-file.json", "w")
    )

    variable_name = "MY_VAR1"
    variable_value = "98765"

    expected_result = [
    {
        "name": "MY_VAR1",
        "sensitive": False,
        "value": "98765"
    },
    {
        "name": "MY_VAR2",
        "sensitive": True,
        "value": "test-second-bulk-var-secret"
    },
    {
        "name": "MY_VAR2",
        "sensitive": False,
        "value": "123456"
    }
]

    var_file = VarFile("test", "test")
    var_file.update_variable(variable_name, variable_value)

    json.loads(open("/tmp/var-file.json", "r").read()) == expected_result


def test_delete_variable_removes_variable_from_file(mocker):
    mocker.patch(
        'VarFile.VarFile.get_all_variables',
        return_value=json.loads(open("./testing/resources/test-vars.json").read())
    )

    mocker.patch(
        'VarFile.VarFile.get_file_to_write',
        return_value=open("/tmp/var-file.json", "w")
    )

    variable_name = "MY_VAR1"

    expected_result = [
    {
        "name": "MY_VAR2",
        "sensitive": True,
        "value": "test-second-bulk-var-secret"
    },
    {
        "name": "MY_VAR2",
        "sensitive": False,
        "value": "123456"
    }
]

    var_file = VarFile("test", "test")
    var_file.delete_variable(variable_name)

    json.loads(open("/tmp/var-file.json", "r").read()) == expected_result