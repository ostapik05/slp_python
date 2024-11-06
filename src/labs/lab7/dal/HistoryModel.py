from shared.classes.DictJsonDataAccess import DictJsonDataAccess

class HistoryModel:
    def __init__(self, path, results_to_save = 5):
        self.__history = DictJsonDataAccess(path)
        self.results_to_save = results_to_save
        if not self.__history.validate(is_can_be_empty=True):
            raise KeyError("History file doesn't exist")

    def get_history(self):
        return self.__history.get('history')

    def add(self, query, regex, regex_field, fields, results):
        event = {
            "query": query,
            "regex": regex,
            "regex_field": regex_field,
            "fields": fields,
            "results": results
        }
        history = self.__history.get('history')
        history = history[1:self.results_to_save-1]
        history.append(event)
        self.__history.set('history', history)

    def clear_history(self):
        self.__history.set('history', [])
