# db_init.py
import sqlite3

# создаём (или открываем) базу movies.db
connection = sqlite3.connect("movies.db")
cursor = connection.cursor()

# таблица фильмов
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)
""")

# таблица пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# таблица оценок (рейтинг фильмов пользователями)
cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    rating INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
)
""")

# добавляем тестовые фильмы
cursor.executemany("INSERT INTO movies (title) VALUES (?)", [
    ("Movie 1",), ("Movie 2",), ("Movie 3",), ("Movie 4",), ("Movie 5",)
])

# добавляем пользователей
cursor.executemany("INSERT INTO users (name) VALUES (?)", [
    ("Alice",), ("Bob",), ("Charlie",)
])

# добавляем рейтинги
cursor.executemany("INSERT INTO ratings (user_id, movie_id, rating) VALUES (?, ?, ?)", [
    (1, 1, 5), (1, 2, 4), (1, 3, 3),
    (2, 2, 5), (2, 3, 4),
    (3, 4, 5), (3, 5, 4),
])

connection.commit()
connection.close()

print("✅ База создана: movies.db")
