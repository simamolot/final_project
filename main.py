from read import Title, Actor, Category, Year, Description
from write import Counter


def color_text(text):
    return f'\033[95m{text}\033[0m'


def format_result(result):
    title, description, year, category, first_name, last_name = result
    print(f"Название: {color_text(title)}\n"
          f"Описание: {color_text(description)}\n"
          f"Год: {color_text(year)}\n"
          f"Категория: {color_text(category)}\n"
          f"Актер: {color_text(first_name)} {color_text(last_name)}\n")


def main():
    search_classes = {
        'title': Title,
        'actor': Actor,
        'category': Category,
        'year': Year,
        'description': Description
    }

    while True:
        print("\nДоступные поля для поиска: Актёр, Категория, Год, Описание, Название, Top (выводит топ запросы от пользователя)")
        field = input("Введите одно из полей: ").strip().lower()

        if field in search_classes:
            value = input(f"Введите значение для {field}: ").strip().lower()
            search_instance = search_classes[field](value)
            results = search_instance.execute_search()
        elif field == "top":
            counter = Counter('')
            results = counter.top_result()
            for query, count in results:
                print(f"Запрос: {color_text(query)}, Количество: {count}")
            counter.close()
            continue
        elif field == "exit":
            print("Выход из программы.")
            break
        else:
            print("Неизвестное поле. Попробуйте снова.")
            continue

        if results:
            for result in results:
                format_result(result)

            counter = Counter(value)
            counter.insert_or_update()
            counter.close()
        else:
            print(color_text("По вашему запросу ничего не найдено."))


if __name__ == "__main__":
    main()
