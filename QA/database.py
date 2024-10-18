import mysql.connector
from mysql.connector import Error

def create_server_connection(host_name, user_name, user_password, database_name):
    """Create a connection to the MySQL server."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name,
            auth_plugin="mysql_native_password",
            buffered=True,
        )
        return connection
    except Error as err:
        print(f"Error: {err}")
        return None

def insert_question_answer(question, answer):
    """Insert question and answer into the MySQL database."""
    connection = create_server_connection("localhost", "root", "password", "qa_db")
    if connection:
        cursor = connection.cursor()
        insert_query = "INSERT INTO qa_table (question, answer) VALUES (%s, %s)"
        cursor.execute(insert_query, (question, answer))
        connection.commit()
        cursor.close()
        connection.close()