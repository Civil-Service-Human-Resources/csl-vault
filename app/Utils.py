def get_keyvault_secret_id_from_variable_name(module, variable_name):
    return module + "-" + variable_name.replace("_", "-").lower()