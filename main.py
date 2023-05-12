import sqlite3
import time
from login import logIn

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()

q1 = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
items = q1.fetchall()

print("Searching for users")
for i in range(2):
    print('.')
    time.sleep(1)

def createNewUser():
    answer = input("Do you want to create a new user? Y/N: ")
    user_name = "EXIT EXIT"
    password = "EXIT EXIT"

    if answer.lower() == 'y':
        print("Okay, initializing interface")
        for i in range(2):
            print('.')
            time.sleep(1)
        while(True):
            user_name = input("Enter a username (cannot contain spaces) : ")
            password = input("Enter a password (cannot contain spaces) : ")
            user_name = user_name.replace(' ', '')
            password = password.replace(' ', '')

            print("")
            if user_name == '':
                print("Username cannot be empty!")
            elif password== '':
                print("Password cannot be empty!")
            elif ' ' in user_name:
                print("Username cannot contain spaces!")
            elif ' ' in password:
                print("Password cannot contain spaces!")
            else:# user_name != '' and password != '':
                break
    return user_name, password

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