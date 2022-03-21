import json
import sqlite3
import jsonschema
from typing import Any
from jsonschema import ValidationError


def json_parser(file_name: str) -> Any:
    """Функция получает из json-файла данные и раскидывает их по спискам."""
    with open(file_name, 'r', encoding="utf-8") as file:
        x = json.load(file)
    return x


def json_validation_check(valid: tuple) -> bool:
    """Функция валидирует поступаемую схему со схемой в valid_schema.json."""
    try:
        jsonschema.validate(valid, json_parser("valid_schema.json"))
    except ValidationError:
        return "Данные не прошли валидацию."
    else:
        return True


def unique_check(conn: Any, valid: tuple) -> Any:
    """Функция проверяет уникальность Id товара, подаваемого в json."""
    c = conn.cursor()
    c.execute(
        f"""SELECT CASE WHEN count(*) != 0 THEN 'Товар с таким ID уже есть в базе данных. Отвергнуто.' ELSE 'True' \
        END AS result FROM goods WHERE id = {valid["id"]}""")
    return c.fetchall()[0][0]


def create_table(conn: Any) -> None:
    """Функция создает таблицу соответствующую dbml_goods_.png."""
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS shops (id INTEGER PRIMARY KEY AUTOINCREMENT, address VARCHAR(100));""")
    c.execute("""CREATE TABLE IF NOT EXISTS shops_goods (id INTEGER PRIMARY KEY AUTOINCREMENT, id_good INT, \
        id_shop INT, amount INT, FOREIGN KEY (id_shop) REFERENCES shops (id));""")
    c.execute("""CREATE TABLE IF NOT EXISTS goods (id INTEGER UNIQUE PRIMARY KEY NOT NULL, name VARCHAR(50), \
        package_id INT, FOREIGN KEY (id) REFERENCES shops_goods (id_good));""")
    c.execute("""CREATE TABLE IF NOT EXISTS packages (id INTEGER PRIMARY KEY AUTOINCREMENT, type PACKAGE_TYPE,\
        height FLOAT, width FLOAT, depth FLOAT, FOREIGN KEY (id) REFERENCES goods (package_id));""")


def insert_one(conn: Any, good_info: tuple) -> None:
    """Функция разносит данные по таблицам."""
    c = conn.cursor()
    c.execute(
        f"""INSERT INTO packages (type, height, width, depth) VALUES ('{good_info["package_params"]["type"]}', \
            {good_info["package_params"]["width"]}, {good_info["package_params"]["height"]}, \
            {good_info["package_params"]["depth"]});"""
    )

    c.execute("""SELECT MAX(id) FROM packages""")
    kostil = int((c.fetchall()[0][0]))
    c.execute(
        f"""INSERT INTO goods (id, name, package_id) VALUES ('{good_info["id"]}', '{good_info["name"]}', {kostil});"""
    )

    for i in range(len(good_info["location_and_quantity"])):
        c.execute(f"""INSERT INTO shops (address) VALUES ('{good_info["location_and_quantity"][i]["location"]}');""")
        c.execute("""SELECT MAX(id) FROM goods""")
        kostil = int((c.fetchall()[0][0]))
        c.execute("""SELECT MAX(id) FROM shops""")
        kostil_1 = int((c.fetchall()[0][0]))
        c.execute(
            f"""INSERT INTO shops_goods (id_good, id_shop, amount) VALUES ({kostil}, {kostil_1}, \
                '{good_info["location_and_quantity"][i]["amount"]}');""")
    conn.commit()


def main(file_name: str) -> None:
    """Основная функция, принимает название файла."""
    jvc = json_validation_check(json_parser(file_name))
    if jvc is True:
        with sqlite3.connect('TASK.db') as conn:
            create_table(conn)
            uni = unique_check(conn, json_parser(file_name))
            if uni == 'True':
                insert_one(conn, json_parser(file_name))
                return "Данные внесены."
            else:
                return uni
    else:
        return jvc
