from AppServiceProperties import AppServiceProperties

def test_get_property_value_returns_correct_value_from_app_service(mocker):
    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_app_properties',
        return_value={
            "MY_VAR": "MyValue",
            "MY_VAR2": "MySecondValue"
        }
    )

    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_web_client'
    )

    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_application_settings'
    )

    app_service_properties = AppServiceProperties("sub1", "resource1", "app1")
    
    expected_property_value = "MyValue"
    actual_value = app_service_properties.get_property_value("MY_VAR")

    assert actual_value == expected_property_value
    
def test_property_exists_in_app_service_returns_true_if_property_exists_in_app_service(mocker):
    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_app_properties',
        return_value={
            "MY_VAR": "MyValue",
            "MY_VAR2": "MySecondValue"
        }
    )

    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_web_client'
    )

    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_application_settings'
    )

    app_service_properties = AppServiceProperties("sub1", "resource1", "app1")

    expected_value = True
    actual_value = app_service_properties.property_exists_in_app_service("MY_VAR")

    assert actual_value == expected_value

def test_property_exists_in_app_service_returns_false_if_property_does_not_exist_in_app_service(mocker):
    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_app_properties',
        return_value={
            "MY_VAR": "MyValue",
            "MY_VAR2": "MySecondValue"
        }
    )

    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_web_client'
    )

    mocker.patch(
        'AppServiceProperties.AppServiceProperties.get_application_settings'
    )

    app_service_properties = AppServiceProperties("sub1", "resource1", "app1")

    expected_value = False
    actual_value = app_service_properties.property_exists_in_app_service("ANOTHER_VAR")

    assert actual_value == expected_value
