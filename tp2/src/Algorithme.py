import sys
import pandas as pd

class Algorithme:

    def __init__(self):
        self.default_path = "/home/gregoire/Documents/INF8775/TP/tp2/"
        self.name = "Algorithme"

    def getDataFromIndex(self, i, j, k):
        data = pd.read_csv("./exemplaires/WC-{}-{}-{}.txt".format(i, j, k),
                           sep="\n|     |    |   |  | ",
                           skiprows=1,
                           header=None)
        data.columns = ['i', 'r', 'q']
        maxQ = data.iloc[len(data) - 1, 0]
        data = data.drop(data.index[len(data) - 1])
        data.index = data['i']
        data = data.drop(['i'], axis=1)
        data.to_numpy()
        return data, maxQ

    def getDataFromPath(self, path):
        data = pd.read_csv(path,
                           sep="\n|     |    |   |  | ",
                           skiprows=1,
                           header=None)
        data.columns = ['i', 'r', 'q']
        maxQ = data.iloc[len(data) - 1, 0]
        data = data.drop(data.index[len(data) - 1])
        data = data.drop(['i'], axis=1)
        data['R'] = data['r']/data['q']
        data['p'] = data['R']/sum(data['R'])
        data = data.to_numpy()
        return data, maxQ

    def getTotal(self, data, indexs,  options = {"default": True}):
        revenus = 0
        capacite = 0
        for index in indexs:
            revenus += data[index, 0]
            capacite += data[index, 1]
        return revenus, capacite

    def resolve(self, data, maxQ,  options = {"defaut": True}):
        pass

    def optionsHandler(self, options = {"defaut": True}):
        """
        fonction prenant en compte les différentes options envoyées depuis le script shell
        :param options: l'options du script
        """

        if options == None:
            options = sys.argv[2:]

        if '-p' in options or '-t' in options:

            data , maxQ = self.getDataFromPath(sys.argv[1])

            arrayRetour = self.resolve(data, maxQ)

            if '-p' in options:  # On imprime les nombres triés

                print(arrayRetour[0])

            if '-t' in options:  # On imprime le temps d'exécution
                print(arrayRetour[1])

