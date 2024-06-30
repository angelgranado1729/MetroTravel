from EDD.Node import Node


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, value):
        new_node = Node(value)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.value

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.front.value

    def __str__(self):
        if self.is_empty():
            return "Queue is empty"
        current = self.front
        result = ""
        while current:
            result += str(current.value) + " "
            current = current.next
        return result

    def len(self):
        if self.is_empty():
            return 0
        current = self.front
        count = 0
        while current:
            count += 1
            current = current.next
        return count
