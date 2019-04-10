import numpy as np
import math
import os
import matplotlib.pyplot as plt
from multiprocessing import Process
import multiprocessing as mp
import time

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

        probaPrice = self.normalize(self.data["prix_par_pieces"])
        print("prix_par_pieces: " + str(probaPrice))

        for model in probaEcart:
            somme=0
            for i in range(self.data["nb_pieces"]):
                
                somme += abs(model[i] - refProbaEcart[i]) * probaPrice[i]**2

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

    def gluttonFunction(self, results):

        myLegos = np.array(self.data["nb_pieces_posses"])
        models = np.array([np.array(model) for model in self.data["pieces_par_model"]])
        nbModels = self.data["nb_models"]

        priceList = np.array(self.data["prix_par_pieces"])
        bestSolution = None
        bestPrice = float('inf')

        for j in range(25):
            currentLegos = myLegos[:]
            totalRemaining = float('inf')
            for repetition in range(50):

                np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
                selectionOrder = np.random.choice(range(nbModels), size=nbModels)

                solution = []
                currentLegos = myLegos[:]

                while len(selectionOrder) > 0:
                    for idx in selectionOrder:
                        if sum((currentLegos - models[idx, :]) < 0) < 1:
                            currentLegos = currentLegos - models[idx,:]
                            solution.append(idx)
                        else:
                            selectionOrder = np.delete(selectionOrder,
                                                       np.where(selectionOrder == idx)[0])
                            pass
                if sum(currentLegos) < totalRemaining:
                    totalRemaining = sum(currentLegos)
                    partialSolution = solution[:]
                    remainingLegos = currentLegos[:]

            currentLegos = remainingLegos[:]
            solution = partialSolution[:]

            while sum(currentLegos) > 0:
                # print(solution, sum(currentLegos))
                minCostRatio = float('inf')
                for idx in range(nbModels):
                    diff = (currentLegos[:] - models[idx,:])
                    nbReduced = np.array(diff[:])
                    nbReduced[nbReduced < 0] = 0
                    nbReduced = sum(currentLegos - nbReduced)
                    if nbReduced > 0:
                        for i in range(len(diff)):
                            if diff[i] > 0:
                                diff[i] = 0
                            else:
                                diff[i] = np.abs(diff[i])
                        additionalCost = np.dot(diff, priceList)
                        costRatio = additionalCost / nbReduced
                        if math.isnan(costRatio):
                            costRatio = float('inf')
                        if costRatio < minCostRatio:
                            new_idx = idx
                            minCostRatio = costRatio
                solution.append(new_idx)
                currentLegos = currentLegos[:] - models[new_idx, ]
                currentLegos[currentLegos < 0] = 0

            test = myLegos[:]

            for idx in solution:
                test = test - models[idx,]

            totalPrice = np.dot(abs(test), priceList)
            # nbLegos = sum(np.abs(test))
            if totalPrice < bestPrice:
                bestPrice = totalPrice
                bestSolution = solution
                print("gouton: " + str((bestSolution, bestPrice)))
        results.put([bestSolution, bestPrice])
        return (bestSolution, bestPrice)

    def heuristicFunction(self):

        overallTime = time.time()
        myLegos = np.array(self.data["nb_pieces_posses"])
        models = np.array([np.array(model) for model in self.data["pieces_par_model"]])
        nbModels = self.data["nb_models"]
        nbTypesLegos = self.data["nb_pieces"]
        priceList = np.array(self.data["prix_par_pieces"])

        pricebyModel = np.dot(models, priceList) / np.sum(models, axis=1)

        gluttonQueue = mp.Queue()
        gluttonResult = []
        processList = [Process(target = self.gluttonFunction, args=(gluttonQueue,)) for i in range(mp.cpu_count())]
        for process in processList:
            process.start()
        for process in processList:
            gluttonResult.append(gluttonQueue.get())
        for process in processList:
            process.join()
        min = float('inf')
        minIndex = 0

        for i in range(len(gluttonResult)):
            if gluttonResult[i][1] < min:
                min = gluttonResult[i][1]
                minIndex = i

        solution = gluttonResult[minIndex][0]

        replacementSize = int(len(solution) / 2)

        while time.time() - overallTime < 180:

            replacementSize = int(replacementSize * 0.80)
            startT = time.time()
            if replacementSize < 4:
                replacementSize = int(len(solution) / 2)
            print(replacementSize)
            totalLegos = np.zeros(nbTypesLegos)

            for idx in solution:
                totalLegos = totalLegos + models[idx,]
            bestPrice = np.dot((totalLegos - myLegos), priceList)

            resultsQueue = mp.Queue()
            results = []
            processList = [Process(target = self.parallLoop, args=(solution,
                                                                   replacementSize,
                                                                   bestPrice, totalLegos,
                                                                   25,
                                                                   resultsQueue)) for i in range(mp.cpu_count())]

            for i in range(mp.cpu_count()):
                processList[i].start()
            for i in range(mp.cpu_count()):
                results.append(resultsQueue.get())
            for i in range(mp.cpu_count()):
                processList[i].join()
            # print("results: " + str(results))
            for items in results:
                bestPrice_temp = items[1]
                solution_temp = items[0]
                if bestPrice > bestPrice_temp:
                    bestPrice = bestPrice_temp
                    solution = solution_temp[:]
                    print("heuristique: " + str((solution,bestPrice)))

    def parallLoop(self, solution, replacementSize, bestPrice, totalLegos, maxTime, results):

        startTime = time.time()

        myLegos = np.array(self.data["nb_pieces_posses"])
        models = np.array([np.array(model) for model in self.data["pieces_par_model"]])
        nbModels = self.data["nb_models"]
        nbTypesLegos = self.data["nb_pieces"]
        priceList = np.array(self.data["prix_par_pieces"])

        while time.time() - startTime < maxTime:
            toRemove = np.random.choice(len(solution), size=replacementSize,
                                        replace=False)

            idxToRemove = []
            for i in toRemove:
                idxToRemove.append(solution[i])

            removedLegos = np.sum(models[idxToRemove,], axis=0)

            tempLegos = totalLegos - myLegos - removedLegos

            for i in range(len(tempLegos)):
                if tempLegos[i] >= 0:
                    tempLegos[i] = 0
                else:
                    tempLegos[i] = np.abs(tempLegos[i])
            currentLegos = np.array(tempLegos[:])

            new_solution = []
            while sum(currentLegos) > 0:
                minCostRatio = float('inf')
                for idx in range(nbModels):
                    diff = (currentLegos[:] - models[idx,])
                    nbReduced = np.array(diff[:])
                    nbReduced[nbReduced < 0] = 0
                    nbReduced = sum(currentLegos - nbReduced)
                    if nbReduced > 0:
                        for i in range(len(diff)):
                            if diff[i] > 0:
                                diff[i] = 0
                            else:
                                diff[i] = np.abs(diff[i])
                        additionalCost = np.dot(diff, priceList)
                        costRatio = additionalCost / nbReduced
                        if math.isnan(costRatio):
                            costRatio = float('inf')
                        if costRatio < minCostRatio:
                            new_idx = idx
                            minCostRatio = costRatio
                new_solution.append(new_idx)
                currentLegos = currentLegos[:] - models[new_idx,]
                currentLegos[currentLegos < 0] = 0

            new_solution = np.append(new_solution, np.delete(solution, toRemove))

            newTotalLegos = np.zeros(nbTypesLegos)
            for idx in new_solution:
                newTotalLegos = newTotalLegos + models[idx,]

            newPrice = np.dot((newTotalLegos - myLegos), priceList)

            if newPrice < bestPrice:
                startT = time.time()
                bestPrice = newPrice
                solution = new_solution[:]

        results.put([solution, bestPrice])

if __name__ == "__main__":

    algo = Algo(50, 50, 1000)
    result = algo.heuristicFunction()