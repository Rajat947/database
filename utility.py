import os
def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
#INSERTING BLOB DATA
def to_raw(string):
    return fr"{string}"

def clear():
    os.system('cls')

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData