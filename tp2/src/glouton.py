from Algorithme import *
import numpy as np


class Glouton(Algorithme):

    def resolve(self, data, maxQ, options = {"defaut": True}):

        best_locations = None
        best_result = 0
        for i in range(10):
            selectionOrder = np.random.choice(range(len(data)), size=len(data),
                                              p=data[:, 3], replace=False)
            solution = []
            currentSpace = maxQ
            counter = -1
            while currentSpace > 0 and counter < len(data) - 1:
                counter += 1
                if data[selectionOrder[counter], 1] <= currentSpace:
                    currentSpace -= data[selectionOrder[counter], 1]
                    solution.append(selectionOrder[counter])
                    result = sum(data[solution, 0])
            if result > best_result:
                best_locations = [x + 1 for x in sorted(solution[:])]
                best_result = sum(data[solution, 0])
        return best_locations, best_result

if __name__ == "__main__":

    algo = Glouton()
    algo.optionsHandler(sys.argv[2:])