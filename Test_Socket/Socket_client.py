import socket

# 소켓 생성
# AF_INET : IPv4,  AF_INET6 : IPv6
# SOCK_STREAM : TCP, SOCK_DGRAM : UDP
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 서버에 연결
HOST = '127.0.0.1'
PORT = 9999
client_sock.connect((HOST, PORT))

# 데이터 수신
# 서버로 부터 데이터를 받는다
DATA_SIZE = 1024

with open('./cat.jpg', 'rb') as file:
    data = file.read(1024)
    while data:
        client_sock.sendall(data)
        data = file.read(1024)


data = client_sock.recv(DATA_SIZE)
decoded_data = data.decode()
print("Received data : ", decoded_data)

client_sock.close()





