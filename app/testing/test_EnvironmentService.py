from EnvironmentService import EnvironmentService

def test_get_environment_gets_specified_environment_data(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    environment_service = EnvironmentService()
    environment_data = environment_service.get_environment("test")

    assert environment_data["subscription"] == "CSL-Test"
    assert environment_data["resourceGroup"] == "lpgtest"
    assert environment_data["vault"] == "https://a-vault.vault.azure.net/"
    assert len(environment_data["modules"]) == 3

    assert environment_data["modules"]["module1"] == "test-module"
    assert environment_data["modules"]["module2"] == "test-module-2"
    
def test_environment_exists_returns_true_if_environment_is_present(mocker):
    mocker.patch(
        'EnvironmentService.EnvironmentService.get_environments_file',
        return_value=open("./testing/resources/environments.json").read()
    )

    environment_service = EnvironmentService()

    environment_exists = environment_service.environment_exists("test")

    assert environment_exists == True
