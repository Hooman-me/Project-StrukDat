# backend/m2_antrean.py

class Queue:
    def __init__(self, cap=8):
        self.cap = cap
        self.size = 0      # jumlah elemen di antrean
        self.front = 0     # indeks elemen terdepan (yang keluar duluan)
        self.rear = 0      # indeks slot kosong berikutnya (tempat masuk)
        self.data = [None] * self.cap

    def _grow(self):
        """Gandakan kapasitas; salin isi berurutan mulai dari front."""
        baru = [None] * (self.cap * 2)
        for i in range(self.size):
            baru[i] = self.data[(self.front + i) % self.cap]
        self.data = baru
        self.cap = self.cap * 2
        self.front = 0
        self.rear = self.size

    def enqueue(self, x):
        if self.size == self.cap:
            self._grow()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.cap
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            return None
        x = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.cap
        self.size -= 1
        return x

    def peek(self):
        """Lihat elemen terdepan tanpa mengeluarkannya."""
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
            baru = [None] * (self.cap * 2)
            for i in range(self.size):
                baru[i] = self.data[i]
            self.data = baru
            self.cap = self.cap * 2
        self.data[self.size] = x
        self.size += 1

    def pop(self):
        if self.size == 0:
            return None
        self.size -= 1
        x = self.data[self.size]
        self.data[self.size] = None
        return x

    def peek(self):
        """Lihat elemen teratas tanpa mengeluarkannya."""
        if self.size == 0:
            return None
        return self.data[self.size - 1]

    def is_empty(self):
        return self.size == 0
