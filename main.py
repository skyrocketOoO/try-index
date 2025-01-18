import mysql.connector
from mysql.connector import Error
import config
import itertools
import subprocess
import json
import csv

def connect_to_mysql(host, database, user, password):
    """
    Connects to a MySQL database and returns the connection object.

    :param host: The host of the MySQL server (e.g., 'localhost' or an IP address).
    :param database: The name of the database to connect to.
    :param user: The username for the MySQL connection.
    :param password: The password for the MySQL connection.
    :return: Connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            print(f"You're connected to the database: {database}")
            return connection

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def close_connection(connection):
    """
    Closes the MySQL database connection.

    :param connection: The connection object to close.
    """
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")

# Example usage
if __name__ == "__main__":
    c = config.load_yaml(".env")
    db_config = c.get("db", {})
    host = db_config.get("host")
    database = "alarm_system"
    user = db_config.get("user")
    password = db_config.get("password")

    # Connect to the database
    conn = connect_to_mysql(host, database, user, password)

    # Perform operations if the connection is successful
    if not conn:
        print("Connection to MySQL failed.")
        exit()
    # Example: Create a cursor and execute a query
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    record = cursor.fetchone()
    print(f"You're connected to the database: {record}")

    table = c.get("table")
    indexes = c.get("indexes", [])
    all_permutations = []
    for length in range(1, len(indexes) + 1):
        all_permutations.extend(itertools.permutations(indexes, length))
    # print(all_permutations)
    
    for index in all_permutations:
        index_name = "idx_" + "_".join(index)
        index_columns = ", ".join(index)
        query = f"CREATE INDEX {index_name} ON {table} ({index_columns});"
        # print(query)
        cursor.execute(query)
        
        # Run the shell command
        result = subprocess.run(['k6', 'run', '--summary-export=result.json', 'index.js'], capture_output=True, text=True)

        # Print the output
        # print("STDOUT:", result.stdout)
        # print("STDERR:", result.stderr)
        
        with open('result.json') as f:
          data = json.load(f)
        open_alarm_times = data['metrics']['open_alarm_duration']['med']
        close_alarm_times = data['metrics']['close_alarm_duration']['med']
        suspend_alarm_times = data['metrics']['suspend_alarm_duration']['med']
        process_alarm_times = data['metrics']['process_alarm_duration']['med']
        
        with open('results.csv', mode='a', newline='') as file:
          writer = csv.writer(file)
          # Append the averaged data as a new row
          writer.writerow([open_alarm_times, close_alarm_times, suspend_alarm_times, process_alarm_times, index_name])
        
        query = f"DROP INDEX {index_name} ON {table};"
        cursor.execute(query)

    # Close the cursor and connection
    cursor.close()
    close_connection(conn)
