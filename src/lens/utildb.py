def is_record_empty(records):
    if records.peek() is None:
        return True
    return False

# in noe4jdriver api.py is changed
# empty() and __len__ functions is added to StatementResult class
# please check and update api.py
'''
    def __len__(self):
        return len(self._records)

    def empty(self):
        return len(self._records) == 0
'''
