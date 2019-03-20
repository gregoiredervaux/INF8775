from Algorithme import *



class Progdyn(Algorithme):

    def resolve(self, data, maxQ, options={"defaut": True}):
        dynTable = pd.DataFrame(columns=range(maxQ + 1),
                                index=range(1, len(data) + 1))
        for j in range(maxQ + 1):
            if j < data.iloc[0, 1]:
                dynTable.iloc[0, j] = 0
            else:
                dynTable.iloc[0, j] = data.iloc[0, 0]
        for i in range(1, len(data)):
            for j in range(maxQ + 1):
                if j - data.iloc[i, 1] >= 0:
                    dynTable.iloc[i, j] = max(
                        (data.iloc[i, 0] + dynTable.iloc[i - 1, int(j - data.iloc[i, 1])]),
                        dynTable.iloc[(i - 1), j])
                else:
                    dynTable.iloc[i, j] = dynTable.iloc[(i - 1), j]
        i = len(data) - 1
        j = maxQ
        maxResult = dynTable.iloc[i, j]
        result = []
        while i >= 0 and dynTable.iloc[i, j] > 0:
            if sum(dynTable.iloc[:, j] == dynTable.iloc[i, j]) > 1:
                i = i - sum(dynTable.iloc[0:(i + 1), j] == dynTable.iloc[i, j]) + 1
                result.append(i + 1)
                j = int(j - data.iloc[i, 1])
                i = i - 1
            else:
                result.append(i + 1)
                j = int(j - data.iloc[i, 1])
                i = i - 1
        return [sorted(result), maxResult]


