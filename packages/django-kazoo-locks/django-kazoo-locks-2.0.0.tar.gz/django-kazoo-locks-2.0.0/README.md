Django Kazoo Locks
==================

![example workflow](https://github.com/innovationinit/django-kazoo-locks/actions/workflows/test-package.yml/badge.svg?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/innovationinit/django-kazoo-locks/badge.svg)](https://coveralls.io/github/innovationinit/django-kazoo-locks)

About
-----

[Django Kazoo
Locks](https://github.com/innovationinit/django-kazoo-locks) provides a
utils for using Zookeeper locks through kazoo in
[Django](https://www.djangoproject.com) applications.

Install
-------

```bash
pip install django-kazoo-locks
```

Usage
-----

Register app in `INSTALLED_APPS` and define following settings:

```python
ZOOKEEPER_APP_NAMESPACE = 'some-unique-app-name'
ZOOKEEPER_HOSTS = ['10.32.96.201:2181']
```

Usage example:

```python
lock = Lock('my-lock-{object_id}')
with lock(object_id=123):
    print('so alone')

try:
    with lock(object_id=123, timeout=9):
        print('so alone')
except LockTimeout:
    print('unable to lock after waiting for 9s')

try:
    with lock(object_id=123, blocking=False):
        print('so alone')
except Locked:
    print('unable to lock immediately')
```

Extras
------

Migrations
----------

This package defines its version of the data migration command -
`migrate_with_kazoo`. Thanks to this command it is possible to quickly
and correctly perform data migration process in applications running
simultaneously on many different hosts and using the same database. The
command can be used independently or as a base class for the migrate
command in your own application. The `__init__` method of the defined
class accepts the optional `lock` argument, which allows you to define
your own `kazoo_locks.locks.Lock` object to protect the critical section
of the migration.

License
-------

The Django Kazoo Locks package is licensed under the [FreeBSD
License](https://opensource.org/licenses/BSD-2-Clause).
