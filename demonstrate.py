import sqlite3
import os
from time import sleep
from prettytable import PrettyTable
import utility
import tkinter
from tkinter import *
import PIL
import io
from PIL import ImageTk, Image

def viewPost(user_id):
    post_id = int(input("Enter Post ID : "))
    try:
        conn = sqlite3.connect('userInfo')
        cursor = conn.cursor()
    except sqlite3.Error as error:
        exit()
    cursor.execute("SELECT post_content FROM post Where user_id = ? AND post_id = ?", (user_id,post_id,))
    record = cursor.fetchone()
    post_data = record[0]
    utility.write_file(post_data, "QueryOutput/" + str(post_id) + ".png")
    image1 = Image.open("QueryOutput/" + str(post_id) + ".png")
    root = Tk()
    image1 = Image.open("QueryOutput/" + str(post_id) + ".png")
    test = ImageTk.PhotoImage(image1)
    label1 = tkinter.Label(image=test)
    label1.image = test
    label1.place(x=0, y=0)
    root.title("Post | " + str(post_id))
    root.geometry("500x500")
    root.mainloop()
            
def viewFeed(user_id):
    utility.clear()
    tbl = PrettyTable()
    tbl.field_names = ["post_id", "post_type" , "Location", "Date and Time"]
    try:
        conn = sqlite3.connect('userInfo')
        cursor = conn.cursor()
    except sqlite3.Error as error:
        exit()
    cursor.execute("SELECT * FROM post Where user_id = ?", (user_id,))
    records = cursor.fetchall()
    for row in records:
        tbl.add_row([row[2],row[4],row[1],row[5]])
    print(tbl)
    choice = 'Y'
    while choice != "N":
        choice = input("View a particular post ? Y | N : ")
        if choice == 'Y':
            viewPost(user_id)
        else:
            break

def viewProfile(user_i):

    utility.clear()
    tbl = PrettyTable()
    tbl.field_names = ["FirstName", "LastName", "Email", "Gender", "Bio" , "Followers" , "Following"]
    try:
        conn = sqlite3.connect('userInfo')
        cursor = conn.cursor()
    except sqlite3.Error as error:
        exit()
    cursor.execute('SELECT * FROM user_info where user_id = ?', (user_i,))
    record = cursor.fetchone()
    cursor.execute('SELECT COUNT(user_id) FROM followers WHERE user_id = ?',(user_i,))
    followers = cursor.fetchone()
    cursor.execute('SELECT COUNT(user_id) FROM userFollowing WHERE user_id = ?',(user_i,))
    following = cursor.fetchone()
    tbl.add_row([record[1],record[2],record[3],record[4],record[5],followers[0],following[0]])
    print(tbl)
    cursor.execute("SELECT pics FROM profile_pics WHERE user_id = ? ",(user_i,))
    record = cursor.fetchone()
    filename = user_i
    if record != None:
        root = Tk()
        profile_pic = record[0]
        utility.write_file(profile_pic, "QueryOutput/" + filename + ".png")
        image1 = Image.open("QueryOutput/" + filename + ".png")

    else:
        root = Tk()
        filename = "blank-profile-picture"
        image1 = Image.open("profile_pics/" + filename + ".png")
    
    test = ImageTk.PhotoImage(image1)
    label1 = tkinter.Label(image=test)
    label1.image = test
    label1.place(x=0, y=0)
    root.title("Profile Pic")
    root.geometry("500x500")
    root.mainloop()
    
def updateProfile(user_i):
    utility.clear()
    try:
        conn = sqlite3.connect('userInfo')
        cursor = conn.cursor()
    except sqlite3.Error as error:
        exit()
    print('1. First Name')
    print('2. Last Name')
    print('3. Email')
    print('4. Gender')
    print('5. Bio')
    print('6. Profile Pic')
    infoToBeUpdated = int(input('Enter choice : '))
    if infoToBeUpdated == 1:
        info = input("Enter New First Name : ")
        cursor.execute(f'UPDATE user_info SET FirstName = ? WHERE user_id = ?',(info,user_i))
        conn.commit()
        conn.close()
    elif infoToBeUpdated == 2:
        info = input("Enter New Last Name : ")
        cursor.execute(f'UPDATE user_info SET LastName = ? WHERE user_id = ?',(info,user_i))
        conn.commit()
        conn.close()
    elif infoToBeUpdated == 3:
        info = input("Enter New Email : ")
        cursor.execute(f'UPDATE user_info SET Email = ? WHERE user_id = ?',(info,user_i))
        conn.commit()
        conn.close()
    elif infoToBeUpdated == 4:
        info = input("Enter Updated Gender : ")
        cursor.execute(f'UPDATE user_info SET Gender = ? WHERE user_id = ?',(info,user_i))
        conn.commit()
        conn.close()
    elif infoToBeUpdated == 5:
        info = input("Enter Updated Bio : ")
        cursor.execute(f'UPDATE user_info SET Bio = ? WHERE user_id = ?',(info,user_i))
        conn.commit()
        conn.close()
    elif infoToBeUpdated == 6:
        utility.clear()
        print("1. Delete Profile Pic")
        print("2. Update Profile Pic")
        internal_choice = int(input("Enter Choice : "))
        if internal_choice == 1:
            cursor.execute("DELETE FROM profile_pics WHERE user_id = ?", (user_i,))
            conn.commit()
            conn.close()
        elif internal_choice == 2:
            print('Pls Make sure that the file to be updated as profile pic is at location specified below !')
            path = input('Enter full Path : ')
            imageData = utility.convertToBinaryData(path)
            cursor.execute(f'UPDATE profile_pics SET pics = ? WHERE user_id = ?', (imageData,user_i,))
            conn.commit()
            conn.close()
    else:
        print('Wrong Option Choosen !')
        return



def authorize(user_id, password):
    try:
        conn = sqlite3.connect('userInfo')
        cursor = conn.cursor()
    except sqlite3.Error as error:
        exit()
    # sql_statement =
    cursor.execute('SELECT ID FROM account_info where ID=? AND password=?', (user_id, password))
    records = cursor.fetchone() 
    if(records != None):
        return user_id
    else:
        return None

def updateFeed(user_id):
    try:
        conn = sqlite3.connect('userInfo')
        cursor = conn.cursor()
    except sqlite3.Error as error:
        exit()
    print('1. Add a post')
    print('2. Delete a post')
    print('3. Edit a post')
    internal_choice = int(input('Enter Choice : '))
    if internal_choice == 1:
        post_type = input('Photo/Video : ')
        post_type.lower()
        location = input('Enter Location : ')
        location.lower()
        location[0].upper()
        path = input('Complete File Path : ')
        data = utility.convertToBinaryData(path)
        cursor.execute("INSERT INTO post (user_id, location , post_type, post_content) VALUES (?,?,?,?)", (user_id,location,post_type,data))
        conn.commit()
        conn.close()
    elif internal_choice == 2:
        viewFeed(user_id)
        post_id = int(input("Enter Post ID : "))
        cursor.execute("DELETE FROM post WHERE user_id = ? AND post_id = ? ", (user_id,post_id,))
        conn.commit()
        conn.close()
    elif internal_choice == 3:
        viewFeed(user_id)
        post_id = int(input('Enter post ID : '))
        print('1. Edit Location')
        print('2. Edit Content and Post Type')
        internal_choice2 = int(input('Enter Choice'))
        if internal_choice2 == 1:
            new_location = input('Enter New Location : ')
            cursor.execute(f'UPDATE post SET location = ? WHERE user_id = ?',(new_location,user_id))
            conn.commit()
            conn.close()
        if internal_choice2 == 2:
            path2 = input('Complete File Path : ')
            data2 = utility.convertToBinaryData(path2)
            new_post_type = lower(input("Enter New File Type : (Photo/Video"))
            cursor.execute(f'UPDATE post SET post_content = ? , post_type = ? WHERE user_id = ?',(data2,new_post_type,user_id))
            conn.commit()
            conn.close()

def main() :
    
    print("Welcome!")
    sleep(1)
    utility.clear()
    print("CONNECT RECONNECT ENDLESSLY | CRE")
    sleep(1.5)
    utility.clear()
    entered_userid = input("Enter User ID : ")
    entered_pass = input("Enter Password : ")

    token = authorize(entered_userid, entered_pass)
    
    if token != None:
        #user is authorised
        utility.clear()
        sleep(0.5)
        print('Welcome back',token+'!')
    else:
        #user is not authorised
        utility.clear()
        sleep(0.5)
        print('Bad luck!, Try again Next time')

    while token!=None:
        print('1. Profile Options')
        print('2. Feed Options')
        print('3. View Others')
        print('4. View Message Log')
        print('5. Security Options')
        print('6. Logout')
        print('7. Exit')
        choice = int((input('Enter Your Choice : ')))
        if choice == 1:
            utility.clear()
            print('1. View Profile')
            print('2. Update Profile')
            internal_choice = int(input("Enter further choice : "))
            if internal_choice == 1:
                utility.clear()
                viewProfile(token)
            elif internal_choice == 2:
                utility.clear()
                updateProfile(token)
                viewProfile(token)
        elif choice == 2:
            utility.clear()
            print('1. View Feed')
            print('2. Update Feed')
            internal_choice = int(input('Enter Choice : '))
            if internal_choice == 1:
                viewFeed(token)
            elif internal_choice == 2:
                updateFeed(token)
                viewFeed(token)
        elif choice == 3:
            utility.clear()
        elif choice == 4:
            utility.clear()
        elif choice == 5:
            utility.clear()
            pass_confirm = input('Enter your Password : ')
            try:
                conn = sqlite3.connect('userInfo')
                cursor = conn.cursor()
            except sqlite3.Error as error:
                exit()
            cursor.execute('SELECT password FROM account_info where ID=?', (token,))
            record = cursor.fetchone()
            if pass_confirm == record[0]:
                print('1. Change Password')
                internal_choice = int(input('Enter Choice : '))
                if internal_choice == 1:
                    try:
                        conn = sqlite3.connect('userInfo')
                        cursor = conn.cursor()
                    except sqlite3.Error as error:
                        exit()
                    new_password = input("Enter New Password : ")
                    confirm_new_pass = input("Confirm New Password : ")
                    if new_password == confirm_new_pass:
                        cursor.execute(f'UPDATE account_info SET password = ? WHERE ID = ?',(new_password,token))
                        conn.commit()
                        conn.close()
                    else:
                        print("Password doesn't match with provided password")
                        sleep(0.5)
                        print("Try Again!")
                else:
                    print('Wrong Choice Entered!')
            else:
                print('User Authentication Failed!')
                sleep(1.5)
                print('Try Again!') 
        elif choice == 6:
            token = None
            utility.clear()
            main()
        elif choice == 7:
            exit()
        else:
            print('Wrong Input Entered!')

main()