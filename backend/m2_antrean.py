# backend/m2_antrean.py

class Queue:
    def __init__(self, cap=8):
        self.cap = cap
        self.size = 0      # jumlah elemen di antrean
        self.front = 0     # indeks elemen terdepan (yang keluar duluan)
        self.rear = 0      # indeks slot kosong berikutnya (tempat masuk)
        self.data = [None] * self.cap

    def _grow(self):
        baru = [None] * (self.cap * 2)
        for i in range(self.size):
            baru[i] = self.data[(self.front + i) % self.cap] #copy dari front, aklo udah ujung putar ke 0
        self.data = baru
        self.cap = self.cap * 2
        self.front = 0
        self.rear = self.size

    def enqueue(self, x): #masuk
        if self.size == self.cap:
            self._grow()
        self.data[self.rear] = x #taruh di belakang
        self.rear = (self.rear + 1) % self.cap #tambah 1 dan cek dengan ujung
        self.size += 1

    def dequeue(self):  #yang depan dilayani 
        if self.size == 0: 
            return None
        x = self.data[self.front]
        self.data[self.front] = None #kosongkan yg depan
        self.front = (self.front + 1) % self.cap #pindah ke setelahnya, cek dgn ujung
        self.size -= 1
        return x

    def peek(self):
        if self.size == 0:
            return None
        return self.data[self.front]

    def is_empty(self):
        return self.size == 0


class Stack:
    def __init__(self, cap=8):
        self.cap = cap
        self.size = 0      # jumlah elemen; juga indeks slot kosong berikutnya
        self.data = [None] * self.cap

    def push(self, x):
        if self.size == self.cap:
            baru = [None] * (self.cap * 2) #buat stack 2 kali lipat
            for i in range(self.size): #pindah isi ke yg baru
                baru[i] = self.data[i]
            self.data = baru
            self.cap = self.cap * 2
        self.data[self.size] = x
        self.size += 1

    def pop(self):
        if self.size == 0: #STACK kosong
            return None
        self.size -= 1 #kurangi biar dapet ke data terakhir
        x = self.data[self.size]
        self.data[self.size] = None #ubah yg diambil jadi none
        return x

    def peek(self):
        if self.size == 0:
            return None
        return self.data[self.size - 1]

    def is_empty(self):
        return self.size == 0
