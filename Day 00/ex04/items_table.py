import psycopg2
from sqlalchemy import create_engine, String, BigInteger
import pandas as pd
import os


def connect_to_database():
    """Connect to the default database and return the connection object."""
    conn = psycopg2.connect(
        database="piscineds",
        user="cbeaurai",
        host="localhost",
        password="mysecretpassword",
        port=5432,
    )
    return conn


def create_database(conn):
    """Create a new database called python_db_3."""
    cur = conn.cursor()
    conn.set_session(autocommit=True)

    cur.execute("CREATE DATABASE python_db_3")

    # Commit the changes and close the connection to the default database
    conn.commit()
    cur.close()
    conn.close()


def create_table(path, engine, type):
    """Create a table in the database with the data from the CSV file."""
    table_name = "items"
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists="replace", index=False, dtype=type)


def main():
    """Create a new database and tables with data from the items folder"""
    conn = connect_to_database()
    create_database(conn)
    engine = create_engine(
        "postgresql://cbeaurai:mysecretpassword@localhost:5432/python_db_3"
    )
    type = {
        "product_id": BigInteger,
        "category_id": BigInteger,
        "category_code": String,
        "brand": String,
    }
    create_table("./items/item.csv", engine, type)


if __name__ == "__main__":
    main()
