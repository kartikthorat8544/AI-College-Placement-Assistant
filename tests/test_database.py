from database import database as database_service


def use_temporary_database(monkeypatch, tmp_path):
    temporary_database = tmp_path / "test_chatbot.db"

    monkeypatch.setattr(
        database_service,
        "DATABASE_PATH",
        temporary_database
    )

    return temporary_database


def test_initialize_database_creates_file(
    monkeypatch,
    tmp_path
):
    temporary_database = use_temporary_database(
        monkeypatch,
        tmp_path
    )

    database_service.initialize_database()

    assert temporary_database.exists()


def test_save_and_get_message(
    monkeypatch,
    tmp_path
):
    use_temporary_database(monkeypatch, tmp_path)
    database_service.initialize_database()

    database_service.save_message(
        "user",
        "Hello chatbot"
    )

    messages = database_service.get_messages()

    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello chatbot"


def test_messages_remain_in_correct_order(
    monkeypatch,
    tmp_path
):
    use_temporary_database(monkeypatch, tmp_path)
    database_service.initialize_database()

    database_service.save_message(
        "user",
        "What is Python?"
    )

    database_service.save_message(
        "assistant",
        "Python is a programming language."
    )

    messages = database_service.get_messages()

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_clear_messages(
    monkeypatch,
    tmp_path
):
    use_temporary_database(monkeypatch, tmp_path)
    database_service.initialize_database()

    database_service.save_message(
        "user",
        "Delete this test message"
    )

    database_service.clear_messages()

    messages = database_service.get_messages()

    assert messages == []