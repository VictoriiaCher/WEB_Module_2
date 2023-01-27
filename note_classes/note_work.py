from book import Book
from note_classes.note import Note


class WorkNote:
    def __init__(self, path):
        self.note_book = Book(path)
        try:
            print(self.note_book.load_from_file())
        except FileNotFoundError:
            self.note_book.save_to_file()

    def create(self, name: str, info: list) -> str:
        """Створює нову нотатку у книзі, якщо нотатки з таким ім'ям ще не існує"""
        if name in self.note_book:
            return f"Note with name '{name} already exist."
        elif not name or not info:
            raise ValueError("You can't create empty note.")
        else:
            tags = []
            for word in info:
                # Шукаємо теги в тексті
                if word.startswith("#"):
                    tags.append(word)
            text = " ".join(info)
            self.note_book[name] = Note(name, tags, text)
            return f"Note with name {name} successfully created."

    def delete_all(self):
        """Видаляє всі нотатки з книги"""
        answer = input("You about to delete all notes in notebook. You shure? Y/N")
        if answer == "Y":
            self.note_book.data = {}
            return "Note book now clean"
        else:
            return "Not deleted"

    def delete_one(self, name: str, *_):
        """Видаляє одну конкретну нотатку з книги"""
        if name in self.note_book.data:
            del self.note_book.data[name]
            return f"Note {name} is deleted"
        else:
            return f"Note {name} is not in notebook"

    def save_to_file(self):
        return self.note_book.save_to_file()

    def load_from_file(self):
        return self.note_book.load_from_file()

    def edit_information(self, name: str, values: list):
        """Редагує інформацію в нотатку. Через те що немає можливості без графічного інтерфейсу зробити зручне редагування в прямому сенсі -
        просто видаляє всі поля окрім імені і додає нову інфу"""
        if not name or not values:
            raise IndexError("You can't edit note without new information.")
        note: Note = self.note_book.data[name]
        note.clear_text()
        note.clear_tags()
        return note.add_to_note(" ".join(values))

    def edit_name(self, name: str, info: list):
        """Змінює ім'я запису. Змінює як ім'я-ключ нотатки, так і в самій нотатці"""
        try:
            new_name = info[0]
        except IndexError:
            raise IndexError(f"Please enter 'old_name' and 'new_name'")
        record: Note = self.note_book[name]
        record.name = new_name
        self.note_book[new_name] = record
        del self.note_book[name]
        return f"{name}'s name has been changed to {new_name}"

    def search_in(self, search_data: str, *_) -> list:
        """Робить пошук у книзі по одному слову"""
        result = []
        for value in self.note_book.values():
            if search_data in (value.name, *value.tags, *value.text.split()):
                result.append(value)
        return result

    def sorted_by_tags(self, *args) -> list:
        """Робить сортування по тегам. Рахує співпадіння тегів, а потім сортує"""
        tags = [args[0], *args[1]]
        matched_records = []

        for note in self.note_book.data.values():
            matched_tags = 0
            for tag in note.tags:
                if tag in tags:
                    matched_tags += 1
            matched_records.append(f"Matches:{matched_tags}\n" f"{str(note)}")
        return (
            sorted(matched_records, reverse=True)
            if matched_records
            else "Matches not found"
        )

    def add_values(self, name: str, info: list):
        """Додає інформацію в нотатку"""
        note: Note = self.note_book[name]
        note.add_to_note(info)
        return f"Value is added to {name}"
