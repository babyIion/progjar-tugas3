import socket
import threading

def read_msg(clients, sock_client, addr_client, username_client):
    while True:
        # terima pesan
        data = sock_client.recv(65535)
        if len(data) == 0:
            break
        
        # parsing pesannya
        dest, msg = data.decode("utf-8").split("|")
        msg = "<{}>: {}".format(username_client, msg)

        if dest == "bcast":
            # teruskan pesan ke semua client
            send_broadcast(clients, data, addr_client)
        else:
            dest_sock_client = clients[dest][0]
            send_msg(dest_sock_client, msg)    
        print(data)

    sock_client.close()
    print("Connection closed", addr_client)

# kirim ke semua klien
def send_broadcast(clients, data, sender_addr_client):
    for sock_client, addr_client, _ in clients.values():
        if not (sender_addr_client[0] == addr_client[0] and sender_addr_client[1] == addr_client[1]):
            send_msg(sock_client, data)

def send_msg(socket_client, data):
    sock_client.send(bytes(data, "utf-8"))

# membuat object socket server
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind object socket ke alamat ip dan port
sock_server.bind(("0.0.0.0", 6666))

# listen for an incoming connection
# 5 --> backlog, maksimum antrian (queue) untuk incoming connection
sock_server.listen(5)

# buat dictionary untuk menyimpan informasi tentang client
clients = {}

while True:
    # accept connection from client
    sock_client, addr_client = sock_server.accept()

    # baca username client
    username_client = sock_client.recv(65535).decode("utf-8")
    print(username_client, "joined")

    #  buat thread baru untuk membaca pesan
    thread_client = threading.Thread(target=read_msg, args=(clients, sock_client, addr_client, username_client))
    thread_client.start()

    # simpan informasi tentang client ke dictionary
    clients[username_client] = (sock_client, addr_client, thread_client)