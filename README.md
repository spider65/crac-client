# crac-client
Client for connection to crac-server via gRPC

# Install Dependencies and Configure environment

We are using Poetry as a dependency management and packaging
Go to https://python-poetry.org/ and install it

Before using this project, you should clone the crac-protobuf project 
alongside this one so that the dependency expressed on pyprject.toml 
can find the package to install.

```
poetry shell
poetry install
```

# Execute the service

You can start the gui client with:

```
cd crac_client
python app.py
```
