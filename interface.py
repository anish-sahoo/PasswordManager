import sqlite3
import customtkinter as ctk
import pyperclip
import sys

global connection, cursor, scrollframe

#gets passwords from database and starts gui
def show(username, password):
    global connection
    global cursor
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    q1 = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords';")
    items = q1.fetchall()
    #print(items)
    #print('in show')
    if len(items) > 0:
        fields = getResults(username, password)
        createGUI(username, fields)
    else:
        cursor.execute("CREATE TABLE IF NOT EXISTS passwords(user, username, password)")
        connection.commit()
        connection.close()

#get all passwords for a given username
def getResults(uname, pwd):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    #print('reached results')
    #q2 = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords'")
    q2 = cursor.execute("SELECT * FROM passwords WHERE user ='"+uname+"';").fetchall()
    #result = q2.fetchall()
    connection.commit() 
    return q2 #result


# modified the CTkScrollableFrame to my requirements, got base code from Ctk library github-
# https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/scrollable_frame_example.py
class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,3,4), weight=1, pad=1)
        self.grid_columnconfigure((1,2), weight=4, pad=1)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.label2_list = []

        self.true_label1_list = []
        self.true_label2_list = []

        self.button_list = []
        self.button2_list = []
        self.button0_list = []

    def add_item(self, item1, item2, image=None):
        if item1 in self.true_label1_list:
            print('Item already exists')
            return False
        
        true_uname = item1
        if len(item1) > 25:
            true_uname = str(item1[0:25]) + '...'

        true_pwd = item2
        if len(item2) > 28:
            true_pwd = item2[0:26] + '...'


        label = ctk.CTkLabel(self, text=true_uname, image=image, compound="left", padx=5, anchor="w")
        label2 = ctk.CTkLabel(self, text=true_pwd, image=image, compound="left", padx=5, anchor=ctk.E)
        button = ctk.CTkButton(self, text="Copy", width=80, height=24)
        button2 = ctk.CTkButton(self, text="Delete", width=80, height=24)
        button0 = ctk.CTkButton(self, text="Copy", width=80, height=24)
        
        if self.command is not None:
            button.configure(command=lambda: self.command(item2))
            button2.configure(command=lambda:self.remove_item(item=item1, tname=true_uname))
            button0.configure(command=lambda:self.command(item1))
        
        button0.grid(row=len(self.button_list), column=0, pady=(4, 6), padx=2)
        label.grid(row=len(self.label_list), column=1, pady=(4, 6), sticky="w")
        label2.grid(row=len(self.label2_list), column=2, pady=(4, 6), sticky="w")
        button.grid(row=len(self.button_list), column=3, pady=(4, 6), padx=5)
        button2.grid(row=len(self.button_list), column=4, pady=(4, 6), padx=5)
        
        self.label_list.append(label)
        self.label2_list.append(label2)
        self.button_list.append(button)
        self.button2_list.append(button2)
        self.button0_list.append(button0)

        self.true_label1_list.append(item1)
        self.true_label2_list.append(item2)
        return True

    def remove_item(self, item, tname):
        for label, label2, button, button2, button0 in zip(self.label_list, self.label2_list, self.button_list, self.button2_list, self.button0_list):
            if tname == label.cget("text"):
                label.destroy()
                label2.destroy()
                button.destroy()
                button2.destroy()
                button0.destroy()

                self.label_list.remove(label)
                self.label2_list.remove(label2)
                self.button_list.remove(button)
                self.button2_list.remove(button2)
                self.button0_list.remove(button0)
                return
    
    def remove_all(self):
        for label, label2, button, button2, button0 in zip(self.label_list, self.label2_list, self.button_list, self.button2_list, self.button0_list):
            label.destroy()
            label2.destroy()
            button.destroy()
            button2.destroy()
            button0.destroy()

            self.label_list.remove(label)
            self.label2_list.remove(label2)
            self.button_list.remove(button)
            self.button2_list.remove(button2)
            self.button0_list.remove(button0)
            return


#creates main gui
def createGUI(uname, fields):
    root = ctk.CTk()
    root.title('Password Manager')
    root.geometry('800x500')
    root.grid_rowconfigure((1), weight=3, pad=10)
    root.grid_rowconfigure((0,2), weight=1, pad=5)

    usernameLabel = ctk.CTkLabel(root, text=f'Username-{uname}', font=ctk.CTkFont('monospace',size=20), text_color='#999999', anchor=ctk.W)
    usernameLabel.grid(row=0, column=0, padx=10, pady=5, sticky='ew', columnspan=3)

    global scrollframe
    scrollframe = ScrollableLabelButtonFrame(master=root, width=770, command=copyBtn, corner_radius=0)
    scrollframe.grid(row=1, column=0, sticky='nsew', padx=10, columnspan=3)

    addItemButton = ctk.CTkButton(root, text='Add Item', font=ctk.CTkFont('monospace',size=25), command=lambda:add(uname, fields))
    addItemButton.grid(row=2, column=0, padx=20, pady=20, sticky='ewns')

    for i in fields:
        scrollframe.add_item(i[1],i[2])

    def on_close():
        connection.close()
        sys.exit()
        #root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close) #sets the on_closing method to be called when gui is closed
    root.mainloop()

#functionality for the copy buttons
def copyBtn(item):
    print(f'copied {item}')
    pyperclip.copy(item)

#gui and methods for adding new items
def add(username, fields):
    window2 = ctk.CTk()
    window2.geometry('800x250')
    window2.grid_columnconfigure((0),weight=1)
    window2.grid_columnconfigure((1),weight=3)
    window2.grid_rowconfigure((0,1,2),weight=1)
    
    label1 = ctk.CTkLabel(window2, text="Username", height=20, font=ctk.CTkFont('monospace',size=20))
    label1.grid(row=0, column=0, sticky='ewns', pady=10)

    label2 = ctk.CTkLabel(window2, text='Password', height=20, font=ctk.CTkFont('monospace',size=20))
    label2.grid(row=1, column=0, sticky='ewns', pady=10)

    entry1 = ctk.CTkEntry(window2, height=20, font=ctk.CTkFont('monospace',size=20))
    entry1.grid(row=0, column=1, sticky='ewns', pady=10, padx=10)

    entry2 = ctk.CTkEntry(window2, height=20, font=ctk.CTkFont('monospace',size=20))
    entry2.grid(row=1, column=1, sticky='ewns', pady=10, padx=10)


    def insert():
        unme = str(entry1.get())
        pwd = str(entry2.get())

        if (username, unme, pwd) in fields:
            print('Item not added as it already exists')
            return

        #if str(entry1.get()).replace(' ', '') != '' and str(entry2.get()).replace(' ', '') != '':
        if ' ' not in unme and ' ' not in pwd and unme!='' and pwd!='':
            print('inserting ' + unme + ' and '+ pwd + ' into passwords')
            scrollframe.add_item(unme,pwd)
            connection = sqlite3.connect("database.sqlite")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO passwords VALUES (?,?,?)",(username, unme, pwd))
            connection.commit()
            window2.destroy()


    add_btn = ctk.CTkButton(window2, text='Add', font=ctk.CTkFont('monospace',size=25), command=insert)
    add_btn.grid(row=2, column=0, sticky='ew', columnspan=2, padx=50)

    window2.mainloop()


# Used only for quick checking
#show('anish','asahoo')
