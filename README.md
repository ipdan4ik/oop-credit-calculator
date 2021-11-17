# oop-credit-calculator
## Описание
Проект кредитного калькулятора, в котором реализованы расчёты месячной выплаты, объёма процентов и общей суммы выплаты. Реализована обработка введённых пользователем данных (при вводе некорректных данных выдаётся ошибка с пояснением)

## Для запуска необходимо
 - Python 3.9 и выше

## Инструкция по установке и запуску
1. Клонируйте репозиторий  
 `git clone https://github.com/ipdan4ik/oop-credit-calculator.git`

2. (Опционально) Проверьте работоспособность программы  
 `python test.py`

3. Запустите файл `calculator.py`  
`python calculator.py`

## Инструкция по использованию
1. Для использования данного программного модуля в своих программах, поместите файл `calculator.py` в папку с вашим проектом.

2. Импортируйте необходимые классы и функции  
```python
from calculator import Credit, process_user_data
```

3. Создайте объект класса Credit с помощью функции `process_user_data`  
```python
USER_DATA = ('amount: 200000\n'
            'interest: 12%\n'
            'downpayment: 0\n'
            'term: 24\n')

credit = process_user_data(USER_DATA)
```

4. Для получения нужных расчётов вызовите соответствующие функции класса Credit  
```python
# Месячная выплата по кредиту
month_payment = credit.get_month_payment()

# Общий объём начисленных процентов
percent_value = credit.get_total_percents()

# Общая сумма выплаты
total_payment = credit.get_total_value()
```