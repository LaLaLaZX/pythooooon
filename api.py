from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def connect_to_database():
    return sqlite3.connect("shop.db")


def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
    id INTEGER PRIMARY KEY,
    Surname TEXT NOT NULL,
    email TEXT NULL,
    telephone TEXT NULL
    )
    ''')
    connection.commit()
    connection.close()


def insert_client(surname, email, telephone):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Clients (Surname, email, telephone) VALUES (?, ?, ?)',(surname, email, telephone))
    connection.commit()
    connection.close()


def select_all_clients():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Clients')
    students = cursor.fetchall()

    connection.close()
    return students


def select_client_by_surname(surname):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT Surname, email, telephone FROM Clients WHERE Surname = ?', (surname,))
    results = cursor.fetchall()

    connection.close()
    return results


def update_email_by_surname(surname, new_email):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('UPDATE Clients SET email = ? WHERE Surname = ?', (new_email, surname))
    connection.commit()
    connection.close()


def delete_client_by_surname(surname):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Clients WHERE Surname = ?", (surname,))
    connection.commit()
    connection.close()


def main():
    create_table()

    while True:
        print('Выберите действие')
        print('1 - Добавить данные в бд')
        print('2 - Просмотреть всю таблицу')
        print('3 - Найти клиента по фамилии')
        print('4 - Изменить почту по фамилии')
        print('5 - Удалить данные из бд')
        print('0 - Выйти')

        choise = int(input('Введите номер действия: '))

        match choise:
            case 1:
                surname = input('Укажите фамилию клиента: ')
                email = input('Укажите почту клиента: ')
                telephone = input('Укажите телефон клиента: ')
                insert_client(surname, email, telephone)
                print('Данные успешно добавлены в бд')
            case 2:
                print('Таблица клиенты: ')
                clients = select_all_clients()
                for client in clients:
                    print(client)
            case 3:
                surname = input('Укажите данные для поиска: ')
                results = select_client_by_surname(surname)
                for row in results:
                    print(row)
            case 4:
                surname = input('Введите фамилию для изменения почты: ')
                new_email = input('Укажите новый почтовый адрес')
                update_email_by_surname(surname, new_email)
                print('Почта обновлена')
            case 5:
                surname = input('Укажите фамилию для удаления: ')
                delete_client_by_surname(surname)
                print('Данные удалены')
            case 0:
                print('Выход...')
                break



class ClientCreate(BaseModel):
    Surname: str
    email: str = None
    telephone: str = None


@app.post("/clients/", response_model=ClientCreate)
async def create_client(client: ClientCreate):
    insert_client(client.Surname, client.email, client.telephone)
    return client


@app.get("/clients/")
async def read_clients():
    clients = select_all_clients()
    return {"Клиенты": clients}


@app.get("/clients/{surname}")
async def read_client_by_surname(surname: str):
    results = select_client_by_surname(surname)
    return {"Клиенты": results}


@app.put("/clients/{surname}")
async def update_client_email(surname: str, new_email: str):
    update_email_by_surname(surname, new_email)
    return {"message": "Почта обновлена"}


@app.delete("/clients/{surname}")
async def delete_client(surname: str):
    delete_client_by_surname(surname)


if __name__ == '__main__':
    main()
