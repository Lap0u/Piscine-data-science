import psycopg2
from sqlalchemy import create_engine, DateTime, Float, Integer
from sqlalchemy import String, BigInteger, Uuid
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
    """Create a new database called python_db3."""
    cur = conn.cursor()
    conn.set_session(autocommit=True)

    cur.execute("CREATE DATABASE python_db3")

    # Commit the changes and close the connection to the default database
    conn.commit()
    cur.close()
    conn.close()


def main():
    """Create a new database and tables with data from the customer folder"""
    conn = connect_to_database()
    create_database(conn)
    engine = create_engine(
        "postgresql://cbeaurai:mysecretpassword@localhost:5432/python_db3"
    )
    type = {
        "event_time": DateTime,
        "event_type": String,
        "product_id": Integer,
        "price": Float,
        "user_id": BigInteger,
        "user_session": Uuid,
    }
    files = [f for f in os.listdir("./customer") if f.endswith(".csv")]
    print(files)
    df = pd.DataFrame()
    for file in files:
        complete_path = f"./customer/{file}"
        curr_df = pd.read_csv(complete_path)
        df = pd.concat([df, curr_df])
    print(df, df.shape)
    df.drop_duplicates(keep='first', inplace=True)
    print(df, df.shape)
    df.to_sql("customers", engine, if_exists="replace", index=False, dtype=type, chunksize=1000000)


if __name__ == "__main__":
    main()
