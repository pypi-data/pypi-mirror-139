"""Test cases for the migrate_with_kazoo management command."""
from io import StringIO

from mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.test.testcases import TestCase

from kazoo_locks.locks import Lock
from kazoo_locks.management.commands import migrate_with_kazoo


@patch('sys.stdout', StringIO())
class MigrateWithKazooCommandTestCase(TestCase):

    """Test case for the migrate_with_kazoo management command."""

    @override_settings(ZOOKEEPER_HOSTS=['localhost'])
    @patch('kazoo_locks.management.commands.migrate_with_kazoo.MigrationExecutor', return_value=None, side_effect=ImproperlyConfigured)
    @patch('kazoo_locks.management.commands.migrate_with_kazoo.nullcontext')
    @patch('django.core.management.commands.migrate.Command.handle', return_value=None)
    def test_using_default_lock(self, base_command_mocked, nullcontext_mocked, executor_mocked):
        command = migrate_with_kazoo.Command()
        self.assertEqual(command.lock.key, 'migrations')
        command.handle()
        nullcontext_mocked.assert_not_called()
        base_command_mocked.assert_called_once()

    @override_settings(ZOOKEEPER_HOSTS=['localhost'])
    @patch('kazoo_locks.management.commands.migrate_with_kazoo.MigrationExecutor', return_value=None, side_effect=ImproperlyConfigured)
    @patch('kazoo_locks.management.commands.migrate_with_kazoo.nullcontext')
    @patch('django.core.management.commands.migrate.Command.handle', return_value=None)
    def test_using_provided_lock(self, base_command_mocked, nullcontext_mocked, executor_mocked):
        lock = Lock('test-lock')
        command = migrate_with_kazoo.Command(lock=lock)
        self.assertEqual(command.lock, lock)
        command.handle()
        nullcontext_mocked.assert_not_called()
        base_command_mocked.assert_called_once()

    @patch('kazoo_locks.management.commands.migrate_with_kazoo.MigrationExecutor', return_value=None, side_effect=ImproperlyConfigured)
    @patch('kazoo_locks.management.commands.migrate_with_kazoo.nullcontext')
    @patch('django.core.management.commands.migrate.Command.handle', return_value=None)
    def test_using_nullcontext(self, base_command_mocked, nullcontext_mocked, executor_mocked):
        command = migrate_with_kazoo.Command()
        command.handle()
        nullcontext_mocked.assert_called_once()
        base_command_mocked.assert_called_once()

    @patch('kazoo_locks.management.commands.migrate_with_kazoo.MigrationExecutor.migration_plan', return_value=False)
    @patch('kazoo_locks.management.commands.migrate_with_kazoo.Command.launched_with_defaults', return_value=True)
    @patch('django.core.management.commands.migrate.Command.handle')
    def test_without_unapplied_migrations(self, base_command_mocked, *other_mocks):
        command = migrate_with_kazoo.Command()
        command.handle()
        base_command_mocked.assert_not_called()
