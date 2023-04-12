# DB Scripts

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites-for-running-the-scripts)
3. [Scripts](#scripts)
4. [Editing the database](#editing-the-database-schema)

## Introduction

DB Scripts is a collection of scripts that help you manage a PostgreSQL database. The scripts use the [psycopg2](https://pypi.org/project/psycopg2/) library to connect to the database and execute SQL queries.

## Prerequisites for running the scripts

1. To run these scripts, you need set your credentials either in the enviroment variables:

    ```powershell
    POSTGRES_HOST POSTGRES_NAME POSTGRES_USER POSTGRES_PASS
    ```

    script parameters:

    ```powershell
    python3 <script_name>.py --host <host> --name <name> --user <user> --pass <pass>
    ```

    or in the [database.ini](scripts) file.

2. Enter the [app](/scripts/app) folder in a terminal.
3. Create and activate a python virtual environment and install requirements from the [requirements.txt](../requirements.txt) file.

On GNU/Linux or macOS, run the following commands in the terminal:

```bash
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On Windows, run the following commands in the Powershell terminal:

```powershell
python3 -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Scripts

The available scripts provide convenient functions to develop apps. To run them head to the [scripts](scripts) folder and type the following command:

```bash
python3 <script_name>.py
```

. The scripts are located in the [scripts](scripts) folder are:

1. [dbconnect.py](scripts/dbconnect.py) - connects to the database and returns the connection object, and also takes an optional config parameter for using in an app
2. [dbcreate.py](scripts/dbcreate.py) - creates the database and tables
3. [dbshow.py](scripts/dbshow.py) - shows tables in the database
4. [dbdelete.py](scripts/dbdelete.py) - drops the database and tables (use with caution)

## Editing the database schema

To make changes to the database schema, change both the [dbdelete.sql](definitions/dbdelete.sql) and [dbschema.sql](definitions/dbschema.sql) files. Then run the [dbdelete.sql](definitions/dbdelete.sql) and [dbcreate.py](definitions/dbcreate.py) scripts.
