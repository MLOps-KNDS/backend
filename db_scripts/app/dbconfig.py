from configparser import ConfigParser

""" Get the database configuration from the database.ini file """


def config(filename="database.ini", section='postgresql') -> dict:
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


if __name__ == "__main__":
    print(config())
