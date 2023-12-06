


class CircularQ:
    def __init__(self, size = 10):
        self._size = size
        self._num_entries = 0
        self.__que = [None] * size
        self._front = self._rear = -1

    def inQue(self, entry):
        self.que[self.front]

    def is_empty(self):
        if self.front == -1:
            return True
        else:
            return False
    
    def is_full(self):
        if (self.rear + 1) % self.size == self.front:
            return True
        else
            return False
        
    def enqueue(self, entry):
        if self.is_full():
            print("SYSTEM_ERROR||Queue is full")
            print("SYSTEM_ERROR||")
            return 
        
        if self.is_empty():
            self._front = self._rear = 0
        else:
            self._rear = (self._rear + 1) % self._size

        self.__que[self.rear] = entry
        print(f"SYSTEM_CALL||ENQUEUED {entry}")

    def dequeue(self):

    

class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = self.rear = -1

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    def enqueue(self, item):
        if self.is_full():
            print("Queue is full. Cannot enqueue.")
            return
        elif self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity

        self.queue[self.rear] = item
        print(f"Enqueued: {item}")

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty. Cannot dequeue.")
            return None

        item = self.queue[self.front]

        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity

        print(f"Dequeued: {item}")
        return item

    def peek(self):
        if self.is_empty():
            print("Queue is empty.")
            return None
        return self.queue[self.front]

    def display(self):
        if self.is_empty():
            print("Queue is empty.")
            return

        current = self.front
        while True:
            print(self.queue[current], end=" ")
            if current == self.rear:
                break
            current = (current + 1) % self.capacity
        print()


# 예제 사용법
queue = CircularQueue(5)

queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
queue.display()  # 출력: 1 2 3

queue.dequeue()
queue.display()  # 출력: 2 3

queue.enqueue(4)
queue.enqueue(5)
queue.enqueue(6)  # 출력: Queue is full. Cannot enqueue.

queue.display()  # 출력: 2 3 4 5

print("Front:", queue.peek())  # 출력: Front: 2
