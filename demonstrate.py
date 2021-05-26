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
    sql_statement = """  SELECT * FROM account_info """ 
    cursor.execute(sql_statement)
    records = cursor.fetchall()
    flag = 0
    for row in records:
        if user_id == row[0]:
            if password == row[1]:
                flag = 1  
    if(flag):
        return user_id
    else:
        return None

value = authorize(entered_userid, entered_pass)
if value != None:
    print('User is Authorized')
else:
    print('User Not Authorized')