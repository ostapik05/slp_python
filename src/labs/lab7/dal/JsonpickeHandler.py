from shared.classes.OrderedSet import OrderedSet
from jsonpickle.handlers import BaseHandler, register

class OrderedSetHandler(BaseHandler):
    def flatten(self, obj, data):
        return list(obj._data.keys())

    def restore(self, data):
        return OrderedSet(data)

def handle():
    register(OrderedSet, OrderedSetHandler)