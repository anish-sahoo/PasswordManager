import sqlite3
import time
from new_user import createNewUser
from login import logIn

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()

q1 = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
items = q1.fetchall()

print("Searching for users")
for i in range(2):
    print('.')
    time.sleep(1)

if len(items) == 0:
    print("No users exist.\n")
    username, password = createNewUser()
    print(f"The credentials you selected are {username}, {password}")
    cursor.execute("CREATE TABLE users(username, password)")
    cursor.execute("INSERT INTO users VALUES (?,?)",(username,password))
    connection.commit()
else:
    print('Users found, starting GUI...')
    connection.commit()
    connection.close()
    logIn()
