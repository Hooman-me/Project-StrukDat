# backend/m2_antrean.py

class Queue:
    def __init__(self, cap=8):
        self.cap = cap
        self.size = 0
        self.front = 0
        self.rear = 0
        self.data = [None] * self.cap

    def enqueue(self, x):
        pass

    def dequeue(self):
        pass


class Stack:
    def __init__(self, cap=8):
        self.cap = cap
        self.size = 0
        self.data = [None] * self.cap

    def push(self, x):
        pass

    def pop(self):
        pass
