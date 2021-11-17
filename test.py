"""Модуль юнит-тестов."""
import unittest

import calculator
from calculator import Credit, process_user_data


class TestCreditClass(unittest.TestCase):
    """Проверка класса Credit."""

    def test_credit_without_downpayment(self):
        """Создание кредита без первоначального взноса."""
        credit = Credit(amount=200000, interest=12, downpayment=0, term=24)
        self.assertEqual(round(credit.get_month_payment(), 4), 9414.6944)
        self.assertEqual(round(credit.get_total_percents(), 4), 12.9763)
        self.assertEqual(round(credit.get_total_value(), 4), 225952.6667)

    def test_credit_with_downpayment(self):
        """Создание кредита с первоначальным взносом."""
        credit = Credit(amount=100000, interest=5.5, downpayment=20000, term=30)
        self.assertEqual(round(credit.get_month_payment(), 4), 2860.2969)


class TestUserInputProcessing(unittest.TestCase):
    """Проверка обработки введённых данных."""

    def test_right_user_input(self):
        """Обработка корректно введённых данных."""
        user_data = ('amount: 200000\n'
                    'interest: 12%\n'
                    'downpayment: 0\n'
                    'term: 24\n')
        credit_generated = process_user_data(user_data)
        credit_right = Credit(amount=200000, interest=12, downpayment=0, term=24)
        self.assertEqual(credit_generated.__repr__(), credit_right.__repr__())

    def test_extra_keys(self):
        """Проверка данных с лишними строками (они должны игнорироваться)."""
        user_data = ('first_extra_key: test\n'
                    'amount: 200000\n'
                    'interest: 12%\n'
                    ' \n'
                    'downpayment: 0\n'
                    'term: 24\n')
        credit_generated = process_user_data(user_data)
        credit_right = Credit(amount=200000, interest=12, downpayment=0, term=24)
        self.assertEqual(credit_generated.__repr__(), credit_right.__repr__())

    def test_less_keys(self):
        """Проверка данных с недостающими строками (должно выдавать ошибку)."""
        user_data = ('amount: 200000\n'
                    'interest: 12%\n'
                    'term: 24\n')
        error_message = calculator.FIELD_MISSING_ERROR.format(difference='downpayment')
        with self.assertRaisesRegex(KeyError, error_message):
            process_user_data(user_data)

    def test_incorrect_value(self):
        """Проверка данных с некорректными значениями полей (должно выдавать ошибку)."""
        user_data = ('amount: test\n'
                    'interest: 12%\n'
                    'downpayment: 0\n'
                    'term: 24\n')
        error_message = calculator.INCORRECT_VALUE_ERROR.format(field='amount')
        with self.assertRaisesRegex(ValueError, error_message):
            process_user_data(user_data)

if __name__ == '__main__':
    unittest.main()
