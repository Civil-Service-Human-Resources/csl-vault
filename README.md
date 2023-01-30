# Civil Service Learning Vault

[![Run unit tests](https://github.com/Civil-Service-Human-Resources/csl-vault/actions/workflows/run-tests.yml/badge.svg?branch=main)](https://github.com/Civil-Service-Human-Resources/csl-vault/actions/workflows/run-tests.yml)

Manage variables and secrets for Civil Service Learning apps.

* [Initial setup](#initial-setup)
    * [Using Docker](#using-docker)
    * [Without Docker](#without-docker)
* [The `vault` command](#using-the-vault-command)
    * [Add a new variable](#add-a-new-variable)
    * [Update a variable](#update-a-variable)
    * [Delete a variable](#delete-a-variable)
    * [Add multiple variables](#add-multiple-variables)
    * [Load a variable to the App Service](#load-a-variable-to-the-app-service)
    * [Bulk load variables to the App Services](#bulk-load-variables-to-the-app-services)
    * [Sync a variable from an App Service](#sync-a-variable-from-an-app-service)

## Initial setup

### Using Docker

The easiest way to run this app is by running it within a Docker container, as you won't need anything else installed.

Once you've cloned the repository, run this command to initialise the container:

```sh
./initial-setup.sh
```

This command will:

* Log you in to Azure. It will first attempt to find if an `.azure` directory exists in your project. If not, it will attempt to get credentials from your host system. If neither of these exist, it will prompt you to log in by visiting a URL and pasting the code provided.
* Then it will create an image `csl-vault` with Azure, Python and all the necessary Python packages installed.

To run the container, enter this command:

```sh
./open-container.sh
```

This will run an instance of the `csl-vault` container, ready to run commands on.

### Without Docker

If you'd rather run this app without a container, you'll need these installed:

* [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
* [Python 3.10 or higher](https://www.python.org/downloads/)

Then run these to initialise the app:

```sh
az login
pip install -r requirements.txt
alias vault="python vault.py"
```

## Using the `vault` command

To add, update or delete variables, you'll be using the `vault` command within the repo's root directory. It's basically an alias of `python vault.py`:

```sh
vault <action> <environment> <module> <variableName> [--value <variableValue>] [--secret]
```

These are the arguments:

* `action`: what to perform: `add`, `update` or `delete`
* `environment`: the environment the variable belongs to. For example `integration`
* `module`: the app service the variable belongs to. For example `identity`, `lpg-ui`
* `variableName`: the name of the variable
* `--value` (optional): the value of the field. If this isn't specified, the app will prompt you to add the value. *Only accepted for the `add` and `update` actions*
* `--secret` (optional): add this flag to specify that this is a sensitive variable that should be added to the KeyVault. *This is only accepted for the `add` action*

### Add a new variable

To add a new variable, use the `vault add` command:

#### Add a non-sensitive variable:

Non-sensitive (non-secret) variables will be only be added in the JSON file for the specified environment and module and not uploaded to the KeyVault:

```sh
vault add <environment> <module> <variableName> [--value <variableValue>]
```

For example, to add a variable called `MYSQL_URL` with value `http://localhost:3306` for the `identity` service in `integration` environment:

```sh
vault add integration identity MYSQL_URL --value http://localhost:3306
```

or you can use this command without the `--value` flag:

```sh
vault add integration identity MYSQL_URL
```

which will prompt you to add the variable:

```
vault add integration identity MYSQL_URL
Enter value for variable 'MYSQL_URL': 
```

#### Add a sensitive variable (secret)

To add a sensitive variable, you can use the `--secret` flag:

```sh
vault add --secret <environment> <module> <variableName> [--value <variableValue>]
```

For example, to add a variable called `MYSQL_PASS` with value `password1` for the `identity` service in `integration` environment:

```sh
vault add --secret integration identity MYSQL_URL
```

This will prompt you to add the secret value:

```
Enter value for variable 'MYSQL_PASS': 
```

If you'd rather add the secret value within the command (not recommended for secrets), use the `--value` flag:

```
vault add --secret integration identity MYSQL_PASS --value my-secret-pw
```

This variable will be added to the KeyVault for the specific environment.

### Update a variable

To update a variable, use the `vault update` command:

```sh
vault update <environment> <module> <variableName> [--value <newVariableValue>]
```

For example:

```sh
vault update integration identity MYSQL_PASS --value password2
```

or without the `--value` argument:

```sh
vault update integration identity MYSQL_PASS
```

which, will prompt you to enter the value.

⚠️ The `--secret` flag is not needed for updating

### Delete a variable

To delete a variable, use the `vault delete` command:

```sh
vault delete <environment> <module> <variableName>
```

For example:

```sh
vault delete integration identity MYSQL_USER
```

⚠️ The `--secret` flag is not needed for deleting

### Add multiple variables

To add multiple variables, you'll first need to create a JSON file, structured like this:

```json
[
    {
        "environment": "integration",
        "module": "mysql",
        "values":[
            {
                "name": "MYSQL_URL",
                "value": "http://localhost:3306",
                "secret": false
            },
            {
                "name": "MYSQL_PASS",
                "value": "password1",
                "secret": true
            }
        ]

    },
    {
        "environment": "integration",
        "module": "learning-catalogue",
        "values":[
            {
                "name": "ES_URL",
                "value": "http://cloud.elastic.co/my-server",
                "secret": false
            },
            {
                "name": "ES_PASS",
                "value": "password2",
                "secret": true
            }
        ]

    }
]
```

Then, to execute the bulk add, use the `vault bulk-add` command like so:

```sh
vault bulk-add <filePath>
```

### Load a variable to the App Service

Use the `load` action to load a variable specified previously into an the configuration properties of an App Service.

```
vault load <environment> <module> <variableName>
```

This will load the variable value if it's a non-secret variable, or its Key Vault reference if it's a secret.

Example:

```
vault load integration identity DB_URL
```

### Bulk load variables to the App Services

Use the `bulk-load` command to compare the variables you have locally with the variables currently in your App Services:

```sh
vault bulk-load <environment>
```

For example:

```sh
vault bulk-load integration
```

This command will scan through all the App Services in the `integration` environment and compare its variables with the variables you have stored in your JSON files. If there are any changes:

```
====== lpg-ui ========
CONTENT_URL: https://example.com
In app service: https://example.com
✅ Variable in sync. No change required.

CONTACT_EMAIL: support@governmentcampus.co.uk
In app service: support-new@governmentcampus.co.uk
🔼 Variable is not in sync.

REDIS_PASSWORD: my-redis-pw
🔵 Variable not in 'lpg-ui'. It will be added.
```

### Sync a variable from an App Service

Use the `sync` action to get a variable from an App Service and update the local JSON files:

💡 `sync` can only update non-secret variables.

```
vault sync <environment> <module> <variableName>
```

Example:

```
vault sync integration identity MY_DB
```