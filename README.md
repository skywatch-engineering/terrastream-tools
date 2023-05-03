
# Terrastream Tools

This repository contains the Python SDK and CLI tools for Terrastream. This is a tool suite designed to facilitate developer integration with the Terrastream platform.


## Contents
---

The contents of this repository are:

`cli/` - The CLI tool for Terrastream

`sdk/` - The Python SDK for Terrastream

## Pre-requisites
---
- Python 3.6 or higher
- Credentials (base api url, username and password) for Terrastream provided by an administrator

## Installation
---
To install the CLI tool, follow these steps:

1. Clone this repository to your local machine.
2. Run the following command to install the CLI dependencies:

```bash
cd cli/
make install
```

3. Prepare .tscfg file with your credentials and place it into the `/cli` folder. You can use the provided template:

```json
{
    "api_base_url": "https://api.provider.terrastream.ca",
    "api_username": "username",
    "api_password": "password"
}
```

## Usage
---

### TS-CLI
Currently these are the available commands through the cli:

- List available commands

```bash
python ts_cli/cli.py --help
```

- Create custom product and upload it to Terrastream

This command will submit the product payload to the api and the bundle file to the storage. The product payload must be a valid json file and the bundle file must be a zip file.

```bash
python ts_cli/cli.py create-custom-product --payload samples/custom_product_tasking.json --input-file samples/custom_product_bundle.zip
```


### TS-SDK
Currently there is no available operation for the SDK. It is only used by the CLI tool for now. However, you can install and import SDK modules into your own project. The SDK is not yet stable and is subject to change.


## Versions
---