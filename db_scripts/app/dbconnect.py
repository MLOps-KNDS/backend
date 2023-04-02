import psycopg2
import dbconfig


def connect() -> psycopg2.extensions.connection:
    config = dbconfig.config()

    conn = psycopg2.connect(**config)
    if conn:
        return conn
    else:
        raise Exception("Connection failed")


if __name__ == "__main__":
    conn = connect()

    # get postgresql version
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print(f"Connected to {record}")

    # close the connection
    cursor.close()
    conn.close()
