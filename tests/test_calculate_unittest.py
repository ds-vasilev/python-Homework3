import unittest
from tests.constant_test_cases import PUBLIC_TEST_CASES, SECRET_TEST_CASES
from main import main  # Импорт функции main из домашнего задания
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.join(sys.path[0]))

class MainTestCase(unittest.TestCase):
    """Такие же тестовые случаи, но реализованные через unittest."""

    def setUp(self):
        """Начальные условия для тестов."""
        self.all_test_cases = PUBLIC_TEST_CASES + SECRET_TEST_CASES

    def test_main(self):
        """Тесирование функции разнесения данных из json по таблицам. Удаление созданной БД."""
        for test_case in self.all_test_cases:
            test_inp = test_case.get("test_input")
            expected = test_case.get("expected")
            self.assertEqual(main(test_inp), expected)
        os.remove("C:/GitHub/python-Homework3/tests/TASK.db")
