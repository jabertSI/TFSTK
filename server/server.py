import socket
import threading


class ThreadClient(threading.Thread):
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.port = port
        self.clientsocket = clientsocket
        self.ip = ip
        print("[+] Thread for %s %s" % (self.ip, self.port,))

    def run(self):
        print("Connexion from %s %s" % (self.ip, self.port,))
        y = self.clientsocket.recv(1024)
        if y == b'putScore':
            copi_c = False
            drop_nicksc = False
            drop_score = False
            file = ('data\high_score.txt')
            if not copi_c:
                if not drop_nicksc:
                    cmd_serv = b'dropNickSc'
                    clientsocket.send(cmd_serv)
                    new_player = clientsocket.recv(2048).decode()
                    drop_nicksc = True
                    print(new_player)
                if drop_nicksc:
                    do_insert = True
                    #Check if same score exists
                    with open(file, "r") as f:
                        for l in f.readlines():
                            l = l.strip()
                            if l == new_player:
                                print("Score already present")
                                do_insert = False
                    if do_insert:
                        with open(file, "a") as classement:
                            classement.write(('\n')+new_player)

                with open(file, "r") as top_3:
                    top_3 = top_3.read()
                    lines = top_3.split("\n")
                top = list()

                for i in lines:
                    res = i.split()
                    if len(res) > 1:
                        top.append([res[0], int(res[1])])

                top_sorted = sorted(top, reverse=True, key=lambda x: x[1])
                # print(top_sorted[:3])
                first_score = top_sorted[0]
                best = first_score[0] + " " + str(first_score[1])
                print(top_sorted[:3])
                if new_player == best:
                    print("best score")
                    clientsocket.send(b'a')

                else:
                    print("Not the best score")
                    clientsocket.send(b'b')


                print("The high score's file has been update : %s." % file)

        else:
            print("Command not understood", y)




tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind(("", 1111))

while True:
    tcp.listen(10)
    print("Litsen...")
    (clientsocket, (ip, port)) = tcp.accept()
    newthread = ThreadClient(ip, port, clientsocket)
    newthread.start()