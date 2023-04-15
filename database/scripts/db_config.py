import os
import argparse
from configparser import ConfigParser


def config_ini(filename="database.ini", section="postgresql") -> dict:
    """Reads the database.ini file and returns a dictionary
    with the database configuration

    ...
    :param filename: Name of the database.ini file
    :type filename: str
    :param section: Section of the database.ini file
    :type section: str
    ...
    :raises Exception: Section not found in the database.ini file
    ...
    :return: Database configuration
    :rtype: dict
    """
    parser = ConfigParser()
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
    """Reads the command line arguments and
    returns a dictionary with the database configuration

    ...
    :return: Database configuration
    :rtype: dict
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-h", "-H", "--host", type=str, help="Database host")
    parser.add_argument("-d", "-D", "--database", type=str, default="postgres")
    parser.add_argument("-u", "-U", "--user", type=str, default="postgres")
    parser.add_argument("-P", "--password", type=str)
    parser.add_argument("-p", "--port", type=str, default="5432")
    args = parser.parse_args()

    return {
        "host": args.host,
        "password": args.port,
        "database": args.database,
        "user": args.user,
        "password": args.password,
    }


def config_env() -> dict:
    """Reads the environment variables and
    returns a dictionary with the database configuration

    ...
    :return: Database configuration
    :rtype: dict
    """
    return {
        "host": os.environ.get("POSTGRES_HOST"),
        "password": os.environ.get("POSTGRES_PORT"),
        "database": os.environ.get("POSTGRES_DB"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
    }


if __name__ == "__main__":
    # Check if environment variables are set
    env_vars_found = True
    env_vars = [
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    ]
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
