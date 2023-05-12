from interface import show
import customtkinter as ctk
import sqlite3

def logIn():
    global root
    #constructor and title
    root = ctk.CTk()
    root.title("Login")

    #layout and dimensions
    root.geometry("600x300")
    root.grid_columnconfigure((0), weight=1)
    root.grid_columnconfigure((1), weight=3)
    root.grid_rowconfigure((0,1,2), weight=0, pad=20)

    #labels and textboxes
    label1 = ctk.CTkLabel(root, text="Username:", font=ctk.CTkFont('monospace',size=25))
    label1.grid(row=0, column=0, padx=(20,20))

    label2 = ctk.CTkLabel(root, text="Password:", font=ctk.CTkFont('monospace',size=25))
    label2.grid(row=1, column=0,  padx=(20,20))

    global usernameInput
    usernameInput = ctk.CTkTextbox(root, 250, 40, font=ctk.CTkFont('monospace',size=25))
    usernameInput.grid(row=0,column=1, sticky='ew', padx=(0,20))

    global passwordInput
    passwordInput = ctk.CTkEntry(root, 250, 40, font=ctk.CTkFont('monospace',size=25), show='\u25CF', placeholder_text="password", placeholder_text_color='#737373')
    passwordInput.grid(row=1, column=1, sticky='ew', padx=(0,20))

    global errorMessageLabel
    errorMessageLabel = ctk.CTkLabel(root, text="", font=ctk.CTkFont(size=15, slant='italic'), text_color='RED')
    errorMessageLabel.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10)

    loginButton = ctk.CTkButton(root, 230, 60, text="Login", font=ctk.CTkFont('monospace',size=25), command=enter)
    loginButton.grid(row=3,column=0, columnspan=2, pady=10)

    root.mainloop()

def enter():
    errorMessageLabel.configure(text="")
    user_name = str(usernameInput.get(1.0, 'end-1c'))
    password = str(passwordInput.get())#1.0, 'end-1c'))

    usernameInput.delete(1.0,'end-1c')
    passwordInput.delete(0, ctk.END)#1.0, 'end-1c')

    if ' ' in user_name or ' ' in password:
        errorMessageLabel.configure(text="Username or password cannot contain spaces")
        return
    
    if user_name == '' or password == '':
        errorMessageLabel.configure(text="Username or password cannot be EMPTY")
        return

    print(user_name + " " + password)

    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    #search for the user in users table
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)
    connection.commit()
    connection.close()
    
    if (user_name,password) in result:
        print('success')
        global root
        root.destroy()
        show(user_name, password)
    else: 
        print('failure')