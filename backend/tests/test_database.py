from src.app import database_operations


class TestDatabase:
    def test_connection(self):
        # Establish a connection to the database
        conn = database_operations.connect_to_mysql()
        # Add an assert statement to check if connection is not None
        assert conn.open is True, "Connection to the database should be established"
        # Close the connection after all tests are done
        database_operations.close_connection(conn)
        assert conn.open is False, "Connection should be closed after all tests"

