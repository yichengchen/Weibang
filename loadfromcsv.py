from Application import Weibnag
from Expection import LoginFail
from tools import half_width
import csv
import sqlite3
import json
import random


def init_database():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("""

    CREATE TABLE Account
    (
        name TEXT,
        username TEXT,
        password TEXT,
        young_token TEXT,
        type INTEGER
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()


def check_and_insert_database():
    with open('user.csv', newline='') as csvfile:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in data:
            name = row[1]
            phone = row[2]
            pwd = row[3]
            if not phone.isdigit():
                continue
            try:
                x = Weibnag(half_width(phone), half_width(pwd))
                x.login()
                x.websocket(False)

                x.bind_user_area()

                cursor.execute("INSERT INTO 'Account' VALUES ('{}','{}','{}','{}',0)"
                               .format(name, x.username, x.password, x.young_token))
                conn.commit()

            except LoginFail:
                print(row)
                print('\033[1;31;40mError:', name, phone, pwd)
                print("\033[0m")
        print('All Done')
        conn.commit()
        cursor.close()
        conn.close()


def read_from_sql():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    lists = cursor.execute("SELECT * FROM Account").fetchall()
    print(lists)
    for each in lists:
        x = Weibnag(each[0], each[1], each[2])
        x.bind_user_area()


def rand(data):
    return data[random.randint(0, len(data) - 1)]


def post_question_with_json():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username,password,young_token,name FROM Account ")
    tokens = cursor.fetchall()
    success = 0
    with open('questions.json', encoding='utf-8') as q:
        data = json.load(q)
        for que in data:
            print(que)
            title = que["question"]
            content = que["answer"]

            chosen = rand(tokens)
            print(chosen)
            tmp = Weibnag(chosen[0], chosen[1], chosen[2])
            x = tmp.post_question(title, content)
            if x:
                success += 1
                print(success)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    pass
