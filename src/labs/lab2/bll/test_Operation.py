import sys
import unittest
from Operation import Operation


class TestOperation(unittest.TestCase):

    def setUp(self):
        # Set up Operation instances for testing
        self.operation_add = Operation("+", 5, 3, 8)
        self.operation_add_2 = Operation("+", 10, 15, 25)
        self.operation_subtract = Operation("-", 7, 2, 5)
        self.operation_subtract_2 = Operation("-", 20, 5, 15)
        self.operation_multiply = Operation("*", 4, 3, 12)
        self.operation_multiply_2 = Operation("*", 6, 7, 42)
        self.operation_divide = Operation("/", 10, 2, 5)
        self.operation_divide_2 = Operation("/", 20, 4, 5)
        self.operation_divide_by_zero = Operation("/", 10, 0, None)

    def test_operation_add(self):
        self.assertEqual(self.operation_add.get_first_number() + self.operation_add.get_second_number(),
                         self.operation_add.get_result())
        self.assertEqual(self.operation_add_2.get_first_number() + self.operation_add_2.get_second_number(),
                         self.operation_add_2.get_result())

    def test_operation_subtraction(self):
        self.assertEqual(self.operation_subtract.get_first_number() - self.operation_subtract.get_second_number(),
                         self.operation_subtract.get_result())
        self.assertEqual(self.operation_subtract_2.get_first_number() - self.operation_subtract_2.get_second_number(),
                         self.operation_subtract_2.get_result())

    def test_operation_multiply(self):
        self.assertEqual(self.operation_multiply.get_first_number() * self.operation_multiply.get_second_number(),
                         self.operation_multiply.get_result())
        self.assertEqual(self.operation_multiply_2.get_first_number() * self.operation_multiply_2.get_second_number(),
                         self.operation_multiply_2.get_result())

    def test_operation_divide(self):
        self.assertEqual(self.operation_divide.get_first_number() / self.operation_divide.get_second_number(),
                         self.operation_divide.get_result())
        self.assertEqual(self.operation_divide_2.get_first_number() / self.operation_divide_2.get_second_number(),
                         self.operation_divide_2.get_result())

    def test_operation_divide_by_zero(self):
        self.assertFalse(self.operation_divide_by_zero.is_complete())
        with self.assertRaises(ZeroDivisionError):
            self.operation_divide_by_zero.get_first_number() / self.operation_divide_by_zero.get_second_number()


if __name__ == '__main__':
    unittest.main()
