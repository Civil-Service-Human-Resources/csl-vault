import add
from AzureKeyVault import AzureKeyVault
import Utils

def test_add_var_calls_insert_variable_to_keyvault_if_variable_is_secret(mocker):
    environment = "myEnv"
    module = "myModule"
    variable_name = "myVar"
    variable_value = "myVarValue"
    is_secret = True

    mocker.patch("add.insert_variable_to_keyvault")
    mocker.patch("add.add_variable_to_file")

    insert_to_keyvault_spy = mocker.spy(add, "insert_variable_to_keyvault")

    add.add_var(environment, module, variable_name, variable_value, is_secret)

    insert_to_keyvault_spy.assert_called_once_with(environment, module, variable_name, variable_value)

def test_add_var_does_not_call_insert_variable_to_keyvault_if_variable_is_secret(mocker):
    environment = "myEnv"
    module = "myModule"
    variable_name = "myVar"
    variable_value = "myVarValue"
    is_secret = False

    mocker.patch("add.insert_variable_to_keyvault")
    mocker.patch("add.add_variable_to_file")

    insert_to_keyvault_spy = mocker.spy(add, "insert_variable_to_keyvault")

    add.add_var(environment, module, variable_name, variable_value, is_secret)

    insert_to_keyvault_spy.assert_not_called()

def test_add_var_calls_add_variable_to_file_for_secret_variables_with_keyvault_secret_id_as_value(mocker):
    environment = "myEnv"
    module = "myModule"
    variable_name = "myVar"
    variable_value = "myVarValue"
    is_secret = True

    mocker.patch("add.get_keyvault_for_environment")
    mocker.patch("add.add_variable_to_file")
    mocker.patch("AzureKeyVault.AzureKeyVault.insert_secret")

    add_to_file_spy = mocker.spy(add, "add_variable_to_file")

    add.add_var(environment, module, variable_name, variable_value, is_secret)

    add_to_file_spy.assert_called_once_with(environment, module, variable_name, Utils.get_keyvault_secret_id_from_variable_name(module, variable_name), is_secret=is_secret)

def test_add_var_calls_add_variable_to_file_for_non_secret_variables_with_variable_value_as_value(mocker):
    environment = "myEnv"
    module = "myModule"
    variable_name = "myVar"
    variable_value = "myVarValue"
    is_secret = False

    mocker.patch("add.get_keyvault_for_environment")
    mocker.patch("add.add_variable_to_file")
    mocker.patch("AzureKeyVault.AzureKeyVault.insert_secret")

    add_to_file_spy = mocker.spy(add, "add_variable_to_file")

    add.add_var(environment, module, variable_name, variable_value, is_secret)

    add_to_file_spy.assert_called_once_with(environment, module, variable_name, variable_value, is_secret=is_secret)

