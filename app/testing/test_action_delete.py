import delete

def test_user_is_prompted_to_confirm_deletion_if_variable_exists_in_any_app_service(mocker):
    environment = "env"
    module = "MyModule"
    variable_name = "MY_VAR"
    app_services = ["app1", "app2", "app3"]

    mocker.patch("delete.get_list_of_app_services_a_property_exists", return_value=app_services)
    mocker.patch("delete.prompt_deletion_confirmation")
    mocker.patch("delete.get_variable")
    mocker.patch("delete.soft_delete_variable_from_key_vault")
    mocker.patch("delete.remove_variable_from_file")

    prompt_deletion_confirmation_spy = mocker.spy(delete, "prompt_deletion_confirmation")

    delete.delete_var(environment, module, variable_name)

    prompt_deletion_confirmation_spy.assert_called_once_with(app_services)

def test_user_is_not_prompted_to_confirm_deletion_if_variable_does_not_exist_in_any_app_service(mocker):
    environment = "env"
    module = "MyModule"
    variable_name = "MY_VAR"
    app_services = []

    mocker.patch("delete.get_list_of_app_services_a_property_exists", return_value=app_services)
    mocker.patch("delete.prompt_deletion_confirmation")
    mocker.patch("delete.get_variable")
    mocker.patch("delete.soft_delete_variable_from_key_vault")
    mocker.patch("delete.remove_variable_from_file")

    prompt_deletion_confirmation_spy = mocker.spy(delete, "prompt_deletion_confirmation")

    delete.delete_var(environment, module, variable_name)

    prompt_deletion_confirmation_spy.assert_not_called()

def test_soft_delete_variable_from_key_vault_is_called_if_variable_is_not_in_app_services_and_variable_is_a_secret(mocker):
    environment = "env"
    module = "MyModule"
    variable_name = "MY_VAR"
    secret_id = "my-var"
    is_secret = True
    app_services = []

    mocker.patch("delete.get_list_of_app_services_a_property_exists", return_value=app_services)
    mocker.patch("delete.prompt_deletion_confirmation")
    mocker.patch("delete.get_variable", return_value = {
        "name": variable_name,
        "value": secret_id,
        "sensitive": is_secret
    })
    mocker.patch("delete.soft_delete_variable_from_key_vault")
    mocker.patch("delete.remove_variable_from_file")

    soft_delete_variable_from_key_vault_spy = mocker.spy(delete, "soft_delete_variable_from_key_vault")

    delete.delete_var(environment, module, variable_name)

    soft_delete_variable_from_key_vault_spy.assert_called_once_with(environment, secret_id)

def test_soft_delete_variable_from_key_vault_is_called_if_deletion_is_confirmed_and_variable_is_a_secret(mocker):
    environment = "env"
    module = "MyModule"
    variable_name = "MY_VAR"
    secret_id = "my-var"
    is_secret = True
    app_services = ["app1", "app2"]

    mocker.patch("delete.get_list_of_app_services_a_property_exists", return_value=app_services)
    mocker.patch("delete.prompt_deletion_confirmation", return_value=True)
    mocker.patch("delete.get_variable", return_value = {
        "name": variable_name,
        "value": secret_id,
        "sensitive": is_secret
    })
    mocker.patch("delete.soft_delete_variable_from_key_vault")
    mocker.patch("delete.remove_variable_from_file")

    soft_delete_variable_from_key_vault_spy = mocker.spy(delete, "soft_delete_variable_from_key_vault")

    delete.delete_var(environment, module, variable_name)

    soft_delete_variable_from_key_vault_spy.assert_called_once_with(environment, secret_id)

def test_remove_variable_from_file_is_not_run_if_deletion_is_not_confirmed(mocker):
    environment = "env"
    module = "MyModule"
    variable_name = "MY_VAR"
    secret_id = "my-var"
    is_secret = True
    app_services = ["app1", "app2"]

    mocker.patch("delete.get_list_of_app_services_a_property_exists", return_value=app_services)
    mocker.patch("delete.prompt_deletion_confirmation", return_value=False)
    mocker.patch("delete.get_variable", return_value = {
        "name": variable_name,
        "value": secret_id,
        "sensitive": is_secret
    })
    mocker.patch("delete.soft_delete_variable_from_key_vault")
    mocker.patch("delete.remove_variable_from_file")

    remove_variable_from_file_spy = mocker.spy(delete, "remove_variable_from_file")

    delete.delete_var(environment, module, variable_name)

    remove_variable_from_file_spy.assert_not_called()

def test_soft_delete_variable_from_key_vault_is_not_called_if_deletion_is_not_confirmed_and_variable_is_a_secret(mocker):
    environment = "env"
    module = "MyModule"
    variable_name = "MY_VAR"
    secret_id = "my-var"
    is_secret = True
    app_services = ["app1", "app2"]

    mocker.patch("delete.get_list_of_app_services_a_property_exists", return_value=app_services)
    mocker.patch("delete.prompt_deletion_confirmation", return_value=False)
    mocker.patch("delete.get_variable", return_value = {
        "name": variable_name,
        "value": secret_id,
        "sensitive": is_secret
    })
    mocker.patch("delete.soft_delete_variable_from_key_vault")
    mocker.patch("delete.remove_variable_from_file")

    soft_delete_variable_from_key_vault_spy = mocker.spy(delete, "soft_delete_variable_from_key_vault")

    delete.delete_var(environment, module, variable_name)

    soft_delete_variable_from_key_vault_spy.assert_not_called()