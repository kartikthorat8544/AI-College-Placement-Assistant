import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "chatbot.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def save_message(role, content):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (role, content)
        VALUES (?, ?)
        """,
        (role, content)
    )

    connection.commit()
    connection.close()


def get_messages():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        ORDER BY id ASC
        """
    )

    rows = cursor.fetchall()
    connection.close()

    messages = []

    for row in rows:
        messages.append(
            {
                "role": row[0],
                "content": row[1]
            }
        )

    return messages


def clear_messages():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM messages")

    connection.commit()
    connection.close()