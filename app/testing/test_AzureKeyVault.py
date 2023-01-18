from AzureKeyVault import AzureKeyVault

def test_get_secret_key_vault_reference_returns_correct_reference():
    key_vault = AzureKeyVault("https://example.com")
    secret_name = "my-secret"
    expected_value = "@Microsoft.KeyVault(SecretUri=https://example.com/secrets/my-secret/)"

    actual_value = key_vault.get_secret_key_vault_reference("my-secret")

    assert actual_value == expected_value