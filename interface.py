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
        createGUI(username, fields)
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



class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = ctk.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = ctk.CTkButton(self, text="Copy", width=80, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return

def createGUI(uname, fields):
    root = ctk.CTk()
    root.title('Password Manager')
    root.geometry('700x500')
    root.grid_columnconfigure((0), weight=5, pad=5)
    root.grid_rowconfigure((1,2), weight=1, pad=20)
    root.grid_rowconfigure((0), weight=0, pad=20)

    usernameLabel = ctk.CTkLabel(root, text=f'Username-{uname}', font=ctk.CTkFont('monospace',size=25))
    usernameLabel.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

    scrollframe = ScrollableLabelButtonFrame(master=root, width=300, command=copyBtn, corner_radius=0)
    scrollframe.grid(row=1, column=0, padx=10, sticky='ew', columnspan=2)

    for i in range(25):
        scrollframe.add_item(f"item{i}")

    root.mainloop()

def copyBtn(item):
    print('coped')
