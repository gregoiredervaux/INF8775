import Algorithme

class Insertion(Algorithme.Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "Insertion"

    def sort(self, array, first, last):

        for i in range(first, last):
            key = array[i]
            j = i-1
            while j >=0 and key < array[j] :
                    array[j+1] = array[j]
                    j -= 1
            array[j+1] = key





