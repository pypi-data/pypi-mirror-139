"""Custom test runners for mocking the KazooClient."""

from unittest import mock

from django.test.runner import DiscoverRunner

from kazoo_locks.tests.utils import FakeKazooClient


class KazooClientMockingTestRunner(DiscoverRunner):

    """Test runner that mocks the Kazoo client created with the kazoo_connection_manager."""

    def run_tests(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Mock the `_create_client` method while running tests."""
        with mock.patch('kazoo_locks.connection.kazoo_connection_manager._create_client', return_value=FakeKazooClient()):
            return super().run_tests(*args, **kwargs)
