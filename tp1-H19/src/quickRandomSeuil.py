import random
import sys
import time
import Algorithme

class QuickSortRandomSeuil(Algorithme.Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "QuickSortRandomSeuil"

    def sort(self, A, options = {"default": True}):
        A = A[:]
        tpsStart = time.time()
        self.quickSort(A, 0, len(A) - 1, 4 if "seuil" not in options else options["seuil"])
        temps = time.time() - tpsStart
        return A, temps

    def quickSort(self, A, start, end, seuil):

        if end - start <= seuil and start < end:
            self.InsertionSort(A, start, end+1)
        elif start < end:
            p = self.partition(A, start, end)
            self.quickSort(A, start, p - 1, seuil)
            self.quickSort(A, p + 1, end, seuil)


    def partition(self, alist,first,last):
        pivotvalue = alist[random.randint(first, last)]

        leftmark = first+1
        rightmark = last

        done = False
        while not done:

            while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
                leftmark = leftmark + 1

            while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
                rightmark = rightmark -1

            if rightmark < leftmark:
                done = True
            else:
                temp = alist[leftmark]
                alist[leftmark] = alist[rightmark]
                alist[rightmark] = temp

        temp = alist[first]
        alist[first] = alist[rightmark]
        alist[rightmark] = temp

        return rightmark


if __name__ == "__main__":
    options = sys.argv[2:]
    print("options :" + str(options))
    QuickSortRandomSeuil().optionsHandler(options)
