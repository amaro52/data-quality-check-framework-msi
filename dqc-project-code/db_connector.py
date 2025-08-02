from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


'''
Creates an SQLAlchemy engine using a connection_string
connection_string [=] database connection string that is compatible with SQLAlchemy
Returns a database engine
'''
def create_db_engine(connection_string):
    try:
        engine = create_engine(connection_string)

        # test connection immediately to get errors quickly
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return engine
    except SQLAlchemyError as e:
        raise e