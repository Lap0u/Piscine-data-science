import psycopg2
from sqlalchemy import create_engine
import pandas as pd


def connect_to_database():
    conn = psycopg2.connect(
        database="piscineds",
        user="cbeaurai",
        host="localhost",
        password="mysecretpassword",
        port=5432,
    )
    return conn


def create_database(conn):
    cur = conn.cursor()
    conn.set_session(autocommit=True)

    cur.execute("CREATE DATABASE python_database")

    # Commit the changes and close the connection to the default database
    conn.commit()
    cur.close()
    conn.close()


def create_table(path, engine):
    table_name = path.split("/")[-1].split(".")[0]
    df = pd.read_csv(path)
    df.to_sql(table_name, engine, if_exists="replace", index=False)


def main():
    conn = connect_to_database()
    create_database(conn)
    engine = create_engine(
        "postgresql://cbeaurai:mysecretpassword@localhost:5432/python_database"
    )
    create_table("./customer/data_2022_dec.csv", engine)


if __name__ == "__main__":
    main()
