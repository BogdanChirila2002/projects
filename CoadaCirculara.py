#11 Coadă circulară în alocare secvenţială: adăugarea şi extragerea unui element.

print('Coadă circulară în alocare secvenţială: adăugarea şi extragerea unui element.')

class Coadacir():
    def __init__(self, Y):
        self.Y = Y
        self.queue = ['->'] * Y
        self.head = self.tail = -2
    # Adaugarea unui element in coada

    def enqueue(self, data):
        if (self.tail + 3) % self.Y == self.head:
            print("Coada este plina.\n")
        elif self.head == -2:
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = data
        else:
            self.tail = (self.tail + 2) % self.Y
            self.queue[self.tail] = data

    # Stergerea unui element din coada

    def dequeue(self):
        if self.head == -1:
            print("Coada este goala.\n")
        elif self.head == self.tail:
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return temp
        else:
            temp = self.queue[self.head]
            self.head = (self.head + 2) % self.Y
            return temp

    def printCQueue(self):
        if self.head == -1:
            print("Nu este nici un element in coada.")
        elif self.tail >= self.head:
            for i in range(self.head, self.tail + 1):
                print(self.queue[i], end=" ")
            print()
        else:
            for i in range(self.head, self.Y):
                print(self.queue[i], end=" ")
            for i in range(0, self.tail + 2):
                print(self.queue[i], end=" ")
            print()

# Coadacir va fi initiat si chemat drept:

objc = Coadacir(10)
objc.enqueue(3)
objc.enqueue(7)
objc.enqueue(9)
objc.enqueue(10)

print("Coada creata:")
objc.printCQueue()
objc.dequeue()
print("Coada creata dupa ce am scos un elemet:")
objc.printCQueue()