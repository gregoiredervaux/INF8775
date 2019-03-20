import glouton
from Algorithme import *
import random


class Local(Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "local"
        self.glouton = glouton.Glouton()

    def resolve(self, data, maxQ, options={"defaut": True}):

        init_solution, init_result = self.glouton.resolve(data, maxQ, options)

        rev_init, capacite_init = self.getTotal(data, init_solution)

        optimum_local = False

        while not optimum_local:
            testedAll = False
            solution_allowed = data[:]
            rev = 0
            while rev_init > rev and len(solution_allowed) !=0:

                # on retire deux morceau au hazard dans le liste des solutions
                pop1 = random.randint(0, len(init_solution) - 1)
                pop2 = random.randint(0, len(init_solution) - 1)

                save_pop1 = init_solution[pop1]
                save_pop2 = init_solution[pop2]

                del (init_solution[pop1])
                del (init_solution[min(pop2, len(init_solution) - 1)])

                # on ajoute deux nouvelles solutions
                target1 = random.randint(0, len(solution_allowed) - 1)
                target2 = random.randint(0, len(solution_allowed) - 1)

                init_solution.append(target1)
                init_solution.append(target2)

                rev, capacite = self.getTotal(data, init_solution)

                # on test nos nouvelles capacite et revenus
                if capacite > maxQ or rev <= rev_init:

                    init_solution.pop()
                    init_solution.pop()

                    init_solution.append(save_pop1)
                    init_solution.append(save_pop2)

                    solution_allowed.drop(target1, 0)
                    solution_allowed.drop(target2, 0)

                if len(solution_allowed) == 0:
                    optimum_local = True

        return init_solution, self.getTotal(init_solution)[0]


if __name__ == "__main__":

    options = sys.argv[2:]
    print("options :" + str(options))
    local = Local()
    data = local.getDataFromPath(
        "/home/gregoire/Documents/INF8775/TP/tp2/exemplaires/WC-100-10-01.txt")
    local.resolve(data[0], data[1])
    #local.optionsHandler(options)
