# python-lib-tmobile-poptoken-builder

## High Level structure of the code
This code bundle contains the following python files for example usage of Canvas API endpoints. 
`pop_util.py` module contains `access_token()` method is used to get the access token and PoP token based on the oauth endpoints, which are required for all the subsequent intereaction with apigee gateways. Once `access_token()` are executed, this function would return the access token with validity of 30min. This access token is required as `Bearer` authorization header
`create_pop()` is a function that returns the pop token for particular api endpoints. This pop token shoudl be used as x-authorization header. 
`common_var.py` is the shared variables modules which are used in the functions in the module

## Usage 
First, you would need to install the following dependencies in your python runtime env. It's recommend to use virtualenv for this if you are running in a local development environment. 
```
# navigate to the directory desired and create virtual env
python3 -m venv pop-env

# activate the virtualenv
source pop-env/bin/activate
```
Following dependencies should be installed using pip within the python env
```
pip install PyJWT
pip install cryptography
```

Once all the dependencies are installed in the virtualenv, you would need to have the following required as well for running these modules
1. A location for python to read the public and private key for the vault apigee app. In this example it was read from a file, but pipeline can potentially leverage vault to read those info 
2. client ID and client secret should be loaded as python os env var. Again these can be loaded from vault if required

Simply modify and run `main.py` to execute the API call on the URI endpoints of interest