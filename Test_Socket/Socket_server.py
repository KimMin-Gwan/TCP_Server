import socket

# 소켓 생성
# AF_INET : IPv4,  AF_INET6 : IPv6
# SOCK_STREAM : TCP, SOCK_DGRAM : UDP
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 바인딩
HOST = '127.0.0.1'
PORT = 9999
server_sock.bind((HOST, PORT))

# 클라이언트 대기
server_sock.listen()

print(f"Server Running and Waiting Client : {HOST}:{PORT}")

try :
    while True:
        # 클라이언트 연결
        client_socket, addr = server_sock.accept()
        print(f"Client Connected : {addr}")

        # 데이터 수신
        # 클라이언트로 부터 데이터를 전송 받는다
        DATA_SIZE = 1024
        data = client_socket.recv(DATA_SIZE)
        recived_data = data.decode()
        print("Received Data : ", recived_data)

        # 데이터 송신
        # 클라이언트 방향으로 데이터를 전송한다
        message = "Hello, Client!"
        encoded_data = message.encode()
        client_socket.sendall(encoded_data)

        client_socket.close()
except KeyboardInterrupt:
    print("Key Board Interrupt irrupted")

finally:
    server_sock.close()


