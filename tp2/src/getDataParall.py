import glouton
import progdyn
import local
import csv
from multiprocessing import Process

def executeHandler(obj, i, j, k):
    solution, result, time, maxQ = obj.execute(i, j, k)
    rendement = obj.getRendement(solution)
    with open("data.csv", mode='a') as csvfile:
        c = csv.writer(csvfile)
        c.writerow([obj.name, str(i), str(j), str(k), str(time), str(result), str(rendement), str(maxQ)])
        print("fait pour algo: {} taille {} serie {} exemple {} en {} ms".format(obj.name,
                                                                                    str(i),
                                                                                    str(j),
                                                                                    str(k),
                                                                                    str(time)
                                                                                    ))


if __name__ == '__main__':

    gloutonObj = glouton.Glouton()
    progdynObj = progdyn.Progdyn()
    localObj = local.Local()

    path = "/home/gregoire/Documents/INF8775/TP/tp1-H19/exemplaires"
    arrayObj = [localObj]
    with open("data.csv", mode='a') as csvfile:
        c = csv.writer(csvfile)
        c.writerow(['algorithme', 'taille', 'serie', 'exemplaire', 'temps d\'exécution', 'revenu', 'rendement', 'maxQ'])

    for obj in arrayObj:
        print(obj.name)
        tailles = [10000]
        series = [100]
        exemples = [6,7,8,9,10]
        nb_core = 5
        for i in tailles:
            for j in series:
                for k in range(exemples[0], exemples[-1], nb_core):
                    if k + nb_core - 1 < 11:
                        p_list = []
                        try:
                            for h in range(nb_core):
                                p_list.append(Process(target=executeHandler, args=(obj, i, j, k + h)))
                                p_list[-1].start()
                            for h in range(nb_core):
                                p_list[h].join()

                        except Exception as error:
                            for h in range(nb_core):
                                print("test_sequentiel " + str(h))
                                p = Process(target=executeHandler, args=(obj, i, j, k + h))
                                try:
                                    p.start()
                                    p.join()
                                except MemoryError:
                                    print("la memoire n'est toujours pas suffisante")
                    else:
                        while k < 11:
                            obj.execute(i, j, k)
                            k += 1

