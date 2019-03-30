from __future__ import print_function
import glouton
import Algorithme
import random
import time



class Local(Algorithme.Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "local"
        self.glouton = glouton.Glouton()

    def chgmtSolution(self, data, solution, solution_allowed, rev, capacite, popIndex, targetIndex):

        popIndex.append(random.randint(0, len(solution_allowed) - 1))
        if len(popIndex) == 2:
            while popIndex[0] == popIndex[1]:
                popIndex[1] = random.randint(0, len(solution_allowed) - 1)

        targetIndex.append(random.randint(0, len(solution_allowed[popIndex[-1]]) - 1))
        cpt_target = len(solution_allowed[popIndex[-1]])
        while solution_allowed[popIndex[-1]][targetIndex[-1]] in solution:
            if len(solution_allowed[popIndex[-1]]) == 1 or cpt_target == 0:
                return rev, capacite
            else:
                targetIndex[-1] = random.randint(0, len(solution_allowed[popIndex[-1]]) - 1)
                cpt_target -=1

        rev = rev - int(data[solution[popIndex[-1]], 0])
        capacite = capacite - int(data[solution[popIndex[-1]], 1])

        del (solution[popIndex[-1]])

        solution.append(solution_allowed[popIndex[-1]][targetIndex[-1]])

        rev = rev + int(data[solution_allowed[popIndex[-1]][targetIndex[-1]], 0])
        capacite = capacite + int(data[solution_allowed[popIndex[-1]][targetIndex[-1]], 1])

        return rev, capacite

    def resolve(self, data, maxQ,  options = {"defaut": True}):

        solution, init_result = self.glouton.resolve(data, maxQ, options)

        for i in range(len(solution)):
            solution[i] -=1

        rev_init, capacite_init = self.getTotal(data, solution)

        optimum_local = False
        i = 0

        nb_de_poss = len(solution) * len(data)

        while not optimum_local:
            # on crée les solutions possibles
            solution_allowed = []
            for h in range(len(solution)):
                solution_allowed.append(list(range(0, len(data))))

            # on vide la matrice solution allowed pour trouver les optimums locaux
            while len(solution_allowed) != 0:

                i += 1
                popIndex = []
                targetIndex = []

                solution_save = solution[:]
                rev = rev_init
                capacite = capacite_init

                rand_iteration = random.choice([1,2])
                if len(solution_allowed) == 1:
                    rand_iteration = 1
                for iter in range(rand_iteration):

                    rev, capacite = self.chgmtSolution(data, solution, solution_allowed, rev, capacite, popIndex, targetIndex)

                # on test nos nouvelles capacite et solution_allowed[popIndex[iter]][targetIndex[iter]]revenus
                if capacite > maxQ or rev <= rev_init:

                    for iter in range(len(popIndex)):
                        del solution_allowed[popIndex[iter]][targetIndex[iter]]

                    if capacite >= maxQ:
                        solution = solution_save[:]

                else:
                    rev_init = rev
                    capacite_init = capacite

                popIndex.sort()
                popIndex.reverse()
                for iter in range(len(popIndex)):
                    if len(solution_allowed[popIndex[iter]]) == 0:
                        del solution_allowed[popIndex[iter]]

                if len(solution_allowed) == 0:
                    optimum_local = True

        return [x + 1 for x in sorted(solution[:])], rev_init


if __name__ == "__main__":

    algo = Local()
    algo.optionsHandler(sys.argv[2:])
