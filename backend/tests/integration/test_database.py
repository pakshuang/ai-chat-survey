import unittest
from unittest.mock import MagicMock, patch
from src.app import database_operations
import pymysql


class TestDatabase(unittest.TestCase):
    @patch('src.app.database_operations.os.environ')
    @patch('src.app.database_operations.pymysql.connect')
    def test_connect_to_mysql(self, mock_connect, mock_environ):
        # Mock environment variables
        mock_environ.get.side_effect = lambda key, default: {
            "API_MYSQL_HOST": "mock_host",
            "API_MYSQL_USER": "mock_user",
            "API_MYSQL_PASSWORD": "mock_password",
            "API_MYSQL_DB": "mock_db"
        }.get(key, default)

        # Call the function
        connection = database_operations.connect_to_mysql()

        # Assert that pymysql.connect was called with the expected arguments
        mock_connect.assert_called_once_with(
            host='mock_host',
            user='mock_user',
            password='mock_password',
            database='mock_db',
            cursorclass=pymysql.cursors.DictCursor  # Use the actual cursor class
        )

        # Assert that the connection is returned correctly
        self.assertEqual(connection, mock_connect.return_value)

    def test_get_cursor(self):
        # Create a mock connection
        mock_connection = MagicMock()

        # Call the function
        cursor = database_operations.get_cursor(mock_connection)

        # Assert that cursor is retrieved from the connection
        mock_connection.cursor.assert_called_once_with()

        # Assert that the cursor is returned correctly
        self.assertEqual(cursor, mock_connection.cursor.return_value)

    def test_close_connection(self):
        # Create a mock connection
        mock_connection = MagicMock()

        # Call the function
        database_operations.close_connection(mock_connection)

        # Assert that connection close method is called
        mock_connection.close.assert_called_once()

    @patch('src.app.database_operations.commit')
    def test_commit(self, mock_commit):
        # Create a mock connection
        mock_connection = MagicMock()

        # Call the function
        database_operations.commit(mock_connection)

        # Assert that commit function is called with the correct argument
        mock_commit.assert_called_once_with(mock_connection)

    @patch('src.app.database_operations.rollback')
    def test_rollback(self, mock_rollback):
        # Create a mock connection
        mock_connection = MagicMock()

        # Call the function
        database_operations.rollback(mock_connection)

        # Assert that rollback function is called with the correct argument
        mock_rollback.assert_called_once_with(mock_connection)

    def test_execute(self):
        # Mock cursor
        mock_cursor = MagicMock()

        # Create a mock connection
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Call the function
        database_operations.execute(mock_connection, "SELECT * FROM table")

        # Assert that execute method is called on cursor with correct arguments
        mock_cursor.execute.assert_called_once_with("SELECT * FROM table", None)

        # Assert that commit is called on the connection
        mock_connection.commit.assert_called_once()

    def test_fetch(self):
        # Mock cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'column1': 'value1'}, {'column2': 'value2'}]

        # Create a mock connection
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Call the function
        result = database_operations.fetch(mock_connection, "SELECT * FROM table")

        # Assert that execute method is called on cursor with correct arguments
        mock_cursor.execute.assert_called_once_with("SELECT * FROM table", None)

        # Assert that fetchall is called on cursor
        mock_cursor.fetchall.assert_called_once()

        # Assert that result is returned correctly
        self.assertEqual(result, [{'column1': 'value1'}, {'column2': 'value2'}])

    def test_close_cursor(self):
        # Mock cursor
        mock_cursor = MagicMock()

        # Call the function
        database_operations.close_cursor(mock_cursor)

        # Assert that close method is called on cursor
        mock_cursor.close.assert_called_once()

