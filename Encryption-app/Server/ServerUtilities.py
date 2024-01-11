from email.headerregistry import HeaderRegistry
import hashlib
from http.client import FOUND
from multiprocessing import connection
import sqlite3
from time import sleep

def write_to_database(values,columns,database,table):
    str1 = "','".join(str(e) for e in columns)
    columnsstr = (f"('{str1}')")
    str2 = "','".join(str(e) for e in values)
    valuesstr = (f"('{str2}')")
    statement = (f"INSERT INTO {table} {columnsstr} VALUES {valuesstr}")
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    cursor.close()


def get_from_database(selection,conditions,database,table):

    statement = str("SELECT "+selection+" FROM "+table)
    if conditions != "None":
        statement += " WHERE "+conditions
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(statement)
    found = cursor.fetchall()
    cursor.close()
    final = []
    for item in found:
        final += item
    return final

def create_username_table(database,username):
    username = "¬"+username
    statement = (f"CREATE TABLE '{username}' ('reciever' TEXT PRIMARY KEY, 'messages' TEXT )")
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    cursor.close()

def find_messages(username,reciever):
    username = "¬"+username
    existing = False
    friends = get_from_database("reciever","None","Users.db",username)
    for friend in friends:
        if friend == reciever:
            existing= True
    if existing:
        statement = (f"SELECT messages FROM {username} WHERE reciever = '{reciever}'")
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        cursor.execute(statement)
        found = cursor.fetchall()
        cursor.close()
        final = found[0]
    else:
        write_to_database([reciever,""],["reciever","messages"],"Users.db",username)
        if str(username) == str("¬"+reciever):
            pass
        else:
            username = username.removeprefix("¬")
            reciever = "¬"+reciever
            write_to_database([username,""],["reciever","messages"],"Users.db",reciever)
        final = ""
    final = to_code(final,"FM")
    return final

def update_table(table,change,conditions,database):
    statement = (f"UPDATE {table} SET {change}")
    if not (conditions == "None"):
        statement = statement+" WHERE "+conditions
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    cursor.close()

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
