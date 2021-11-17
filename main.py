"""Модуль кредитного калькулятора."""
from dataclasses import dataclass
from typing import ClassVar

INPUT_FIELDS = ['amount', 'interest', 'downpayment', 'term']

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
        return 100 + (self.term * self.interest * self.YY_TO_MM)

    def get_total_value(self):
        """Возвращает общую сумму выплаты по кредиту."""
        return self.amount * self.get_total_percents() * self.PERCENT_TO_FRAC


def process_user_data(data: str) -> Credit:
    """Возвращает объект Credit, полученный на основе введённых строковых данных."""
    values = {}
    for line in data.splitlines()[:-1]:
        field, amount = line.split(': ')
        values[field] = float(amount.replace('%', ''))
    print(values)
    return Credit(**values)


if __name__ == '__main__':
    USER_DATA = ('amount: 200000\n'
                'interest: 12%\n'
                'downpayment: 0\n'
                'term: 24\n'
                ' ')

    credit = process_user_data(USER_DATA)

    month_payment = credit.get_month_payment()
    percent_value = credit.get_total_percents()
    total_payment = credit.get_total_value()
    print(f'Месячная выплата: {month_payment}\nОбщий объём процентов:'
            f'{percent_value}\nОбщая сумма выплаты: {total_payment}')
