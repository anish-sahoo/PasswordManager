import sqlite3
import customtkinter as ctk

global connection, cursor

# main gui, where user will be able to add and view passwords

def show(username, password):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    q1 = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords';")
    items = q1.fetchall()
    print(items)
    print('in show')
    if len(items) > 0:
        fields = getResults(username, password)
        createGUI(fields)
    else:
        cursor.execute("CREATE TABLE IF NOT EXISTS passwords(user, username, password)")
        connection.commit()
        connection.close()


def getResults(uname, pwd):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    print('reached results')
    q2 = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords'")
    result = q2.fetchall()
    connection.commit()
    return result

def createGUI(fields):
    root = ctk.CTk()
    root.title('Password Manager')
    root.geometry('700x500')

    root.mainloop()
