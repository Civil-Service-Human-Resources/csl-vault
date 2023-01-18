import bulk

def test_add_variable_to_key_vault_is_run_once_if_one_secret_variable_is_present_in_bulk_file(mocker):
    file_path = "/path/to/file.json"

    environment = "test"
    module = "test"
    var_name = "MYSQL_PASS"
    var_value = "password1"

    mocker.patch("bulk.get_variables_from_bulk_file", return_value=[
            {
                "environment": "test",
                "module": "test",
                "values":[
                    {
                        "name": "MYSQL_URL",
                        "value": "http://localhost:3306",
                        "secret": False
                    },
                    {
                        "name": "MYSQL_PASS",
                        "value": "password1",
                        "secret": True
                    }
                ]

            }
        ])

    mocker.patch("bulk.add_variable_to_key_vault")
    mocker.patch("bulk.add_variable_to_variables_file")

    add_variable_to_key_vault_spy = mocker.spy(bulk, "add_variable_to_key_vault")

    bulk.add(file_path)

    add_variable_to_key_vault_spy.assert_called_once_with(environment, module, var_name, var_value)
    
def test_add_variable_to_key_vault_is_run_twice_if_two_secret_variables_are_present_in_bulk_file(mocker):
    file_path = "/path/to/file.json"

    mocker.patch("bulk.get_variables_from_bulk_file", return_value=[
            {
                "environment": "test",
                "module": "test",
                "values":[
                    {
                        "name": "MYSQL_URL",
                        "value": "http://localhost:3306",
                        "secret": False
                    },
                    {
                        "name": "MYSQL_PASS",
                        "value": "password1",
                        "secret": True
                    },
                    {
                        "name": "MONGO_URL",
                        "value": "http://mongodb/",
                        "secret": True
                    }
                ]

            }
        ])

    mocker.patch("bulk.add_variable_to_key_vault")
    mocker.patch("bulk.add_variable_to_variables_file")

    add_variable_to_key_vault_spy = mocker.spy(bulk, "add_variable_to_key_vault")

    bulk.add(file_path)

    add_variable_to_key_vault_spy.assert_has_calls([
        mocker.call("test", "test", "MYSQL_PASS", "password1"),
        mocker.call("test", "test", "MONGO_URL", "http://mongodb/")
    ])

def test_add_variable_to_variables_file_is_called_three_times_if_three_variables_are_present_in_bulk_file(mocker):
    file_path = "/path/to/file.json"

    mocker.patch("bulk.get_variables_from_bulk_file", return_value=[
            {
                "environment": "test",
                "module": "test",
                "values":[
                    {
                        "name": "MYSQL_URL",
                        "value": "http://localhost:3306",
                        "secret": False
                    },
                    {
                        "name": "MYSQL_PASS",
                        "value": "password1",
                        "secret": True
                    },
                    {
                        "name": "MONGO_URL",
                        "value": "http://mongodb/",
                        "secret": True
                    }
                ]

            }
        ])

    mocker.patch("bulk.get_key_vault_for_environment")
    mocker.patch("bulk.add_variable_to_variables_file")

    add_variable_to_variables_file_spy = mocker.spy(bulk, "add_variable_to_variables_file")

    bulk.add(file_path)

    add_variable_to_variables_file_spy.assert_has_calls([
        mocker.call("test", "test", "MYSQL_URL", "http://localhost:3306", is_secret=False),
        mocker.call("test", "test", "MYSQL_PASS", "test-mysql-pass", is_secret=True),
        mocker.call("test", "test", "MONGO_URL", "test-mongo-url", is_secret=True)
    ])