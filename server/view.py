from controller import Master_Controller
from linkedList import Linked_List, Node
from unit import TCP_Server
from common import Client
from constant import HOST, PORT
from threading import Thread

# APP Layer에서 동작하는 APP_Server
class APP_Server():
    def __init__(self, controller):
        # TCP_Server 초기화
        self.__app = TCP_Server(host = HOST, port = PORT)
        # 컨트롤러 준비
        self.__controller:Master_Controller = controller
        # 클라이언트 관리용 List
        self.__client_list = Linked_List()
        
    # 서버 시작을 위한 공개 함수
    def run_system(self):
        #데이터 처리를 위한 route준비 (멀티 스레드)
        thread = Thread(target=self.__route) 
        thread.start()
        # TCP 서버는 메인 스레드를 사용하여 동작 
        # (TCP 서버가 죽으면 자식 스레드가 다죽어야되서 그런가봄)
        self.__app.waiting_client(self.__client_list)
        
    # 클라이언트의 입장 루트 생성기
    def __route(self):
        threads = []
        now_count = 0 # APP서버에서 확인된 클라이언트 수
        while True:
            
            # 클라이언트가 추가되면 루트 생성 및 실행
            # self.__client_list.getSize() == TCP서버에서 추가된 클라이언트 수
            if self.__client_list.getSize() > now_count:
                now_count = now_count + 1 # 현재 클라이언트 수 증가
                # 데이터 처리 루트 생성 및 실행
                thread = Thread(target = self.__data_process, args=(self.__client_list.getRear(), ))
                threads.append(thread) #여기 변경 필요
                thread.start()
            
            # 반대로 클라이언트 빠져나갔으면 클라이언트 수 줄이기
            elif self.__client_list.getSize() < now_count:
                now_count = now_count - 1
            
            else:
                continue
        
    def __data_process(self, client_node:Node):
        while True:
            # client 가 미리 선언되어야함
            client = None
            try:
                while True:
                    client:Client = client_node.getData()
                    # 데이터가 준비되면 flag가 Set 이 됨
                    if client.get_flag() == "Set":
                        break
                
                # 헤드가 END면 데이터 프로세스 할 필요없음
                if client.get_data()['head'] == "END":
                    # 종료 
                    break
                
                # 데이터 확인하기
                data = client.get_data()

                # 헤드가 FILE이면 파일 처리 컨트롤러로 연결
                if data['head'] == "FILE":
                    result = self.__controller.makeWAV2Text(client.get_client_id())
                    
                # 헤드가 STRING이면 최단 거리 찾기 컨트롤러로 연결
                elif data['head'] == "STRING":
                    bid = data['bid']
                    target = data['target']
                    result = self.__controller.getShortestPath(bid=bid, target=target)
                    
                # 헤드가 END면 데이터 프로세스 할 필요없음
                if client.get_data()['head'] == "END":
                    # 종료 
                    break
                
                # 결과값 세팅
                client.set_result(result=result)
                # 클라이언트에게 데이터 보낼 준비 끝
                client.dataReady2Send()
            except:
                print("SYSTEM_CALL||Client Deleted")
                break
        return
            
            
        
        
        

