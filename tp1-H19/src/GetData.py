import sys
import counting
import quick
import quickSeuil
import quickRandomSeuil

if __name__ == '__main__':

    countingObj = counting.Counting()
    quickShortObj = quick.QuickSort()
    quickSeuilObj = quickSeuil.QuickSortSeuil()
    quickRandomSeuilObj = quickRandomSeuil.QuickSortRandomSeuil()

    path = "/home/gregoire/Documents/INF8775/TP/tp1-H19/exemplaires"
    arrayObj = [countingObj, quickShortObj, quickSeuilObj, quickRandomSeuilObj]
    for obj in arrayObj:
        print(obj.name)
        k = 10 if obj.name == "QuickSortRandomSeuil" else 1
        for i in range(k):
            obj.paralExecute([1000, 5000, 10000, 50000, 100000, 500000],
                             {"nb_core": 5,
                              "defaut": False,
                              "seuil": 10})
