import socket
from threading import Thread
from time import sleep

from controller import Master_Controller
from constant import HOST, PORT, BUFFER_SIZE


"""
socket.socket의 accept()를 통해 반환된 데이터를 보관하기 위한 클래스
소켓을 통한 송신 수신 기능을 포함한다.
"""
class Socket:
    def __init__(self, socket, addr):
        self.__socket = socket
        self.__addr = addr
    
    #주소 데이터 반환
    def get_addr(self):
        return self.__addr

    # 데이터 받기
    # data = <데이터타입>:<본문>
    # head = 데이터 타입  ('FILE', "STRING")
    # body = 본문
    def recive_data(self, buffuer_size = BUFFER_SIZE):
        data:bytes = self._client_socket.recv(buffuer_size)
        decoded_data = data.decode()
        head, body= self.__recognize_protocol(data = decoded_data)
        print(f"{head}Received Data : {body}")
        return head, body   


    # String 보내기
    def send_data(self, data:str):
        encoded_data = data.encode()
        self._client_socket.sendall(encoded_data)
        return 

    # 파일전송
    def send_file(self, data:bytes):
        self._client_socket.sendall(data)
        return
    
    # 프로토콜 분석
    def __recognize_protocol(self, data:str):
        data_parts = data.split(":")
        return data_parts[0], data_parts[1:]



"""
Client를 정의하기 위한 클래스  (위의 Socket 클래스를 상속)
_id : 클라이언트 번호
_data : 필수 데이터 (head, bid, target)
_flag : 데이터가 처리 되었다는 것을 알려주기 위한 세마포어
"""
class Client(Socket):
    def __init__(self, id, client_socket:socket.socket, addr:socket._RetAddress):
        self._id:int = id
        self._data = {'head':'default', 'bid':'-1', 'target':'default'}
        self._flag = False
        super.__init__(client_socket, addr)


    def get_client_id(self):
        return self._id

    def get_data(self):
        return self._data

    def set_data(self, bid:str, target:str):
        self._data['bid'] = bid
        self._data['target'] = target
        return


    def isDataReady(self):
        return self._flag

    def dataReady(self):
        self._flag = True
        return

    def dataReset(self):
        self._flag = False
        return


class AppServer:
    def __init__(self):
        self.num_client = 0

        # 소켓 세팅
        self.init_socket()

        # 클라이언트 대기
        self.waiting_client()


    def init_socket(self):

        # 소켓 생성
        # AF_INET : IPv4,  AF_INET6 : IPv6
        # SOCK_STREAM : TCP, SOCK_DGRAM : UDP
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 서버 바인딩
        self.__server_socket.bind((HOST, PORT))
        print(f"SYSTEM_CALL||Server Running at {HOST}:{PORT}")

        # 클라이언트 대기
        self.__server_socket.listen()
        print("SYSTEM_CALL||Socket Ready and Initialized")


    def waiting_client(self, client_list:list):
        terminate_flag = False
        print("SYSTEM_CALL||Waiting for Client...")
        try:
            while True:
                # 클라이언트 연결
                client_socket, addr = self.__server_socket.accept()
                print(f"Client Connected : {addr}")

                # 다중 연결을 위한 멀티 스레드 생성
                client = Client(len(client_list), client_socket, addr)

                new_client = Thread(target=self.__client_handle, 
                                    args=(client, client_list, terminate_flag,))
                client_list.append(new_client)
                new_client.start()
            
                
        except KeyboardInterrupt:
            print("SYSTEM_CALL||Key Board Interrupt irrupted")
            print("SYSTEM_CALL||Closing System")

        except Exception as e:
            print("SYSTEM_ERROR||{e}")
            print("SYSTEM_CALL||Closing System")

        finally:
            print("SYSTEM_CALL||terminate all")
            terminate_flag = True
            sleep(1.0)
            self.__server_socket.close()

    # 클라이언트 처리 함수 (멀티 스레드로 운영됨)
    # 매게변수(client_socket)
    def __client_handle(self, client:Client, client_list, terminate_flag):
        print(f"SYSTEM_CALL||Start to Comunicate {client.get_addr()}")
        
        num_client = 0
        FILE_NAME = f"sample{num_client}.wav"

        while not terminate_flag:
            head, body = client.recive_data()

            if head == "FILE":
                with open(FILE_NAME, 'wb') as file:
                    while body:
                        file.write(body)
                        head, body = client.recive_data()
                    # 여기서 데이터를 head와 파일이름으로  해서 전달
                    # client_list[i] = (head, FILE_NAME) 이런 느낌
                    # client가 생길테니 거기다 넣는게 맞음
                message = "wait"
                client.send_data(message)


            if head == "STRING":
                bid = body[0]
                target = body[1]

                # 여기서 데이터를 head와 데이터 두개를 전달
                # client_list[i] = (head, bid, target) 이런 느낌
                # client가 생길테니 거기다 넣는게 맞음