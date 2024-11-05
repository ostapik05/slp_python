import json
import unittest
from shared.classes.DictJsonDataAccess import DictJsonDataAccess


class TestDictJsonDataAccess(unittest.TestCase):
    def setUp(self):
        # Setting up a json file with initial data for testing
        self.file_path = "assets/test_file.json"
        with open(self.file_path, 'w') as f:
            json.dump({'key1': 'value1', 'key2': 'value2'}, f)
        self.data_access = DictJsonDataAccess(path=self.file_path, is_caching=False)

    def tearDown(self):
        # Removing the file after tests
        import os
        os.remove(self.file_path)

    def test_getitem(self):
        self.assertEqual(self.data_access['key1'], 'value1')

    def test_setitem(self):
        self.data_access['test_key'] = 'value'
        self.assertEqual(self.data_access['test_key'], 'value')

    def test_delitem(self):
        del self.data_access['key1']
        self.assertNotIn('key1', self.data_access)

    def test_len(self):
        self.assertEqual(len(self.data_access), 2)

    def test_iter(self):
        keys = []
        for key in self.data_access:
            keys.append(key)
        self.assertCountEqual(keys, ['key1', 'key2'])

    def test_contains(self):
        self.assertIn('key1', self.data_access)

    def test_keys(self):
        self.assertCountEqual(self.data_access.keys(), ['key1', 'key2'])

    def test_values(self):
        self.assertCountEqual(self.data_access.values(), ['value1', 'value2'])

    def test_clear(self):
        self.data_access.clear()
        self.assertEqual(len(self.data_access), 0)

    def test_update(self):
        self.data_access.update({'key3': 'value3'})
        self.assertIn('key3', self.data_access)

    def test_get(self):
        self.assertEqual(self.data_access.get('key1'), 'value1')

    def test_set(self):
        self.data_access.set('test_key', 'value')
        self.assertEqual(self.data_access['test_key'], 'value')

    def test_insert(self):
        self.data_access.insert('test_key', 'value')
        self.assertEqual(self.data_access['test_key'], 'value')

    def test_different_types(self):
        test_cases = {
            'int_key': 123,
            'float_key': 123.456,
            'bool_key': True,
            'list_key': [1, 2, 3],
            'dict_key': {'nested_key': 'nested_value'}
        }
        for key, value in test_cases.items():
            self.data_access[key] = value
            self.assertEqual(self.data_access[key], value)


if __name__ == '__main__':
    unittest.main()
