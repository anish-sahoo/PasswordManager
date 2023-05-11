import time

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