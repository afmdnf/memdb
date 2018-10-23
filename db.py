class MemDB:

    def __init__(self):
        self.disk = {}
        self.dirty = {}
        self.log = list()
        self.transaction_cnt = 0

    def set(self, name, value):
        if self.transaction_cnt == 0:
            self.disk[name] = value
        else:
            if name in self.dirty:
                self.log.append((name, self.dirty.get(name), value))
            else:
                self.log.append((name, self.disk.get(name), value))
            self.dirty[name] = value

    def get(self, name):
        if name in self.dirty:
            return self.dirty[name]
        return self.disk.get(name, None)

    def unset(self, name):
        """
        Unset the variable name, making it just like that variable was never set.
        """
        if self.transaction_cnt == 0:
            del self.disk[name]
        else:
            if name in self.dirty:
                self.log.append((name, self.dirty.get(name), None))
            else:
                self.log.append((name, self.disk.get(name), None))
            self.dirty[name] = None

    def numWithValue(self, value):
        """
        Print out the number of variables that are currently set to value. 
        If no variables equal that value, print 0.
        """
        count = 0
        for name in self.dirty:
            if self.dirty[name] == value:
                count += 1
        for name in self.disk:
            if name not in self.dirty and self.disk[name] == value:
                count += 1
        return count

    def begin(self):
        """
        Open a new transaction block. Transaction blocks can be nested (BEGIN can
        be issued inside of an existing block) but you should get non‐nested 
        transaction working first before starting on nested. A GET within a 
        transaction returns the latest value by any command. Any data command that 
        is run outside of a transaction block should commit immediately. 
        """
        self.log.append("BEGIN")
        self.transaction_cnt += 1

    def rollback(self):
        """
        Undo all of the commands issued in the most recent transaction block, 
        and close the block. Print nothing if successful, 
        or print NO TRANSACTION if no transaction is in progress. 
        """
        if self.transaction_cnt == 0:
            return "NO TRANSACTION"

        cur = self.log.pop()
        while cur != "BEGIN":
            name, old, new = cur
            self.dirty[name] = old
            cur = self.log.pop()

        self.transaction_cnt -= 1

    def commit(self):
        """
        Close all open transaction blocks, permanently applying the changes made 
        in them. Print nothing if successful, or print NO TRANSACTION if no 
        transaction is in progress. 
        """
        if self.transaction_cnt == 0:
            return "NO TRANSACTION"

        for name in self.dirty:
            value = self.dirty[name]
            if value == None:
                del self.disk[name]
            else:
                self.disk[name] = value

        self.transaction_cnt = 0

    def end(self):
        """
        Exit the program. Your program will always receive this as its 
        last command.
        """
        pass

