import socket
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5004
serversocket.bind((host, port))
client_address = {}
clients = {}
qwaitlist = {}
lwaitlist = {}
shortquestionasked = {}
longquestionasked = {}


def wait_connection():
    """
    Constantly wait for student/tutor connection.
    """
    while True:
        clientsocket, clientaddress = serversocket.accept()
        print(f"Received connection from {clientaddress}")
        client_address[clientsocket] = clientaddress
        Thread(target=handleclient, args=(clientsocket,)).start()


def handleclient(client):
    """
    Communicate with the client.

    Parameter:
        client: the student/ tutor.
    """
    name = client.recv(1024).decode("utf-8")
    clients[client] = name
    for student in qwaitlist:
        client.send(bytes(
            f"student: {student} , short question asked: {shortquestionasked[student]} , askedtime: {qwaitlist[student]}",
            "utf-8"))
    for student in lwaitlist:
        client.send(bytes(
            f"student: {student} , long question asked: {longquestionasked[student]} , askedtime: {lwaitlist[student]}",
            "utf-8"))
    while True:
        clientmsg = client.recv(1024).decode("utf-8")
        if clientmsg == "quit":
            client.close()
            del clients[client]
            del client_address[client]
            print(f"{name} has disconnected")
            break
        elif "student: " in clientmsg:
            print(clientmsg)
            update_waitlist(clientmsg)
        elif "deleted" in clientmsg:
            print(clientmsg)
            delete_student(clientmsg)
        elif "accepted" in clientmsg:
            print(clientmsg)
            accept_student(clientmsg)
        update_student(clientmsg, client)


def update_student(msg, sender):
    """
    Update student's information to everyone in the server except the student itself.

    Parameters:
        msg(str): message to be sent to the client.
        sender: the client who sent the message.
    """
    for client in client_address:
        if client == sender:
            continue
        else:
            client.send(bytes(msg, "utf-8"))


def update_waitlist(msg):
    """
    Update the waitlist.

    Parameter:
        msg(str): the message received from client.
    """
    name = msg.split()[1]
    askedtime = msg.split()[-1]
    questionasked = int(msg.split()[-4])
    if "short" in msg:
        qwaitlist[name] = float(askedtime)
        shortquestionasked[name] = questionasked
        print(qwaitlist)
        print(shortquestionasked)
    else:
        lwaitlist[name] = float(askedtime)
        print(lwaitlist)
        longquestionasked[name] = questionasked
        print(longquestionasked)


def delete_student(msg):
    """
    Delete student from waitlist.

    Parameter:
        msg(str): the message received from client.
    """
    name = msg.split()[1]
    if "short" in msg:
        if name in qwaitlist:
            del qwaitlist[name]
    else:
        if name in lwaitlist:
            del lwaitlist[name]


def accept_student(msg):
    """
    Add 1 to the number of questions asked by the student.

    Parameter:
        msg(str): the message received from client.
    """
    name = msg.split()[1]
    if "short" in msg:
        shortquestionasked[name] += 1
    else:
        longquestionasked[name] += 1
    delete_student(msg)


if __name__ == "__main__":
    serversocket.listen(100)
    wait_thread = Thread(target=wait_connection)
    wait_thread.start()
    wait_thread.join()
    serversocket.close()








