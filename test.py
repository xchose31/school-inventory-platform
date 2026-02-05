import pandas as pd
import random
import json
from app import db, app
from app.models import Equipment


def extract_random_rows(file_path, n=200):
    # Загружаем Excel-файл в DataFrame
    df = pd.read_excel(file_path)

    # Убедимся, что в файле достаточно строк
    if len(df) < n:
        raise ValueError(f"Файл содержит меньше {n} строк. Всего строк: {len(df)}")

    # Выбираем случайные индексы без повторений
    random_indices = random.sample(range(len(df)), n)

    # Получаем выбранные строки
    selected_rows = df.iloc[random_indices]

    # Преобразуем в список списков
    result = selected_rows.values.tolist()

    return result


# Пример использования:
file_path = 'Свод СВТ .xlsx'
random_rows = extract_random_rows(file_path, n=300)
with app.app_context():
    for elem in random_rows:
        if elem[0] == 'г Москва, ул Молостовых, д 10А':
            eq = Equipment(
                name=elem[2],
                territory='Альфа',
                office=elem[1],
                categories=json.dumps(
                    {"type": random.choice(["Учебное", "Техническое"]), "subject": random.choice([
                        "Физика",
                        "Информатика",
                        "Математика",
                        "Химия",
                        "Биология",
                        "География",
                        "История",
                        "Литература",
                        "Русский язык",
                        "Английский язык",
                        "Немецкий язык",
                        "Французский язык",
                        "Обществознание",
                        "Экономика",
                        "Право",
                        "Астрономия",
                        "Технология",
                        "ОБЖ",
                        "Физкультура",
                        "Музыка",
                        "ИЗО",
                        "Черчение",
                        "Экология",
                        "Психология",
                        "Алгебра",
                        "Геометрия",
                        "Астрономия"])}, ensure_ascii=False),
                photo_path=random.choice(["b2982b4981ec445c823946c5c7b32a62.jpeg", "342b8a9ca3c74c3586d9863952f67b68.jpeg", "56e6053adacf441ab198bc6e0b462d0a.jpeg"])
            )
            db.session.add(eq)
            db.session.commit()

