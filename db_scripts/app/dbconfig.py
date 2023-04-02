import os
import argparse
from configparser import ConfigParser

# Get the database configuration from the database.ini file


def config_ini(filename="database.ini", section='postgresql') -> dict:
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return db

# Get config from command line arguments


def config_params() -> dict:
    # read host, database, user, password script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-h", "-H", "--host", type=str, help="Database host")
    parser.add_argument("-d", "-D", "--database", type=str, default="postgres")
    parser.add_argument("-u", "-U", "--user", type=str, default="postgres")
    parser.add_argument("-p", "-P", "--password", type=str)
    args = parser.parse_args()

    return {
        "host": args.host,
        "database": args.database,
        "user": args.user,
        "password": args.password
    }


def config_env() -> dict:
    return {
        "host": os.environ.get("DB_HOST"),
        "database": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASS"),
    }


if __name__ == "__main__":
    # Check if environment variables are set
    env_vars_found = True
    env_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASS"]
    for var in env_vars:
        if os.environ.get(var) is None:
            print(f"Environment var {var} not set, looking for database.ini")
            env_vars_found = False
            break
    if env_vars_found:
        config = config_env()
    else:
        config = config_ini()
    print(config)
