

class Node:
    def __init__(self, data = None):
        self.__data = data
        self.__front:Node = None
        self.__backword:Node = None
        
    def setData(self, data):
        self.__data = data
        return
       
    def getData(self):
        return self.__data
    
    def setFront(self, node):
        self.__front = node 
        return 
    
    def setBackword(self, node):
        self.__backword = node 
        return 

    def getFront(self):
        return self.__front
    
    def getBackword(self):
        return self.__backword
    


class Linked_List:
    def __init__(self):
        self.__num_entry = 0
        self.__rear:Node = None
        self.__front:Node = None
        
    def isEmpty(self):
        if self.__num_entry == 0:
            return True
        else:
            return False
        
    def getRear(self):
        return self.__rear
        
    def getSize(self):
        return self.__num_entry
    
    def insertNode(self, data):
        new_node = Node(data=data)
        
        if not self.isEmpty():
            new_node.__front.setFront(self.__rear)
            self.__rear.setBackword(new_node)
            self.__front = new_node #front 지정
        
        self.__num_entry = self.__num_entry + 1
        self.__rear = new_node
        
        return new_node
        
        
    def removeNode(self, node:Node):
        node.getFront().setBackword(node.getBackword())
        node.getBackword().setFront(node.getFront())
        node.setData(None)
        node = None  # Free
        return
        
    def searchNode(self, node:Node):
        now_node = self.__rear
        
        while now_node.getFront() == None:
            if now_node == node:
                break
            now_node = now_node.getFront()

        if now_node == self.__front:
            return -1
        else:
            return now_node
        
    
        
        