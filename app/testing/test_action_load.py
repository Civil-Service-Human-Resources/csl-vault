import load
from AzureKeyVault import AzureKeyVault

def test_update_property_in_app_service_is_called_if_variable_not_a_secret_with_value(mocker):

    environment = "env"
    module = "my-module"
    var_name = "MY_VAR"
    var_value = "1234"
    is_secret = False
    use_keyvault_reference = False

    mocker.patch("load.get_variable_from_file", return_value = {
        "name": var_name,
        "value": var_value,
        "sensitive": is_secret,
        "use_keyvault_reference": use_keyvault_reference
    })
    mocker.patch("load.get_key_vault_for_environment", return_value=AzureKeyVault("http://a-vault.azure.net"))
    mocker.patch("load.update_property_in_app_service")

    update_property_in_app_service_spy = mocker.spy(load, "update_property_in_app_service")

    load.load(environment, module, var_name)

    update_property_in_app_service_spy.assert_called_once_with(environment, module, var_name, "1234")

def test_update_property_in_app_service_is_called_if_variable_is_a_secret_with_raw_secret(mocker):

    environment = "env"
    module = "my-module"
    var_name = "MY_VAR"
    var_value = "my-var"
    is_secret = True
    use_keyvault_reference = False

    expected_raw_value = "secret-value"

    mocker.patch("load.get_variable_from_file", return_value = {
        "name": var_name,
        "value": var_value,
        "sensitive": is_secret,
        "use_keyvault_reference": use_keyvault_reference
    })
    mocker.patch("AzureKeyVault.AzureKeyVault.get_secret", return_value="secret-value")
    mocker.patch("load.get_key_vault_for_environment", return_value=AzureKeyVault("http://a-vault.azure.net"))
    mocker.patch("load.update_property_in_app_service")

    update_property_in_app_service_spy = mocker.spy(load, "update_property_in_app_service")

    load.load(environment, module, var_name)

    update_property_in_app_service_spy.assert_called_once_with(environment, module, var_name, expected_raw_value)

def test_update_property_in_app_service_is_called_if_variable_is_a_secret_with_key_vault_reference(mocker):

    environment = "env"
    module = "my-module"
    var_name = "MY_VAR"
    var_value = "my-var"
    is_secret = True
    use_keyvault_reference = True

    expected_key_vault_reference = "@Microsoft.KeyVault(SecretUri=http://a-vault.azure.net/secrets/my-var/)"

    mocker.patch("load.get_variable_from_file", return_value = {
        "name": var_name,
        "value": var_value,
        "sensitive": is_secret,
        "use_keyvault_reference": use_keyvault_reference
    })
    mocker.patch("load.get_key_vault_for_environment", return_value=AzureKeyVault("http://a-vault.azure.net"))
    mocker.patch("load.update_property_in_app_service")

    update_property_in_app_service_spy = mocker.spy(load, "update_property_in_app_service")

    load.load(environment, module, var_name)

    update_property_in_app_service_spy.assert_called_once_with(environment, module, var_name, expected_key_vault_reference)