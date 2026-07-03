import re
from decimal import Decimal
from typing import Callable


def parse_number(text: str):
    try:
        return Decimal(text.strip())
    except Exception:
        return None


def generator_numbers(text: str):
    matched = re.findall(r" (?:(?:\d+\.\d+)|(?:\d+)) ", text)
    numbers = map(parse_number, matched)
    for number in filter(None, numbers):
        yield number


def sum_profit(text: str, generator: Callable):
    return sum(number for number in generator(text))


if __name__ == "__main__":
    text = "11 Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів.  22"
    print(sum_profit(text, generator_numbers))
