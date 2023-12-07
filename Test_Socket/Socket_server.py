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


        # 데이터 송신
        # 클라이언트 방향으로 데이터를 전송한다
        data = client_socket.recv(1024)
        with open("./cat2.jpg", 'wb') as file:
            while data:
                file.write(data)
                data = client_socket.recv(1024)
        
        message = ""
        
        client_socket.close()
except KeyboardInterrupt:
    print("Key Board Interrupt irrupted")

finally:
    server_sock.close()


