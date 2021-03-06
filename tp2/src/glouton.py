import Algorithme
import numpy as np
import sys


class Glouton(Algorithme.Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "glouton"

    def resolve(self, data, maxQ, options = {"defaut": True}):

        R = data[:, 0] / data[:, 1]
        probVector = R / np.sum(R)
        best_locations = None
        best_result = 0
        for i in range(10):
            selectionOrder = np.random.choice(range(len(data)),
                                              size=len(data),
                                              p=probVector,
                                              replace=False)
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