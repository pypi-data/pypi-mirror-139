"""Tests for the KazooConnectionManager class."""

from unittest import mock

from kazoo.exceptions import ConnectionClosedError

from django.test import TestCase

from kazoo_locks.connection import kazoo_connection_manager

from .utils import FakeKazooClient


class KazooConnectionManagerTestCase(TestCase):

    """Test the KazooConnectionManager."""

    def test_context_manager(self):
        """Test that the context manager interface of the manager has correct is_managed property."""
        self.assertFalse(kazoo_connection_manager.is_managed)
        with kazoo_connection_manager:
            self.assertTrue(kazoo_connection_manager.is_managed)
        self.assertFalse(kazoo_connection_manager.is_managed)

    def test_nesting_context_manager(self):
        """Test that the is_manager property has a proper value when nesting context managers."""
        with kazoo_connection_manager:
            with kazoo_connection_manager:
                self.assertTrue(kazoo_connection_manager.is_managed)
            self.assertTrue(kazoo_connection_manager.is_managed)
        self.assertFalse(kazoo_connection_manager.is_managed)

    def test_decorator(self):
        """Test that the decorator interface of the manager has correct is_managed property."""
        @kazoo_connection_manager
        def some_function():
            """Just assert that the is_manager property is True."""
            self.assertTrue(kazoo_connection_manager.is_managed)
        self.assertFalse(kazoo_connection_manager.is_managed)
        some_function()
        self.assertFalse(kazoo_connection_manager.is_managed)

    def test_getting_client_out_of_context(self):
        """Test that getting a client out of the manager context raises an AssertionError."""
        self.assertFalse(kazoo_connection_manager.is_managed)
        with self.assertRaises(AssertionError) as cm:
            kazoo_connection_manager.get_client()
        self.assertFalse(kazoo_connection_manager.has_client)
        self.assertTupleEqual(
            cm.exception.args,
            ('Use the kazoo_locks.connection.KazooConnectionManager as a context manager or decorator.', )
        )

    def test_getting_client(self):
        """Test that using the connection manager creates and connects the KazooClient when necessary."""
        fake_client = FakeKazooClient()
        with mock.patch('kazoo_locks.locks.kazoo_connection_manager._create_client', return_value=fake_client), \
                mock.patch.object(fake_client, 'start', wraps=fake_client.start) as start_mock:
            with kazoo_connection_manager:
                client = kazoo_connection_manager.get_client()
                self.assertIs(client, fake_client)
                self.assertTrue(kazoo_connection_manager.has_client)
                self.assertTrue(fake_client.started)
                kazoo_connection_manager.get_client()
                with kazoo_connection_manager:
                    self.assertTrue(kazoo_connection_manager.has_client)
                    self.assertTrue(fake_client.started)
                    kazoo_connection_manager.get_client()
                self.assertTrue(fake_client.started)
                start_mock.assert_called_once()
            self.assertFalse(fake_client.started)
            with kazoo_connection_manager:
                kazoo_connection_manager.get_client()
            start_mock.assert_has_calls([mock.call(), mock.call()])

    def test_restarting_client(self):
        """Test that connection is restarted on ConnectionClosedError when it's needed."""
        fake_client = FakeKazooClient()
        with mock.patch('kazoo_locks.locks.kazoo_connection_manager._create_client', return_value=fake_client), \
                mock.patch.object(fake_client, 'restart', wraps=fake_client.restart) as restart_mock:
            with self.assertRaises(ConnectionClosedError):
                with kazoo_connection_manager:
                    kazoo_connection_manager.get_client()
                    raise ConnectionClosedError()
            restart_mock.assert_not_called()

            with self.assertRaises(ConnectionClosedError):
                with kazoo_connection_manager:
                    with kazoo_connection_manager:
                        raise ConnectionClosedError()
            restart_mock.assert_not_called()

            with self.assertRaises(ConnectionClosedError):
                with kazoo_connection_manager:
                    with kazoo_connection_manager:
                        kazoo_connection_manager.get_client()
                        raise ConnectionClosedError()
            restart_mock.assert_called_once()

