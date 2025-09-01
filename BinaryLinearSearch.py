#Pentru a incepe codul mai intai vom declara o lista cu numele A
#Folosind libraria random vom genera 10 numere cu valori intre 1 si 99
#Folosind extensia .append din list aceste 10 numere sunt inserate inapoi in lista
import random as rand
#Numim variabilul listei "Array" si il declaram *[]* gol pentru a insera valorile folosind modulul random
Array = []
amount = 10
for k in range(amount):
    Array.append(rand.randint(1, 99))

def sort_schimb(array_sort_schimb):
    for i in range(len(Array)):
        iter_min = i
        for j in range(i + 1, len(Array)):
            if Array[iter_min] > Array[j]:
                iter_min = j
        Array[i], Array[iter_min] = Array[iter_min], Array[i]
    return array_sort_schimb

print("Lista nesortata:", Array)

cap_liniar_nesortat = int(input("Alegeti numarul pe care vreti sa-l gasiti in lista folosind search liniar nesortat"))

def linear_search_nesortat(array_sort_liniar_nesortat, cap):
    i = 0
    while i < len(array_sort_liniar_nesortat):
        if array_sort_liniar_nesortat[i] == cap:
            globals()["pozitia"] = i
            return True
        i += 1

if linear_search_nesortat(Array, cap_liniar_nesortat):
    print("Gasit la pozitia", pozitia + 1)
else:
    print("Null")

array_sort = sort_schimb(Array)
print("Lista sortata", array_sort)
#Dam ca output cel mai mare numar intreg din lista Array
#Acesta sa gaseste gasind ultimu termen dat n din lista -1 "n-1" sau intr-o lista n[-1]
print("Numarul cel mai mare este: ", max(Array))

cap_liniar_sortat = int(input("Alegeti numarul pe care vreti sa-l gasiti in lista folosind search liniar sortat"))

def linear_search_sortat(array_sort_liniar_sortat, cap):
    i = 0

    while i < len(array_sort_liniar_sortat):
        if array_sort_liniar_sortat[i] == cap:
            globals()["pozitia"] = i
            return True
        i += 1

if linear_search_sortat(array_sort, cap_liniar_sortat):
    print("Gasit la pozitia", pozitia + 1)
else:
    print("Null")

cap_binar = int(input("Alegeti numarul pe care vreti sa-l gasiti in lista folosind search binar"))
def binary_search(array_sort_binar, cap_binar_local):
    lower = 0
    upper = len(array_sort_binar) - 1
    while upper >= lower:
        mid_list = (upper + lower) // 2
        if array_sort_binar[mid_list] == cap_binar_local:
            globals()["pozitia"] = mid_list
            return True

        elif array_sort_binar[mid_list] < cap_binar_local:
            lower = mid_list
        else:
            upper = mid_list

if binary_search(array_sort, cap_binar):
    print("\nNumarul a fost gasit la pozitia: ", pozitia + 1)
else:
    print("Numarul nu a fost gasit!: ")


#program End
def sortare_main():
    print("Lista sortata crescator: ")
    for cresc in range(len(Array)):
        print(Array[cresc], end=" ")
    print("\nLista sortata descrescator: ")
    rev_array = Array[::-1]
    for desc in range(len(rev_array)):
        print(rev_array[desc], end = " ")
sortare_main()