"""Модуль кредитного калькулятора."""
from dataclasses import dataclass
import sys
from typing import ClassVar
from loguru import logger
import Levenshtein

INPUT_FIELDS = {'amount', 'interest', 'downpayment', 'term'}
FIELD_MISSING_ERROR = 'Не введены следующие данные: {difference}'
INCORRECT_VALUE_ERROR = 'Некорректные данные для поля {field}'

TYPO_FRACTION = 0.25

SCRIPT_PATH = sys.path[0]
logger.add(sink=SCRIPT_PATH + '\\calculator.log',
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            encoding="utf8")
logger.info('Модуль calculator запущен.')

@dataclass
class Credit:
    """Основной класс обработки кредита."""
    YY_TO_MM: ClassVar[int] = 1/12
    PERCENT_TO_FRAC: ClassVar[int] = 1/100

    amount: float
    interest: float
    downpayment: float
    term: float

    def __post_init__(self):
        logger.info(f"Объект создан: {self.__repr__()}")

    def get_month_payment(self) -> float:
        """Возвращает месячную выплату по кредиту."""
        months_interest_frac = self.interest * self.YY_TO_MM * self.PERCENT_TO_FRAC
        return ((self.amount - self.downpayment) * (months_interest_frac +
                (months_interest_frac) /
                (((1 + months_interest_frac) ** self.term) - 1)))

    def get_total_percents(self) -> float:
        """Возвращает общий объём начисленных процентов."""
        return  (self.get_total_value() / self.amount) / self.PERCENT_TO_FRAC - 100

    def get_total_value(self) -> float:
        """Возвращает общую сумму выплаты по кредиту."""
        return self.get_month_payment() * self.term

    def __str__(self) -> str:
        month_payment = self.get_month_payment()
        percent_value = self.get_total_percents()
        total_payment = self.get_total_value()
        return (f'Месячная выплата: {month_payment:.2f}\n'
                f'Общий объём начисленных процентов: {percent_value:.2f}\n'
                f'Общая сумма выплаты: {total_payment:.2f}')

def find_typo(string):
    """Возвращает строку с исправленными опечатками, если их объём не превышает TYPO_FRACTION."""
    for field in INPUT_FIELDS:
        if field == string:
            return field
        if Levenshtein.distance(string, field) <= round(TYPO_FRACTION * len(field), 0):
            logger.info(f'Typo fixed: {string} to {field}')
            return field

def process_user_data(data: str) -> Credit:
    """Возвращает объект Credit, полученный на основе введённых строковых данных."""
    logger.info(f"Обработка введённых данных:\n{data}")
    values = {}
    data = data.replace(' ', '').lower()
    try:
        for line in data.splitlines():
            key_value_pair = line.split(':')
            if len(key_value_pair) != 2:
                continue
            field, amount = key_value_pair
            field = find_typo(field)
            if field:
                values[field] = float(amount.replace('%', ''))
    except ValueError as val_error:
        error_message = INCORRECT_VALUE_ERROR.format(field=field)
        logger.error(error_message)
        raise ValueError(error_message) from val_error

    if set(values.keys()) != INPUT_FIELDS:
        difference = ', '.join(INPUT_FIELDS - set(values.keys()))
        error_message = FIELD_MISSING_ERROR.format(difference=difference)
        logger.error(error_message)
        raise KeyError(error_message)

    return Credit(**values)


if __name__ == '__main__':
    USER_DATA = ('amont: 200000\n'
                'interest: 12%\n'
                'downpayment: 0\n'
                'term: 24\n')

    credit = process_user_data(USER_DATA)
    print(credit)
