from collections import OrderedDict

class OrderedSet:
    def __init__(self):
        self._data = OrderedDict()

    def add(self, item):
        if item not in self._data:
            self._data[item] = None

    def discard(self, item):
        if item in self._data:
            del self._data[item]

    def remove(self, item):
        if item in self._data:
            del self._data[item]
        else:
            raise KeyError(f"Item {item} not found in OrderedSet")

    def __contains__(self, item):
        return item in self._data

    def __repr__(self):
        return f"{', '.join(self._data.keys())}"

    def __iter__(self):
        return iter(self._data.keys())