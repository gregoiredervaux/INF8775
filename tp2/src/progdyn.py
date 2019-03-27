from Algorithme import *
import numpy as np
import time



class Progdyn(Algorithme):

    def resolve(self, data, maxQ, options={"defaut": True}):
        dynTable = np.zeros((len(data), maxQ + 1))
        for j in range(maxQ + 1):
            if j < data[0, 1]:
                dynTable[0, j] = 0
            else:
                dynTable[0, j] = data[0, 0]
        for i in range(1, len(data)):
            for j in range(maxQ + 1):
                if j - data[i, 1] >= 0:
                    dynTable[i, j] = max(
                        (data[i, 0] + dynTable[i - 1, int(j - data[i, 1])]),
                        dynTable[(i - 1), j])
                else:
                    dynTable[i, j] = dynTable[(i - 1), j]
        i = len(data) - 1
        j = maxQ
        maxResult = dynTable[i, j]
        result = []
        while i >= 0 and dynTable[i, j] > 0:
            if sum(dynTable[:, j] == dynTable[i, j]) > 1:
                i = i - sum(dynTable[0:(i + 1), j] == dynTable[i, j]) + 1
                result.append(i + 1)
                j = int(j - data[i, 1])
                i = i - 1
            else:
                result.append(i + 1)
                j = int(j - data[i, 1])
                i = i - 1
        return sorted(result), maxResult

if __name__ == "__main__":

    algo = Progdyn()
    algo.optionsHandler(sys.argv[2:])