import csv
import sys
import quick
import quickSeuil
import quickRandomSeuil

if __name__ == '__main__':

    quick = quick.QuickSort()
    quickSeuilObj = quickSeuil.QuickSortSeuil()
    quickRandomSeuilObj = quickRandomSeuil.QuickSortRandomSeuil()

    path = "/home/gregoire/Documents/INF8775/TP/tp1-H19/exemplaires"
    arrayObj = [quickSeuilObj, quickRandomSeuilObj]

    with open("data.csv", mode='a') as csvfile:
        c = csv.writer(csvfile)
        c.writerow(['algorithme', 'exemplaire', 'taille du tableau', 'seuil', 'temps d\'exécution'])
        csvfile.close()

    for obj in arrayObj:
        print(obj.name)
        for k in [1, 2, 5, 10, 100, 1000]:
            obj.paralExecute([500000],
                             {"nb_core": 5,
                              "defaut": False,
                              "seuil": k,
                              "first_ite": 20,
                              "last_ite": 29})
            print("fait pour seuil = " + str(k))
