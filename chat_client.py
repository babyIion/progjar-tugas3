import socket
import sys
import threading

def read_mdg(socket_client):
    while True:
        # terima pesan
        data = socket_client.recv(65535)
        if len(data) == 0:
            break
        print(data)

# buat object socket
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect ke server
socket_client.connect(("127.0.0.1", 6666))

# kirim username ke server
socket_client.send(bytes(sys.argv[1], "utf-8"))

# buat thread untuk membaca pesan dan jalankan threadnya
thread_client = threading.Thread(target=read_mdg, args=(socket_client,))
thread_client.start()

while True:
    # kirim/terima pesan
    dest = input("Masukkan username tujuan (ketikkan bcast untuk broadcast pesan): ")
    msg = input("Masukkan pesan Anda: ")

    if msg == "exit":
        socket_client.close()
        break

    socket_client.send(bytes("{}|{}".format(dest, msg), "utf-8"))