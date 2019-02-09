# In-Memory Datastore

`db.py` is a basic Python implementation of a transaction-based in-memory datastore, capable of storing key-value pairs.
All calls to `get(key)`, `set(key, value)` and `remove(key)` are recorded in the log of the respective transaction block, which is created by `begin()`. We can then persist the changes by `commit()` and forget about them through `rollback()`. This implementation supports nesting of transaction blocks.

The testing harness `test.py` runs the tests in the `/tests` directory.
