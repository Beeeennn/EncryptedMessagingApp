from time import sleep as s
from random import randint as r
import Utilities as U

class User():
    def __init__(self,user):
        self.user = user
    def login(self,username,password):
        hash = U.hash(password)
        required_password = U.get_from_database("Hashkey",("Username = '"+username+"'"),"Users.db","user",self.user)
        if required_password != None:
            if required_password[0] == hash[1:-1]:
                send = "NICK®"+username
                self.user.write(send)
                self.user.nickname = username
                return True
            else:
                return False
        else:
            return False
    
    def create_account(self,username,password,password_check,email):
        Ucase,Uaccept = U.validate_username(username,3,13,self.user)
        Pcase,Paccept = U.validate_password(password,password_check,5,15)
        if Uaccept:
            if Paccept:
                hashed = U.hash(password)
                U.write_to_database([username,hashed[1:-1],email],["Username","Hashkey","Email"],"Users.db","user",self.user)
                U.create_username_table("Users.db",username,self.user)
                return 99,99,True
            else:
                return 0,Pcase,False
        else:
            return 1,Ucase,False