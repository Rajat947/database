import sqlite3
#INSERTING BLOB DATA
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
def insertBlobData(user_id, pics):
    try:
        sqliteConnection = sqlite3.connect('userInfo')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO profile_pics
                                  (user_id,pics) VALUES (?, ?)"""
        
        profile_pic = convertToBinaryData(pics)
        data_tuple = (user_id, profile_pic)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image inserted successfully as a BLOB into a table")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
insertBlobData("Prateek",r"C:\Users\Rahul Kakkar\Desktop\Rahul\database\profile_pics\prateek_pic.jpg")