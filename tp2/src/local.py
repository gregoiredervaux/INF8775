from __future__ import print_function
import glouton
from Algorithme import *
import random
import time



class Local(Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "local"
        self.glouton = glouton.Glouton()

    def chgmtSolution(self, data, solution, solution_allowed, rev, capacite, popIndex, targetIndex):

        popIndex.append(random.randint(0, len(solution_allowed) - 1))
        if len(popIndex) == 2:
            while popIndex[0] == popIndex[1]:
                popIndex[1] = random.randint(0, len(solution_allowed) - 1)
        print("\npopIndex: " + str(popIndex[-1]))

        print("rev: " + str(rev))
        print("capa: " + str(capacite))
        rev = rev - int(data[popIndex[-1], 0])
        capacite = capacite - int(data[popIndex[-1], 1])
        print("rev del: " + str(rev))
        print("capa del: " + str(capacite))

        print("init_solution avant " + str(solution))
        del (solution[popIndex[-1]])
        print("init_solution apres " + str(solution))


        targetIndex.append(random.randint(0, len(solution_allowed[popIndex[-1]]) - 1))

        print("targetIndex " + str(targetIndex[-1]))

        solution.append(targetIndex[-1])
        print("init_solution " + str(solution))

        rev = rev + int(data[targetIndex[-1], 0])
        capacite = capacite + int(data[targetIndex[-1], 1])
        print("rev apres " + str(rev))
        print("capacite apres " + str(capacite))

        return rev, capacite

    def resolve(self, data, maxQ,  options = {"defaut": True}):

        solution, init_result = self.glouton.resolve(data, maxQ, options)

        rev_init, capacite_init = self.getTotal(data, solution)

        print("rev_init: " + str(rev_init) + " capacite: " + str(capacite_init) + " capaMax: " + str(maxQ))
        print("solution: " + str(solution))


        optimum_local = False
        i = 0

        while not optimum_local:
            # on crée les solutions possibles
            solution_allowed = []
            for h in range(len(solution)):
                solution_allowed.append(list(range(1, len(data))))

            print("solution_allowed_init: " + str(solution_allowed))

            # on vide la matrice solution allowed pour trouver les optimums locaux
            while len(solution_allowed) != 0:

                i += 1
                init_loop = time.time()
                print("nb de tours: {} solution: {} revenue: {} time loop {}".format(str(i),
                                                                                            str(solution),
                                                                                            str(rev_init),
                                                                                            str((time.time() - init_loop))),
                      end="", flush=False)

                popIndex = []
                targetIndex = []

                solution_save = solution[:]
                rev = rev_init
                capacite = capacite_init

                rand_iteration = random.choice([1,2])
                if len(solution_allowed) == 1:
                    rand_iteration = 1
                print("rand_iteration " + str(rand_iteration))
                for iter in range(rand_iteration):

                    rev, capacite = self.chgmtSolution(data, solution, solution_allowed, rev, capacite, popIndex, targetIndex)

                print("")
                # on test nos nouvelles capacite et solution_allowed[popIndex[iter]][targetIndex[iter]]revenus
                if capacite > maxQ or rev <= rev_init:

                    for iter in range(len(popIndex)):
                        del solution_allowed[popIndex[iter]][targetIndex[iter]]

                    if capacite >= maxQ:
                        solution = solution_save[:]

                else:
                    print("\nNouvelle solution trouvée: " + str(solution) +
                          " revenu: " + str(rev) +
                          " pour la capacité de : " + str(capacite))
                    rev_init = rev
                    capacite_init = capacite

                popIndex.sort()
                popIndex.reverse()
                for iter in range(len(popIndex)):
                    if len(solution_allowed[popIndex[iter]]) == 0:
                        print("deletion d'une dimention: " + str(popIndex[iter]))
                        del solution_allowed[popIndex[iter]]

                if len(solution_allowed) == 0:
                    optimum_local = True
                    print("optimum local: ")
                    print("solution: {} revenue: {} capacite: {}".format(str(solution),str(rev_init),str(capacite)))

if __name__ == "__main__":

    options = sys.argv[2:]
    print("options :" + str(options))
    local = Local()
    data = local.getDataFromPath(
        "/home/gregoire/Documents/INF8775/TP/tp2/exemplaires/WC-100-10-01.txt")
    print(data)
    while True:
        local.resolve(data[0], data[1])
    #local.optionsHandler(options)
