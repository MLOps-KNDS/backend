from sqlalchemy import Connection
from db_schema import Base
import sqlalchemy


async def create_db(conn: Connection) -> dict:
    """Creates all tables set in the dbschema.sql file

    ...
    :param conn: Database connection
    :type conn: Connection
    ...
    :raises sqlalchemy.exc.ProgrammingError: Some tables already exist
    ...
    :return: A dict with the status and an optional message
    :rtype: dict
    """

    try:
        Base.metadata.create_all(bind=conn)
    except sqlalchemy.exc.ProgrammingError:
        conn.close()
        return {"status": "error", "message": "sqlalchemy.exc.ProgrammingError"}
    conn.close()
    return {"status": "ok"}


if __name__ == "__main__":
    import asyncio
    import db_connect

    conn = db_connect.connect()
    response = asyncio.run(create_db(conn))
    conn.close()
    print(response)
