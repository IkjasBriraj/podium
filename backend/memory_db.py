"""
In-memory storage for when MongoDB is not available.
This provides the same interface as MongoDB collections.
"""

class InMemoryCollection:
    def __init__(self):
        self.data = []
    
    async def find(self, filter_dict=None):
        return InMemoryCursor([
            item for item in self.data
            if not filter_dict or all(item.get(k) == v for k, v in filter_dict.items())
        ])
    
    async def find_one(self, filter_dict):
        for item in self.data:
            if all(item.get(k) == v for k, v in filter_dict.items()):
                return item
        return None
    
    async def insert_one(self, document):
        self.data.insert(0, document)
        return type('Result', (), {'inserted_id': document.get('_id')})()
    
    async def update_one(self, filter_dict, update_dict):
        for item in self.data:
            if all(item.get(k) == v for k, v in filter_dict.items()):
                if '$set' in update_dict:
                    item.update(update_dict['$set'])
                return type('Result', (), {'matched_count': 1})()
        return type('Result', (), {'matched_count': 0})()
    
    async def delete_one(self, filter_dict):
        for i, item in enumerate(self.data):
            if all(item.get(k) == v for k, v in filter_dict.items()):
                self.data.pop(i)
                return type('Result', (), {'deleted_count': 1})()
        return type('Result', (), {'deleted_count': 0})()
    
    def sort(self, field, direction):
        # Sort in place and return self for chaining
        reverse = direction == -1
        self.data.sort(key=lambda x: x.get(field, ''), reverse=reverse)
        return self


class InMemoryCursor:
    def __init__(self, data):
        self.data = data
    
    async def to_list(self, length):
        return self.data[:length]
    
    def sort(self, field, direction):
        reverse = direction == -1
        self.data.sort(key=lambda x: x.get(field, ''), reverse=reverse)
        return self


class InMemoryDatabase:
    def __init__(self):
        self.collections = {}
    
    def __getitem__(self, name):
        if name not in self.collections:
            self.collections[name] = InMemoryCollection()
        return self.collections[name]
