"""Multiprocessing hooks."""
from multiprocessing.util import Finalize

from kazoo_locks.connection import kazoo_connection_manager


def kazoo_multiprocessing_connection_initializer():
    """Kazoo multiprocessing connection initializer. Connection will not be closed on an raise of unhandled exception"""
    kazoo_connection_manager.start_context()
    Finalize(kazoo_connection_manager, kazoo_connection_manager.stop_context, exitpriority=16)
