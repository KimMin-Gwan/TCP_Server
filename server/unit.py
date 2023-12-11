import socket
from threading import Thread
from time import sleep
import shutil

from controller import Master_Controller
from constant import HOST, PORT, BUFFER_SIZE
from linkedList import Linked_List, Node
from common import Client

# Transport Layer에서 동작하는 TCP_Server 구현
class TCP_Server:
    def __init__(self, host, port):
        self.__num_client = 0

        # 소켓 세팅
        self.__init_socket(host, port)

        # 클라이언트 대기
        #self.waiting_client()


    def __init_socket(self, host, port):

        # 소켓 생성
        # AF_INET : IPv4,  AF_INET6 : IPv6
        # SOCK_STREAM : TCP, SOCK_DGRAM : UDP
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 서버 바인딩
        self.__server_socket.bind((host, port))
        print(f"SYSTEM_CALL||Server Running at {host}:{port}")

        # 클라이언트 대기
        self.__server_socket.listen()
        print("SYSTEM_CALL||Socket Ready and Initialized")


    def waiting_client(self, client_list:Linked_List):
        # 종료 플래그
        terminate_flag = [False]
        print("SYSTEM_CALL||Waiting for Client...")
        try:
            while True:
                # 클라이언트 연결
                client_socket, addr = self.__server_socket.accept()
                print(f"SYSTEM_CALL||Client Connected : {addr}")
                self.__num_client = self.__num_client + 1

                # 클라이언트를 처리하기 위해 객체로 설정 후 리스트에 삽입
                # Client는 Socket 정보를 처리하는 Socket 클래스를 상속함
                client = Client(self.__num_client, client_socket, addr)
                client_node = client_list.insertNode(client)

                # 다중 연결을 위한 멀티 스레드 생성
                client_thread = Thread(target=self.__client_handle, 
                                    args=(client_node, client_list, terminate_flag,))
                client.set_thread(client_thread)  # 클라이언트에 스레드 객체 보관
                client_thread.start()
                
        # Ctrl + C 입력시 서버 작동 중지
        except KeyboardInterrupt:
            print("SYSTEM_CALL||Key Board Interrupt irrupted")
            print("SYSTEM_CALL||Closing System")

        # 이외의 모든 에러에 대한 처리
        except Exception as e:
            print(f"SYSTEM_ERROR||{e}")
            print("SYSTEM_CALL||Closing System")

        # 자식 스레드를 모두 종료 시키고 소켓 종료
        finally:
            print("SYSTEM_CALL||terminate all")
            terminate_flag[0] = True
            sleep(1.0)
            self.__server_socket.close()

    # 클라이언트 처리 함수 (멀티 스레드로 운영됨)
    # 매게변수(client_node, client_list, terminateflag)
    def __client_handle(self, client_node:Node, client_list:Linked_List, terminate_flag:list):
        client:Client = client_node.getData() # 노드에서 클라이언트 뽑아오기
        print(f"SYSTEM_CALL||Start to Comunicate {client.get_addr()}")
        
        save_path = f"./sample{client.get_client_id()}.wav"

        # 부모스레드에서 정지 명령이 내려오기 전까지 동작
        while not terminate_flag[0]:
            # 데이터를 클라이언트에게서 받아옴
            head, body = client.recive_data()
            client.send_data("Recive Data:{head}")

            # head가 FILE로 설정되었다면 FILE을 받도록 함 
            # head가 FILE이라면 body는 파일의 길이
            if head == "FILE":
                # 파일을 받자마자 저장할 것
                with open(save_path, 'wb') as file:
                    file_length = 0
                    data = client.recive_file() # 파일의 첫번째 데이터를 받아옴
                    # 데이터값이 있다면 바로 진행
                    while data :
                        file_length += len(data) # 파일 길이를 확인
                        file.write(data) # 파일 쓰기
                        # 만약 파일 길이가 초기에 설정된 길이를 넘었다면 그만 쓰기
                        if file_length >= int(body[0]):
                            break
                        # 다음 파일 데이터 받아오기
                        data = client.recive_file()
            
                sleep(1) # 파일이 저장되기 까지 잠시 대기
                print(f"SYSTEM_CALL||WAV_File_Saved_to_{save_path}")
                # 헤드를 설정
                client.set_head("FILE")
                # 데이터 다 받았다고 APP서버에 알림
                client.dataCompletelyCame()

            # 만약 헤드가 STRING으로 오면 bid와 target 수령하기
            elif head == "STRING":
                bid = body[0]
                target = body[1]
                # bid와 target 설정
                client.set_BidnTarget(bid=bid, target=target)
                # 헤드값 변경
                client.set_head("STRING")
                # 데이터 다 받았다고 APP서버에 알림
                client.dataCompletelyCame()
                
            # 소켓 종료를 알림
            # 여긴 연구가 더 필요함
            # 더미 데이터 보내고 1초 후 종료로 설정하기 바람
            elif head == "END":
                client.set_head("END")
                client.close_socket()
                try:
                    client_list.removeNode(client_node)
                except Exception as e:
                    return
                break
                
            # 위의 일련 과정이 종료되면 데이터 보내기 준비
            while not client.get_flag() == "Ready":
            # APP서버에서 모든 과정이 끝나면 아래로 진행
                sleep(0.5)
                
            # 클라이언트에게 모든 연산 결과값(TTS용 TEXT) 전송
            client.send_result(client.get_data()['result'])
            # flag 초기화
            client.dataReset()
        return
            
            
                
            
                
        
                
    
        