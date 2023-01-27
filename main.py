import os
from os import getlogin
from sys import platform

from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

from contact_classes.contact_work import WorkContact
from note_classes.note_work import WorkNote

from book_interface import BookInterface
from file_sorter import sort_targets
from instructions import show_instructions
from bug_catcher import erorr_catcher


def main():
    """Основна функція. Приймаємо текст, парсимо його, передаємо в хендлер. Виводимо результат."""
    while True:
        print("\nCommand 'help' will help you.")
        data = input_user_text()
        try:
            command, name, data = parse_user_text(data)
        except ValueError:
            print("Enter some information please")
            continue
        result = handler(command, name, data)
        show_results(result)


@erorr_catcher
def input_user_text() -> str:
    """Просто зчитує текст."""
    commands_completer = commands
    users = {k: None for k in book.contacts_book}
    input_completer = NestedCompleter.from_nested_dict(
        {k: users for k in commands_completer}
    )
    data = prompt('"Please enter what do you want to do: ', completer=input_completer)
    # data = input("Enter: ")
    return data


@erorr_catcher
def parse_user_text(text: str) -> list:
    """Обробка тексту. Поділяє текст на три частини, у разі виклику юзером команди яка не потребує аргументів - повертає все одно список
    з трьох елементів, щоб виклик всіх команд був однаковий."""

    data = text.split()
    if len(data) == 1:
        return [data[0], "", ""]
    else:
        return [data[0], data[1], data[2:]]


@erorr_catcher
def handler(command: str, name: str, data) -> str | list:
    """Перевірка команди на наявність в нашому словнику і відповідно виклик функції, якщо команда існує, або рейз помилки. Ця помилка обрана,
    щоб відокремитися від KeyError. Коли декоратор ловить цей Warning - він має запускати процес аналізу і підказки команд."""

    if command in commands:
        return commands[command](name, data)
    else:
        raise Warning(command, commands.keys())


def help_me(*_) -> str:
    return (
        "If you want to know how to use this script - use command 'instruction' with:\n"
        "'contacts' - to read about ContactBook commands.\n"
        "'notes' - to read about NoteBook.\n"
        "'file' - to read about FileSorter.\n"
        "Or use 'exit' if you want to leave."
    )


@erorr_catcher
def instructions(category: str, *_) -> str:
    """Обирає який файл інструкцій відкрити відповідно до команди користувача."""

    result = show_instructions(category)
    return result


@erorr_catcher
def show_results(result: str | list):
    """Виводить результат запросу користувача. Вдалий чи не вдалий - все одно виводить. Навіть декоратор якщо ловить помилку - він не принтує
    рядок, а ретюрнить його сюди. Всі принти мають виконуватися саме тут. І ніде більше в програмі. Окрім FileSorter"""

    if isinstance(result, list):
        for page in result:
            print(page)
    else:
        print(result)


@erorr_catcher
def good_bye(*_):
    print(book.save_to_file())
    print(notes.save_to_file())
    exit("Bye")


@erorr_catcher
def file_sorter(path_for_sorting: str, path_for_sorting_2: list):
    if path_for_sorting_2:
        sort_targets([path_for_sorting, *path_for_sorting_2])
        return f"Folders {path_for_sorting} and {','.join(path_for_sorting_2)} successfully sorted."
    else:
        sort_targets(path_for_sorting)
        return f"Folder {path_for_sorting} successfully sorted."


@erorr_catcher
def create_path_for_saves():
    match platform:
        case "linux":
            abs_path = f"/home/{getlogin()}/Documents/my_helper"
        case "win32":
            abs_path = f"C:/Users/{getlogin()}/AppData/Local/my_helper"
        case "darwin":
            pass
        case _:
            raise OSError("I can't work with this OS. Sorry.")
    try:
        os.mkdir(abs_path)
        return abs_path
    except FileExistsError:
        return abs_path


class ContactInterface(BookInterface):
    def show_all(self, *_) -> list:
        """Створює рядок з інформацією про кожен контакт"""
        print("______")
        rec_info = []
        for record in book.contacts_book.values():
            rec_info.append(str(record))
        return rec_info

    def show_one(self, *args) -> str:
        """Виводить інформацію про один конкретний контакт"""
        if not self:
            raise ValueError("You can't search empty contact-name.")
        return f"{str(book.contacts_book[self]) if self in book.contacts_book else f'Contact {self} is not found.'}"

    def show_page(self, number_of_contacts: str, *_) -> list:
        """Ітеруємось по записам і формуєм сторінку з контактами по number_of_contacts штук на сторінку"""
        if self:
            n = int(self)
        else:
            n = 5
        result = []
        for page in book.contacts_book.iterator(n):
            result_str = []
            for record in page:
                result_str.append(str(book.contacts_book[record]))
            result.extend(["Page Start", *result_str, "Page End"])
        return result


class NoteInterface(BookInterface):
    def show_all(self, *_):
        """Показує всі нотатки"""
        all_notes = []
        for note in notes.note_book.values():
            all_notes.append(str(note))
        return all_notes if all_notes else "Notes is empty"

    def show_one(self, *_):
        """Показує одну конкретну нотатку"""
        return str(notes.note_book[self])

    def show_page(self, *_) -> list:
        """Ітеруємось по записам і формуєм рядок з нотатками по number_of_notes штук на сторінку"""
        if self:
            n = int(self)
        else:
            n = 5
        result = []
        for page in notes.note_book.iterator(int(n)):
            result_str = []
            for record in page:
                result_str.append(str(notes.note_book[record]))
            result.extend(["Page Start", *result_str, "Page End"])
        return result


absolute_path = create_path_for_saves()
book = WorkContact(f"{absolute_path}/contacts.bin")
notes = WorkNote(f"{absolute_path}/notes.bin")


commands = {
    "help": help_me,
    "instruction": instructions,
    "create_contact": book.create,
    "show_contact_book": ContactInterface.show_all,
    "show_contact": ContactInterface.show_one,
    "show_contact_page": ContactInterface.show_page,
    "clear_contact_book": book.delete_all,
    "delete_contact": book.delete_one,
    "add_to_contact": book.add_values,
    "edit_contact": book.edit_information,
    "edit_contact_name": book.edit_name,
    "search_in_contacts": book.search_in,
    "show_nearest_birthdays": book.show_nearest_birthdays,
    "days_to_birthday_for_one": book.days_to_birthday_for_one,
    "days_to_birthday_for_all": book.days_to_birthday_for_all,
    "create_note": notes.create,
    "show_note_book": NoteInterface.show_all,
    "show_note": NoteInterface.show_one,
    "show_note_page": NoteInterface.show_page,
    "clear_note_book": notes.delete_all,
    "delete_note": notes.delete_one,
    "add_to_note": notes.add_values,
    "edit_note": notes.edit_information,
    "edit_note_name": notes.edit_name,
    "search_in_notes": notes.search_in,
    "sorted_notes_by_tags": notes.sorted_by_tags,
    "file_sorter": file_sorter,
    "exit": good_bye,
}

if __name__ == "__main__":
    main()
