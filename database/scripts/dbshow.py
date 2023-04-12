import psycopg2


async def show_db(conn: psycopg2.extensions.connection) -> dict:
    """Shows all tables in the database

    ...
    :param conn: Database connection
    :type conn: psycopg2.extensions.connection
    ...
    :return: A dict with status and data
    :rtype: dict
    """
    cursor = conn.cursor()
    cursor.execute(
        """SELECT *
                    FROM pg_catalog.pg_tables
                    WHERE schemaname != 'pg_catalog' AND
                        schemaname != 'information_schema';"""
    )
    records = cursor.fetchall()
    cursor.close()
    return {"status": "ok", "data": records}


if __name__ == "__main__":
    import asyncio
    import dbconnect

    conn = dbconnect.connect()
    response = asyncio.run(show_db(conn))
    conn.close()
    print(response)
