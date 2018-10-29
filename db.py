class MemDB:
    
    def __init__(self):
        self.disk = {}
        self.dirty = {} # items not committed to disk yet
        self.log = list() # maintains state/changes during transactions
        self.trans_count = 0

    def set(self, key, value):
        if self.trans_count == 0:
            self.disk[key] = value
        else:
            if key in self.dirty:
                self.log.append((key, self.dirty.get(key), value)) # (key, oldvalue, newvalue)
            else:
                self.log.append((key, self.disk.get(key), value))
            self.dirty[key] = value

    def get(self, key):
        if key in self.dirty:
            return self.dirty[key]
        return self.disk.get(key, None)

    def remove(self, key):
        if self.trans_count == 0:
            del self.disk[key]
        else:
            if key in self.dirty:
                self.log.append((key, self.dirty.get(key), None))
            else:
                self.log.append((key, self.disk.get(key), None))
            self.dirty[key] = None

    def begin(self):
        """
        Opens a new transaction block. Transaction blocks can be nested. Any data command run outside
        of a transaction block committed immediately. 
        """
        self.log.append("BEGIN")
        self.trans_count += 1

    def rollback(self):
        """
        Undo all commands in most recent transaction block and close block.
        """
        if self.trans_count == 0:
            return "NO TRANSACTION"

        cur = self.log.pop()
        while cur != "BEGIN":
            key, old, new = cur
            self.dirty[key] = old
            cur = self.log.pop()

        self.trans_count -= 1

    def commit(self):
        """
        Closes all open transaction blocks and commits all changes to disk.
        """
        if self.trans_count == 0:
            return "NO TRANSACTION"

        for key in self.dirty:
            value = self.dirty[key]
            if value == None:
                del self.disk[key]
            else:
                self.disk[key] = value

        self.trans_count = 0
        self.log.clear()
        self.dirty.clear()
