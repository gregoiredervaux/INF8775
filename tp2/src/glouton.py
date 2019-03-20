from Algorithme import *
import numpy as np


class Glouton(Algorithme):

    def resolve(self, data, maxQ, options = {"defaut": True}):
        data['R'] = data['r'] / data['q']
        data['p'] = data['R'] / sum(data['R'])

        best_locations = None
        best_result = 0
        for i in range(10):
            selectionOrder = np.random.choice(range(1, len(data) + 1),
                                              size=len(data),
                                              p=data['p'],
                                              replace=False)
            solution = []
            currentSpace = maxQ
            counter = -1
            while currentSpace > 0:
                counter += 1
                if data['q'][selectionOrder[counter]] <= currentSpace:
                    currentSpace -= data['q'][selectionOrder[counter]]
                    solution.append(selectionOrder[counter])
                    result = sum(data['r'][solution])
            if result > best_result:
                best_locations = solution[:]
                best_result = sum(data['r'][solution])

        return best_locations, best_result