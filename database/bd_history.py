import sqlite3
from sqlite3 import Connection, Cursor

from hotlog import hotels_log


def general_operation() -> tuple[Connection, Cursor]:
    """
    Инициируем соединение с базой данных
    :return: (conn, cursor)
    """
    try:
        # Создаем соединение с нашей базой данных
        conn = sqlite3.connect(r'database/hotel_bot.db')

        # Создаем курсор - это специальный объект который
        # делает запросы и получает их результаты
        cursor = conn.cursor()
        return conn, cursor

    except Exception as e:
        hotels_log.logger.exception(e)


def add_entry(data) -> None:
    """
    Добавления записи
    :param data: данные из запроса пользователя
    :return: (None)
    """
    try:
        conn, cursor = general_operation()

        # Если таблицы не существует, то создаем
        cursor.execute("""CREATE TABLE IF NOT EXISTS src_history(
           user_id TEXT,
        command TEXT,
        city TEXT,
        check_in TEXT,
        check_out TEXT,
        number_hotels TEXT,
        number_photos TEXT,
        id TEXT);
        """)

        check_full_result = check_full(data['user_id'])

        # Проверяем, если в истории этого пользователя больше
        # 10 значений, то удаляем самое старое
        if check_full_result == 'no':
            user_entries_id = 1
        elif check_full_result == 'full':
            overwriting(data['user_id'])
            user_entries_id = 10
        else:
            user_entries_id = check_full_result + 1

        entry = (data['user_id'], data['command'], data['city'], data[
            'check_in'], data['check_out'],
                 data['number_hotels'], data['number_photos'], user_entries_id)

        cursor.execute("INSERT INTO src_history VALUES("
                       "?, ?, ?, ?, ?, ?, ?, ?)", entry)

        conn.commit()
        close_db(cursor, conn)
    except Exception as e:
        hotels_log.logger.exception(e)


def check_full(user_id) -> str | int:
    """
    Проверка переполняемости буфера
    :param user_id: id пользователя
    :return: Или маркер, что буфер переполнен или
    записей от этого пользователя нет
    или последний порядковый номер записи
    """
    try:
        conn, cursor = general_operation()
        cursor.execute("SELECT * FROM src_history WHERE user_id=?", (user_id,))
        one_result = cursor.fetchall()
        close_db(cursor, conn)
        if not one_result:
            return 'no'
        else:
            all_ids = []
            for line in one_result:
                all_ids.append(int(line[-1]))
            all_ids.sort()
            max_id = all_ids[-1]
            if int(max_id) >= 10:
                return 'full'
            else:
                return int(max_id)
    except Exception as e:
        hotels_log.logger.exception(e)


def overwriting(user_id) -> None:
    """
    Перезапись истории
    :param user_id: id пользователя
    :return: (None)
    """
    try:
        conn, cursor = general_operation()

        # Удалить запись с id=10 для указанного user_id
        cursor.execute("DELETE FROM src_history WHERE user_id=? AND id=?", (
            user_id, 1))

        # Изменить id для всех записей с user_id и id > 10
        cursor.execute("UPDATE src_history SET id=id-1 WHERE user_id=?", (
            user_id,))

        conn.commit()
        close_db(cursor, conn)
    except Exception as e:
        hotels_log.logger.exception(e)


def history_output(user_id) -> list:
    """
    Вывод истории
    :param user_id: id пользователя
    :return: (one_result), выводит все записи этого
    пользователя в список списков
    """
    try:
        conn, cursor = general_operation()
        cursor.execute("SELECT * FROM src_history WHERE user_id=?", (user_id,))
        one_result = cursor.fetchall()
        close_db(cursor, conn)
        return one_result
    except Exception as e:
        hotels_log.logger.exception(e)


def get_entry(user_id, entry_id) -> list:
    """
    Вывод определенной записи
    :param user_id: id пользователя
    :param entry_id: порядковый номер записи
    :return: (one_result), выводит определенную запись пользователя
    """
    try:
        conn, cursor = general_operation()
        cursor.execute("SELECT * FROM src_history WHERE user_id=? AND id=?", (
            user_id, entry_id))
        one_result = cursor.fetchall()
        close_db(cursor, conn)
        return one_result
    except Exception as e:
        hotels_log.logger.exception(e)


def close_db(cursor, conn) -> None:
    """
    Не забываем закрыть соединение с базой данных
    :param cursor:
    :param conn:
    :return: (None)
    """
    try:
        cursor.close()
        conn.close()
    except Exception as e:
        hotels_log.logger.exception(e)
