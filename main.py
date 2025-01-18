import mysql.connector
from mysql.connector import Error

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
    host = "localhost"
    database = "your_database_name"
    user = "your_username"
    password = "your_password"

    # Connect to the database
    conn = connect_to_mysql(host, database, user, password)

    # Perform operations if the connection is successful
    if conn:
        # Example: Create a cursor and execute a query
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"You're connected to the database: {record}")

        # Close the cursor and connection
        cursor.close()
        close_connection(conn)
