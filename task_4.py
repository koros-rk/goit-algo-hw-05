from collections.abc import Callable
from functools import wraps

from colorama import Fore


def input_error(function: Callable):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ValueError or IndexError or KeyError:
            return "Enter the argument for the command"

    return wrapper


def hello(_):
    return "How can I help you?"


@input_error
def add(args, repository: dict):
    (name, phone) = args
    if name not in repository:
        repository.update({name: phone})
        return f"Person {name} added."
    else:
        return "Person already exists."


@input_error
def change(args, repository: dict):
    name, phone = args
    if name in repository:
        repository.update({name: phone})
        return f"Phone number for {name} changed."
    else:
        return "Person not found."


@input_error
def phone(args, repository: dict):
    (name,) = args
    if name in repository:
        return repository.get(name)
    else:
        return "Person not found."


@input_error
def all(_, repository: dict):
    if not repository:
        return "No persons found."

    lines = []

    for name, phone in repository.items():
        lines.append(f"{name}: {phone}")

    return "\n".join(lines)


def default_handler(command: str):
    return f"Command {Fore.GREEN}{command}{Fore.RESET} not found."


def get_handler(command: str):
    match command.casefold():
        case "hello":
            return hello
        case "add":
            return add
        case "change":
            return change
        case "phone":
            return phone
        case "all":
            return all

    return None


def main():
    persons = {}

    print("Welcome to the assistant bot!")

    while True:
        command, *args = input("Enter a command: ").split()
        command_handler = get_handler(command)

        if command in ["exit", "quit"]:
            print("Goodbye!")
            break

        if command_handler:
            print(command_handler(args, repository=persons))
        else:
            print(default_handler(command))


if __name__ == "__main__":
    main()
