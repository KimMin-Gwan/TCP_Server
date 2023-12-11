
# 링크드 리스트의 노드
class Node:
    def __init__(self, data = None):
        self.__data = data
        self.__front:Node = None
        self.__backword:Node = None
        
    # 노드에 데이터 세팅
    def setData(self, data):
        self.__data = data
        return     
    
    # 앞의 노드를 선정
    def setFront(self, node):
        self.__front = node 
        return 
    
    # 뒤의 노드를 선정
    def setBackword(self, node):
        self.__backword = node 
        return 

    def getData(self):
        return self.__data

    def getFront(self):
        return self.__front
    
    def getBackword(self):
        return self.__backword
    
"""
Double Linked_List로 구현 (삽입과 삭제가 빠름)
Circular Queue로 구현하면 동기 서버에 적절
그러나 이번 APP 서버는 비동기 서버라서 다른 자료구조를 사용
"""
class Linked_List:
    def __init__(self):
        self.__num_entry = 0
        self.__rear:Node = None
        self.__front:Node = None
    
    # 리스트가 비었는지 확인
    def isEmpty(self):
        if self.__num_entry == 0:
            return True
        else:
            return False
        
    def getRear(self):
        return self.__rear
        
    def getSize(self):
        return self.__num_entry
    
    # 노드 삽입
    def insertNode(self, data):
        new_node = Node(data=data)
        
        # 초기상태에서 접근이 아닐 때
        if not self.isEmpty():
            new_node.__front.setFront(self.__rear) # 앞을 설정
            self.__rear.setBackword(new_node)  #뒤를 설정
        else:
            self.__front = new_node # 가장 처음 들어온 노드 설정
        
        self.__num_entry = self.__num_entry + 1 # 노드 수 추가
        self.__rear = new_node  # 맨 마지막에 들어온 노드
        
        return new_node
        
    # 노드 삭제
    def removeNode(self, node:Node):
        self.__front = node.getBackword() # 가장 먼저 들어온 노드 초기화
        # 앞의 노드와 뒤 노드 연결
        node.getFront().setBackword(node.getBackword()) 
        node.getBackword().setFront(node.getFront())
        # 데이터 지우기 (필요없을 지도 모름 : Garbage 컬랙터가 처리해준다)
        node.setData(None)
        # node 비우기 
        node = None  # Free
        return
        
    # Node 검색
    def searchNode(self, node:Node):
        now_node = self.__rear
        
        # 맨 뒤에서 부터 앞으로 하나씩 탐색
        while now_node.getFront() == None:
            if now_node == node:
                break
            now_node = now_node.getFront()

        # 못찾으면 -1을 반환
        if now_node == self.__front:
            return -1
        else:
            return now_node
        
    
        
        