import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

def connect_to_database():
    """Connect to the default database and return the connection object."""
    conn = psycopg2.connect(
        database="python_db10",
        user="cbeaurai",
        host="localhost",
        password="mysecretpassword",
        port=5432,
    )
    return conn

def get_dataframe(conn):
    """Retrieve the dataset from the database and return it as a DataFrame."""
    cur = conn.cursor()
    cur.execute("SELECT event_type, COUNT(*) FROM customers GROUP BY event_type;")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["event_type", "count"])
    cur.close()
    conn.close()
    return df

def plot_pie(df):
    """Plot a pie chart of the dataset."""
    print(df)
    _, ax = plt.subplots()
    ax.pie(df["count"], labels=df["event_type"], autopct="%1.1f%%")
    plt.show()

def main():
    """Create a new database and tables with data from the customer folder"""
    conn = connect_to_database()
    df = get_dataframe(conn)
    plot_pie(df)

if __name__ == "__main__":
    main()