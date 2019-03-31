from __future__ import print_function
import glouton
import Algorithme
import random
import sys
import numpy as np



class Local(Algorithme.Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "local"
        self.glouton = glouton.Glouton()

    def resolve(self, data, maxQ,  options = {"defaut": True}):

        best_locations = self.glouton.resolve(data, maxQ)[0]
        best_solution = [x - 1 for x in best_locations]
        R = data[:, 0] / data[:, 1]

        def recurrence(best_solution):

            minDensity = float('inf')
            for idx1 in best_solution:
                if R[idx1] < minDensity:
                    minDensity = R[idx1]
                    toRemove = idx1

            partial_solution = best_solution[:]
            partial_solution.remove(toRemove)
            spaceLeft = maxQ - sum(data[partial_solution, 1])
            removedValue = data[toRemove, 0]

            # toTest = list(range(len(data)))
            toTest = np.where(R > minDensity)[0]

            idx_toRemove = []

            for x in partial_solution:
                idx_toRemove = np.append(idx_toRemove, np.where(toTest == x)[0])

            toTest = np.delete(toTest, idx_toRemove)
            toTestOrder = [x for _, x in sorted(zip(-R[toTest], toTest))]

            new_idx = []
            i = 0
            tracking = []

            while spaceLeft > 0 and i < len(toTest) - 1:
                idx2 = toTestOrder[i]
                if data[idx2, 1] <= spaceLeft:
                    new_idx.append(idx2)
                    spaceLeft -= data[idx2, 1]
                    i += 1
                    tracking.append(i)

                    if spaceLeft == 0 or i >= len(toTest) - 1:
                        if np.sum(data[new_idx, 0]) < removedValue:
                            new_idx = []
                            spaceLeft = maxQ - sum(data[partial_solution, 1])
                            i = tracking[0] + 1
                            tracking = []
                else:
                    i += 1

            if len(new_idx) == 0:
                new_solution = partial_solution[:]

            else:
                new_solution = sorted(np.append(partial_solution[:], new_idx))

            if sum(data[new_solution, 0]) <= sum(data[best_solution, 0]):

                return best_solution
            else:

                best_solution = new_solution[:]
                return recurrence(best_solution)

        best_solution = recurrence(best_solution)

        return [[x + 1 for x in best_solution], sum(data[best_solution, 0])]


if __name__ == "__main__":

    algo = Local()
    algo.optionsHandler(sys.argv[2:])