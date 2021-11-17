import unittest

from main import Credit, process_user_data


class TestCreditClass(unittest.TestCase):

    def test_credit_without_downpayment(self):
        credit = Credit(amount=200000, interest=12, downpayment=0, term=24)
        self.assertEqual(round(credit.get_month_payment(), 4), 9414.6944)
        self.assertEqual(round(credit.get_total_percents(), 4), 112.9763)
        self.assertEqual(round(credit.get_total_value(), 4), 225952.6667)

    def test_credit_with_downpayment(self):
        credit = Credit(amount=100000, interest=5.5, downpayment=20000, term=30)
        self.assertEqual(round(credit.get_month_payment(), 4), 2860.2969)


class TestUserInputProcessing(unittest.TestCase):
    FIELD_MISSING_ERROR = 'Не введены следующие данные: {difference}'
    INCORRECT_VALUE_ERROR = 'Некорректные данные для поля {field}'
    
    def test_right_user_input(self):
        user_data = ('amount: 200000\n'
                    'interest: 12%\n'
                    'downpayment: 0\n'
                    'term: 24\n')
        credit_generated = process_user_data(user_data)
        credit_right = Credit(amount=200000, interest=12, downpayment=0, term=24)
        self.assertEqual(credit_generated.__repr__(), credit_right.__repr__())

    def test_extra_keys(self):
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
        user_data = ('amount: 200000\n'
                    'interest: 12%\n'
                    'term: 24\n')
        error_message = self.FIELD_MISSING_ERROR.format(difference='downpayment')
        with self.assertRaisesRegex(KeyError, error_message):
            process_user_data(user_data)

    def test_incorrect_value(self):
        user_data = ('amount: test\n'
                    'interest: 12%\n'
                    'downpayment: 0\n'
                    'term: 24\n')
        error_message = self.INCORRECT_VALUE_ERROR.format(field='amount')
        with self.assertRaisesRegex(ValueError, error_message):
            process_user_data(user_data)

if __name__ == '__main__':
    unittest.main()
