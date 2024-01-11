import queue
from time import sleep
import socket
import threading
import ServerUtilities as SU

HOST = "81.154.243.202"
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []
chat = []

recieved_queue = queue.Queue(0)

#broadcast
def broadcast(message):
    for client in clients:
        client.send(message)
#handle
def handle(client):
    while True:
        sleep(0.1)
        try:
            message = client.recv(1024)
            added = str(message.decode('utf-8'))
            if added.startswith("NICK"):
                nickname = added.removeprefix("NICK®")
                index = clients.index(client)
                nicknames[index] = nickname
                print(f"Nickname of client is {nickname}\n")

            elif added.startswith("WTDB"): # write to database
                values,columns,database,table = SU.from_code(added,"WTDB")
                SU.write_to_database(values,columns,database,table)

            elif added.startswith("FM"): #find messages
                username,reciever = SU.from_code(added,"FM")
                index = nicknames.index(username)
                chat[index] = reciever
                messagestr = SU.find_messages(username,reciever)
                messagestr = messagestr.encode('utf-8')
                client.send(messagestr)

            elif added.startswith("GFDB"): # get from database
                selection,conditions,database,table = SU.from_code(added,"GFDB")
                gotten = SU.get_from_database(selection,conditions,database,table)
                gotten = SU.to_code(gotten,"GFDB")
                gotten = gotten.encode('utf-8')
                client.send(gotten)

            elif added.startswith("*"): # to be displayed
                print("received_message")
                added = added.removeprefix("*")
                items = added.split("§")
                recievername = items[0]
                msg = items[1]
                print("found"+ msg)
                #adding to database
                index2 = clients.index(client)
                sendername = nicknames[index2]
                print(sendername)
                listtext = SU.get_from_database("messages",(f"reciever = '{recievername}'"),"Users.db",("¬"+sendername))
                text = listtext[0]
                text += "¶" + msg
                SU.update_table(("¬"+sendername),(f"messages = '{text}'"),(f"reciever = '{recievername}'"),"Users.db")
                SU.update_table(("¬"+recievername),(f"messages = '{text}'"),(f"reciever = '{sendername}'"),"Users.db")
                #displaying
                msg = "*"+msg
                msg = msg.encode('utf-8')
                client.send(msg)
                print("sent back")
                print(recievername)
                print(nicknames)
                if recievername in nicknames:
                    index = nicknames.index(recievername)
                    reciever = clients[index]
                    if chat[index]==sendername:
                        reciever.send(msg)
            elif added.startswith("CDB"): #create table for user
                database,username = SU.from_code(added,"CDB")
                SU.create_username_table(database,username)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            chatter = chat[index]
            chat.remove(chatter)
            break
#recieve
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with{str(address)}")
        clients.append(client)
        nicknames.append("")
        chat.append("")

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server running...")
receive()


