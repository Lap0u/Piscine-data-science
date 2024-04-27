import psycopg2
from sqlalchemy import create_engine, DateTime, Float, Integer
from sqlalchemy import String, BigInteger, Uuid
import pandas as pd


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
    """Create a new database called python_database."""
    cur = conn.cursor()
    conn.set_session(autocommit=True)

    cur.execute("CREATE DATABASE python_database")

    # Commit the changes and close the connection to the default database
    conn.commit()
    cur.close()
    conn.close()


def create_table(path, engine, type):
    """Create a table in the database with the data from the CSV file."""
    table_name = path.split("/")[-1].split(".")[0]
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists="replace", index=False, dtype=type)


def main():
    """Create a new database and a table with the data from the CSV file"""
    conn = connect_to_database()
    create_database(conn)
    engine = create_engine(
        "postgresql://cbeaurai:mysecretpassword@localhost:5432/python_database"
    )
    type = {
        "event_time": DateTime,
        "event_type": String,
        "product_id": Integer,
        "price": Float,
        "user_id": BigInteger,
        "user_session": Uuid,
    }
    create_table("./customer/data_2022_dec.csv", engine, type)


if __name__ == "__main__":
    main()
