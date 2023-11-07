import sys
from typing import TextIO

Reservation = tuple[int, int, int]
Problem = tuple[int, list[Reservation]]
Forecast = list[int]


def read_data(f: TextIO) -> Problem:
    num_rooms = int(f.readline().strip())
    reservations = []
    for line in f:
        day, rooms, duration = map(int, line.strip().split())
        reservations.append((day, rooms, duration))
    return (num_rooms, reservations)


def process(problem: Problem) -> Forecast:
    num_rooms, reservations = problem

    def generate_forecast(reservations):
        if not reservations:
            return []

        mid = len(reservations) // 2
        left = generate_forecast(reservations[:mid])
        right = generate_forecast(reservations[mid:])

        forecast = [reservations[mid][0], reservations[mid][1]]
        i, j = 0, 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                forecast.extend([left[i] + reservations[mid][0], left[i + 1]])
                i += 2
            else:
                forecast.extend([right[j] + reservations[mid][0], right[j + 1]])
                j += 2

        forecast.extend(left[i:] + right[j:])
        return forecast

    reservations.sort(key=lambda x: x[0])
    forecast = generate_forecast(reservations)
    forecast.append(forecast[-1] + reservations[-1][2])

    return forecast


def show_results(forecast: Forecast) -> None:
    print(" ".join(map(str, forecast)))


if __name__ == "__main__":
    problem = read_data(sys.stdin)
    forecast = process(problem)
    show_results(forecast)
