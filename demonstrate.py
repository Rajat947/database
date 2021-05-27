import sqlite3


entered_userid = input("Enter User ID : ")
entered_pass = input("Enter Password : ")

def authorize(user_id, password):
    try:
        conn = sqlite3.connect('userInfo')
        cursor = conn.cursor()
        print('connected successfully..')
    except sqlite3.Error as error:
        print("Failed to connect..")
        exit()
    # sql_statement =
    cursor.execute('SELECT ID FROM account_info where ID=? AND password=?', (user_id, password))
    records = cursor.fetchone() 
    if(records != None):
        return user_id
    else:
        return None

value = authorize(entered_userid, entered_pass)
if value != None:
    print('User is Authorized')
    print('Welcome back',value+'!')
else:
    print('User Not Authorized')