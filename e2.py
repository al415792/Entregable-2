import sys
from typing import TextIO

Reservation = tuple[int, int, int]
Problem = tuple[int, list[Reservation]]
Forecast = list[int]


def read_data(f: TextIO) -> Problem:
    pass


def process(problem: Problem) -> Forecast:
    pass


def show_results(forecast: Forecast) -> None:
    print(" ".join(map(str, forecast)))


if __name__ == "__main__":
    problem = read_data(sys.stdin)
    forecast = process(problem)
    show_results(forecast)
