import hashlib
from http.client import FOUND
from multiprocessing import connection
from time import sleep

def hash(password):
    plaintext = (str(password)).encode()
    d = hashlib.sha256(plaintext)
    hash = d.digest()
    hash = (str(hash)).lstrip("b")
    hash = hash.replace("'","")
    return (hash)

def write_to_database(values,columns,database,table,user):
    items = [values,columns,database,table]
    coded = to_code(items,"WTDB") #write to database
    user.write(coded)

def get_from_database(selection,conditions,database,table,user):
    items = [selection,conditions,database,table]
    coded = to_code(items,"GFDB") #get from database
    user.write(coded)
    while user.from_database == "":
        pass
    final = user.from_database
    final = from_code(final,"GFDB")
    user.from_database = ""
    return final

def check_username_exists(username,user):
    correct = False
    for i in get_from_database("Username","None","Users.db","user",user):
        if i == username:
            correct = True
    return correct

def validate_username(username,min_length,max_length,user):
    if not check_username_exists(username,user):
        if (len(username)<=min_length) or (len(username)>=max_length):
            return (0,False)
        else:
            return(2,True)
    else:
        return(1,False)

def validate_password(password1,password2,min_length,max_length):
    specialCharacters = "!£$%^&*()_+-={}[]:@~;'#<>?,./"
    if password1 == password2:
        if any(c in specialCharacters for c in password1):
            if (len(password1)<=min_length) or (len(password1)>=max_length):
                return (0,False)
            else:
                return(3,True)
        else:
            return(1,False)
    else:
        return(2,False)

def casechecker(case1,case2):
    caselist = [["Please choose a password between 5 and 15 characters long","Make sure your password contains at least 1 special character","your passwords dont match"],
                ["Please choose a username between 4 and 13 characters long","That username already exists","error"]]

    error_msg = caselist[case1][case2]
    return error_msg


def find_messages(username,reciever,user):
    items = [username,reciever]
    coded = to_code(items,"FM") # create database
    user.write(coded)
    while user.new_messages == "":
        pass
    final = user.new_messages
    final = from_code(final,"FM")
    user.new_messages = ""
    return final

def create_username_table(database,username,user):
    items = [database,username]
    coded = to_code(items,"CDB") # create database
    user.write(coded)

def send_message(text,reciever,user):
    to_send = "*"+reciever+"§"+text
    user.write(to_send)


def validate_message(message):
    not_allowed_Characters = "•®©§"
    if any(c in not_allowed_Characters for c in message):
        return False
    else:
        return True


def to_code(items,prefix):
    coded = ""
    for i in items:
        if isinstance(i, list):
            for j in i:
                coded += str(j)+"•"
            coded = coded[:-1]
            coded +="©§"
        else:
            coded += str(i)+"§"
    coded = coded[:-1]
    coded = prefix + "®" + coded
    return coded

def from_code(coded,prefix):
    decoded = coded.removeprefix(prefix+"®")
    decoded = decoded.split("§")
    for i in range(len(decoded)):
        if "©" in decoded[i]:
            decoded[i]=decoded[i].strip("©")
            decoded[i]=decoded[i].split("•")
    return decoded