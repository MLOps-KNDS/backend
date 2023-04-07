import os
import psycopg2


async def delete_db(conn: psycopg2.extensions.connection) -> dict:
    """Deletes tables specified in dbdelete.sql
    Keyword arguments:
    conn -- psycopg2 connection object
    """
    # Check if schema file exists
    file_path = "../db/dbdelete.sql"
    if os.path.exists(file_path):
        # Read schema
        with open(file_path, "r") as file:
            query = file.read()
    else:
        file_name = file_path.split("/")[-1]
        return {"status": "error", "message": f"{file_name} not found"}
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return {"status": "ok"}


if __name__ == "__main__":
    import asyncio
    import dbconnect
    conn = dbconnect.connect()
    response = asyncio.run(delete_db(conn))
    conn.close()
    print(response)
