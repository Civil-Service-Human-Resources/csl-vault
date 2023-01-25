import update

def test_add_variable_to_keyvault_is_called_if_variable_is_secret(mocker):
    environment = "integration"
    module = "myModule"
    variable_name = "MY_VAR"
    variable_value = "01234"
    is_secret = True

    mocker.patch("update.variable_is_secret", return_value=is_secret)
    mocker.patch("update.get_key_vault_for_environment")
    mocker.patch("AzureKeyVault.AzureKeyVault.insert_secret")
    mocker.patch("update.update_variable_in_var_file")

    add_variable_to_keyvault_spy = mocker.spy(update, "add_variable_to_keyvault")

    update.update_var(environment, module, variable_name, variable_value)

    add_variable_to_keyvault_spy.assert_called_once_with(environment, module, variable_name, variable_value)

def test_add_variable_to_keyvault_is_not_called_if_variable_is_not_secret(mocker):
    environment = "integration"
    module = "myModule"
    variable_name = "MY_VAR"
    variable_value = "01234"
    is_secret = False

    mocker.patch("update.variable_is_secret", return_value=is_secret)
    mocker.patch("update.get_key_vault_for_environment")
    mocker.patch("AzureKeyVault.AzureKeyVault.insert_secret")
    mocker.patch("update.update_variable_in_var_file")

    add_variable_to_keyvault_spy = mocker.spy(update, "add_variable_to_keyvault")

    update.update_var(environment, module, variable_name, variable_value)

    add_variable_to_keyvault_spy.assert_not_called()

def test_update_variable_in_var_file_is_called_if_variable_is_secret_with_key_vault_secret_id_as_value(mocker):
    environment = "integration"
    module = "myModule"
    variable_name = "MY_VAR"
    variable_value = "01234"
    is_secret = True

    expected_value_in_file = "myModule-my-var"

    mocker.patch("update.variable_is_secret", return_value=is_secret)
    mocker.patch("update.get_key_vault_for_environment")
    mocker.patch("AzureKeyVault.AzureKeyVault.insert_secret")
    mocker.patch("update.update_variable_in_var_file")

    update_variable_in_var_file_spy = mocker.spy(update, "update_variable_in_var_file")

    update.update_var(environment, module, variable_name, variable_value)

    update_variable_in_var_file_spy.assert_called_once_with(environment, module, variable_name, expected_value_in_file)

def test_update_variable_in_var_file_is_called_if_variable_is_not_secret_with_variale_value_as_value(mocker):
    environment = "integration"
    module = "myModule"
    variable_name = "MY_VAR"
    variable_value = "01234"
    is_secret = False

    expected_value_in_file = "01234"

    mocker.patch("update.variable_is_secret", return_value=is_secret)
    mocker.patch("update.get_key_vault_for_environment")
    mocker.patch("AzureKeyVault.AzureKeyVault.insert_secret")
    mocker.patch("update.update_variable_in_var_file")

    update_variable_in_var_file_spy = mocker.spy(update, "update_variable_in_var_file")

    update.update_var(environment, module, variable_name, variable_value)

    update_variable_in_var_file_spy.assert_called_once_with(environment, module, variable_name, expected_value_in_file)