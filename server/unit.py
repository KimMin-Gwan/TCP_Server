import socket
from threading import Thread
from time import sleep
import shutil

from controller import Master_Controller
from constant import HOST, PORT, BUFFER_SIZE
from linkedList import Linked_List, Node
from common import Client


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
        terminate_flag = [False]
        print("SYSTEM_CALL||Waiting for Client...")
        try:
            while True:
                # 클라이언트 연결
                client_socket, addr = self.__server_socket.accept()
                print(f"Client Connected : {addr}")
                self.__num_client = self.__num_client + 1
                # 다중 연결을 위한 멀티 스레드 생성
                client = Client(self.__num_client, client_socket, addr)
                print("hello")
                client_node = client_list.insertNode(client)

                client_thread = Thread(target=self.__client_handle, 
                                    args=(client_node, client_list, terminate_flag,))
                client.set_thread(client_thread)
                client_thread.start()
                
        except KeyboardInterrupt:
            print("SYSTEM_CALL||Key Board Interrupt irrupted")
            print("SYSTEM_CALL||Closing System")

        except Exception as e:
            print(f"SYSTEM_ERROR||{e}")
            print("SYSTEM_CALL||Closing System")

        finally:
            print("SYSTEM_CALL||terminate all")
            terminate_flag[0] = True
            sleep(1.0)
            self.__server_socket.close()

    # 클라이언트 처리 함수 (멀티 스레드로 운영됨)
    # 매게변수(client_socket)
    def __client_handle(self, client_node:Node, client_list:Linked_List, terminate_flag:list):
        client:Client = client_node.getData()
        print(f"SYSTEM_CALL||Start to Comunicate {client.get_addr()}")
        
        FILE_NAME = f"./sample{client.get_client_id()}.wav"

        while not terminate_flag[0]:
            head, body = client.recive_data()
            client.send_data("FILE")

            if head == "FILE":
                with open(FILE_NAME, 'wb') as file:
                    file_length = 0
                    data = client.recive_file()   
                    while data :
                        file_length += len(data)
                        file.write(data)
                        if file_length >= int(body[0]):
                            break
                        data = client.recive_file()
                        
                sleep(1)
                save_path = f"./sample{client.get_client_id()}.wav" 
                #with open(save_path, "wb") as f:
                    #shutil.copyfileobj(file, f) # 받은 파일 저장
                print(f"SYSTEM_CALL||WAV_File_Saved_to_{save_path}")
                client.set_head("FILE")
                client.dataCompletelyCame()

            elif head == "STRING":
                bid = body[0]
                target = body[1]
                
                client.set_BidnTarget(bid=bid, target=target)
                client.set_head("STRING")
                client.dataCompletelyCame()
                
            elif head == "END":
                client.set_head("END")
                client.close_socket()
                try:
                    client_list.removeNode(client_node)
                except Exception as e:
                    return
                break

            while not client.get_flag() == "Ready":
                sleep(0.5)
                
            
            client.send_result(client.get_data()['result'])
            client.dataReset()
        return
            
            
                
            
                
        
                
    
        