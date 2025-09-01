import random as rd


class ArboreBinar:
    def __init__(self, data):
        self.data = data
        self.leftchild = None
        self.rightchild = None


nod1 = ArboreBinar(rd.randint(60, 99))
nod2 = ArboreBinar(rd.randint(50, 60))
nod3 = ArboreBinar(rd.randint(70, 99))
nod4 = ArboreBinar(rd.randint(0, 20))
nod5 = ArboreBinar(rd.randint(20, 70))
nod6 = ArboreBinar(rd.randint(30, 70))
nod7 = ArboreBinar(rd.randint(10, 30))

print("Radacina arborelui este: ")
print(nod1.data)

nod1.leftchild = nod2
nod1.rightchild = nod3
nod2.leftchild = nod4
nod2.rightchild = nod5
nod3.leftchild = nod6
nod3.rightchild = nod7

print(nod1.data)
print(nod1.leftchild.data)
print(nod1.rightchild.data)
print(nod2.rightchild.data)
print(nod2.leftchild.data)
print(nod3.leftchild.data)
print(nod3.rightchild.data)
