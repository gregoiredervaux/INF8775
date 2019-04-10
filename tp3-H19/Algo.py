import numpy as np
import matplotlib.pyplot as plt

class Algo:

    def __init__(self, i, j, k):
        self.data = self.getStartData(i, j, k)

    def getStartData(self, i, j, k, path='./exemplaires'):
        fichier = open('{}/LEGO_{}_{}_{}'.format(path, i, j, k))
        data = fichier.read().split('\n')
        pieces_par_model = data[4:]
        array_pieces_par_model = []
        for pieces in pieces_par_model:
            array_pieces_par_model.append([int(x) for x in pieces.split()])
        return {"nb_pieces": int(data[0]),
                "nb_pieces_posses": np.array([int(x) for x in data[1].split()]),
                "prix_par_pieces": np.array([int(x) for x in data[2].split()]),
                "nb_models": int(data[3]),
                "pieces_par_model": np.array(array_pieces_par_model)[:-1]}

    def normalize(self, list):
        max = np.max(list)
        min = np.min(list)
        return [(list[i] - min) / (max - min) for i in range(len(list))]

    def getMotivationEcart(self, reference):

        sumEcart = []

        probaEcart = []
        refProbaEcart = self.normalize(reference)
        for model in self.data["pieces_par_model"]:
            probaEcart.append(self.normalize(model))

        print("\nrefProbaEcart avant: " + str(refProbaEcart))
        for i in range(self.data["nb_pieces"]):
            if reference[i] < 0:
                refProbaEcart[i] = 0
                for model in probaEcart:
                    model[i] = 0

        print("refProbaEcart apres: " + str(refProbaEcart))
        probaPrice = self.normalize(self.data["prix_par_pieces"])
        print("prix_par_pieces: " + str(probaPrice))

        for model in probaEcart:
            somme=0
            for i in range(self.data["nb_pieces"]):
                somme += abs(model[i] - refProbaEcart[i]) * probaPrice[i]
            sumEcart.append(somme)
        print("sumEcart: " + str(sumEcart))
        return sumEcart

    def getMotivationPrice(self, reference):

        probaEcart = []
        refProbaEcart = self.normalize(reference)
        for model in self.data["pieces_par_model"]:
            probaEcart.append(self.normalize(model))

        probaPrice = self.normalize(self.data["prix_par_pieces"])

        mergeProba = []
        for i in range(self.data["nb_models"]):
            mergeProba.append(
                self.normalize([probaEcart[i][j] * probaPrice[j] for j in range(self.data["nb_pieces"])]))

        return mergeProba

    def getModelPrice(self, model, prix):
        prixTotal = 0
        for i in range(len(model)):
            prixTotal += model[i] * prix[i]
        return prixTotal

    def getSolutionPrice(self, sumValues):
        totalPrice = 0
        maxValuesDiff = []
        for i in range(self.data["nb_pieces"]):
            maxValuesDiff.append(sumValues[i] - self.data["nb_pieces_posses"][i])
        return self.getModelPrice(maxValuesDiff, self.data["prix_par_pieces"])

    def gloutonFull(self):

        solution = []
        sumValues = np.zeros(self.data["nb_pieces"]).tolist()
        limite_unreached = True
        while limite_unreached:
            sumValues_save = sumValues
            solution_saved = solution
            sumEcart = self.getMotivationEcart(self.data["nb_pieces_posses"] - sumValues)
            minSumEcart = np.min(sumEcart)
            for i in range(self.data["nb_models"]):
                if sumEcart[i] == minSumEcart:
                    index_solution = i
            self.showModel(self.data["pieces_par_model"][index_solution], self.data["nb_pieces_posses"] - sumValues)
            solution.append(index_solution)
            print("solution: " + str(solution))
            limite_unreached = False
            for i in range(self.data['nb_pieces']):
                sumValues[i] += self.data['pieces_par_model'][index_solution][i]
                if sumValues[i] < self.data["nb_pieces_posses"][i]:
                    limite_unreached = True
        return solution, sumValues

    def showModel(self, model, reference):

        ind = np.arange(self.data["nb_pieces"])
        referenceDiff = [(reference[i] - model[i]) for i in range(self.data["nb_pieces"])]
        referenceDiffPoss = [reference[i] if reference[i] > 0 else 0 for i in range(self.data["nb_pieces"])]
        referenceDiffNeg = [reference[i] if reference[i] < 0 else 0 for i in range(self.data["nb_pieces"])]
        width = 0.9
        p1 = plt.bar(ind, referenceDiffNeg, width)
        p2 = plt.bar(ind, model, width, bottom=referenceDiffNeg)
        p3 = plt.bar(ind, referenceDiffPoss, width, bottom=model)


        plt.ylabel("values")
        plt.xlabel("pieces")

        plt.legend((p2[0], p1[0], p3[0]), ("model", "referenceNegative", "referencePossitive"))

        plt.show()

    def showSolution(self, solution):
        pass


if __name__ == "__main__":

    algo = Algo(1, 1, 1)
    result = algo.gloutonFull()
    print("solution: " + str(result[0]))
    print("sumValues: " + str(result[1]))
    print("diff: " + str([result[1][i] - algo.data["nb_pieces_posses"][i] for i in range(algo.data["nb_pieces"])]))
    print(algo.getSolutionPrice(result[1]))