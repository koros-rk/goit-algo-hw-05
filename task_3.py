import argparse
import sys
from collections import namedtuple

from rich.console import Console
from rich.table import Table

parser = argparse.ArgumentParser()

parser.add_argument("path")
parser.add_argument("severity_level", nargs="?", default=None)


def parse_log_line(line: str):
    try:
        date, time, severity, *message = line.split(" ")
        return namedtuple("Log", ["date", "time", "severity", "message"])(
            date=date, time=time, severity=severity, message=" ".join(message)
        )
    except ValueError:
        return None


def load_logs(path: str):
    logs = []

    try:
        with open(path) as file:
            for line in file:
                parsed_line = parse_log_line(line.strip())
                logs.append(parsed_line)

        return list(filter(None, logs))
    except FileNotFoundError:
        return logs


def filter_logs_by_level(logs: list, level: str):
    return list(filter(lambda log: log.severity.casefold() == level.casefold(), logs))


def count_logs_by_level(logs: list):
    severity_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
    return {level: len(filter_logs_by_level(logs, level)) for level in severity_levels}


def display_log_counts(logs_count: dict[str, int]):
    console = Console()
    table = Table()

    table.add_column(
        "Рівень логування",
        justify="left",
    )
    table.add_column("Кількість", justify="center")

    for level, count in logs_count.items():
        table.add_row(level, str(count))

    console.print(table)


def display_log_severity(logs: list, severity_level: str):
    print(f"Деталі логів для рівня '{severity_level.upper()}':")
    filtered_logs = filter_logs_by_level(logs, severity_level)

    if len(filtered_logs) == 0:
        print(f"{' ' * 2} NO LOGS FOUND")

    for log in filter_logs_by_level(logs, severity_level):
        print(f"{' ' * 2}[{log.severity}] {log.message}")


def main():
    args = parser.parse_args()

    if not args.path:
        print("No logfile path was provided.")
        return

    logs = load_logs(args.path)
    logs_count = count_logs_by_level(logs)

    display_log_counts(logs_count)

    if args.severity_level:
        display_log_severity(logs, args.severity_level)


if __name__ == "__main__":
    main()
