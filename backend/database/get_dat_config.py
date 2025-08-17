import json
from typing import Union

DATABASE_CONFIG_PATH = "database_config.json"
DATABASE_CONFIG_HOSTNAME = "hostname"
DATABASE_CONFIG_DATABASENAME="database"
DATABASE_CONFIG_USERNAME = "user"
DATABASE_CONFIG_DATABASEPASSWORD = "password"
DATABASE_CONFIG_PORT = "port"

class Config:
    hostname: Union[str, None]
    database: Union[str, None]
    user: Union[str, None]
    password: Union[str, None]
    port: Union[str, None]


    def __init__(self):
        self.hostname = None
        self.database = None
        self.user = None
        self.password = None
        self.port = None

def get_config() -> Config:
    data = Config()
    with open(DATABASE_CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)

    data.hostname = config[DATABASE_CONFIG_HOSTNAME]
    data.database = config[DATABASE_CONFIG_DATABASENAME]
    data.user = config[DATABASE_CONFIG_USERNAME]
    data.password = config[DATABASE_CONFIG_DATABASEPASSWORD]
    data.port = config[DATABASE_CONFIG_PORT]

    return data
