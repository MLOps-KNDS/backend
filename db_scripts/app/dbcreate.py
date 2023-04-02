import os
import psycopg2

"""Create all tables in the database if they don't exist"""


async def create_db(conn: psycopg2.extensions.connection) -> dict:
    cursor = conn.cursor()
    # Check if schema file exists
    file_path = "../db/dbschema.sql"
    file_name = file_path.split("/")[-1]

    if os.path.exists(file_path):
        # Read schema
        with open(file_path, "r") as file:
            query = file.read()
    else:
        cursor.close()
        return {"status": "error", "message": f"{file_name} not found"}

    try:
        cursor.execute(query)
    except psycopg2.errors.DuplicateTable:
        cursor.close()
        return {"status": "error", "message": "Some tables already exist"}
    conn.commit()
    cursor.close()
    return {"status": "ok"}

if __name__ == "__main__":
    import asyncio
    import dbconnect
    conn = dbconnect.connect()
    response = asyncio.run(create_db(conn))
    conn.close()
    print(response)
