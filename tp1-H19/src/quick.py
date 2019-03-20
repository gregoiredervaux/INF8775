import sys
import time
import Algorithme


class QuickSort(Algorithme.Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "QuickShort"

    def sort(self, alist, options = {"default": True}):
        alist=alist[:]
        tpsStart = time.time()
        self.quickSortHelper(alist, 0, len(alist)-1)
        temps = time.time() - tpsStart
        return alist, temps

    def quickSortHelper(self, alist,first,last):
        if first<last:
            splitpoint = self.partition(alist,first,last)

            self.quickSortHelper(alist,first,splitpoint-1)
            self.quickSortHelper(alist,splitpoint+1,last)

    def partition(self, alist,first,last):
        pivotvalue = alist[first]

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
    QuickSort().optionsHandler(options)
