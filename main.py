"""Модуль кредитного калькулятора."""
from dataclasses import dataclass
from typing import ClassVar

INPUT_FIELDS = {'amount', 'interest', 'downpayment', 'term'}
FIELD_MISSING_ERROR = 'Не введены следующие данные: {difference}'
INCORRECT_VALUE_ERROR = 'Некорректные данные для поля {field}'

@dataclass
class Credit:
    """Основной класс обработки кредита."""
    YY_TO_MM: ClassVar[int] = 1/12
    PERCENT_TO_FRAC: ClassVar[int] = 1/100

    amount: float
    interest: float
    downpayment: float
    term: float

    def get_month_payment(self):
        """Возвращает месячную выплату по кредиту."""
        months_interest_frac = self.interest * self.YY_TO_MM * self.PERCENT_TO_FRAC
        return ((self.amount - self.downpayment) * (months_interest_frac +
                (months_interest_frac) /
                (((1 + months_interest_frac) ** self.term) - 1)))

    def get_total_percents(self):
        """Возвращает общий объём начисленных процентов."""
        return  (self.get_total_value() / self.amount) / self.PERCENT_TO_FRAC

    def get_total_value(self):
        """Возвращает общую сумму выплаты по кредиту."""
        return self.get_month_payment() * self.term

    def __repr__(self) -> str:
        month_payment = self.get_month_payment()
        percent_value = self.get_total_percents()
        total_payment = self.get_total_value()
        return (f'Месячная выплата: {month_payment}\nОбщий объём процентов: '
            f'{percent_value}\nОбщая сумма выплаты: {total_payment}')


def process_user_data(data: str) -> Credit:
    """Возвращает объект Credit, полученный на основе введённых строковых данных."""
    values = {}
    try:
        for line in data.splitlines():
            key_value_pair = line.split(': ')
            if len(key_value_pair) != 2:
                continue
            field, amount = key_value_pair
            if field in INPUT_FIELDS:
                values[field] = float(amount.replace('%', ''))
    except ValueError as val_error:
        raise ValueError(INCORRECT_VALUE_ERROR.format(field=field)) from val_error

    if set(values.keys()) != INPUT_FIELDS:
        difference = ', '.join(INPUT_FIELDS - set(values.keys()))
        raise KeyError(FIELD_MISSING_ERROR.format(difference=difference))
    return Credit(**values)


if __name__ == '__main__':
    USER_DATA = ('amount: 200000\n'
                'interest: 12%\n'
                'downpayment: 0\n'
                'term: 24\n')

    credit = process_user_data(USER_DATA)

    print(credit)
