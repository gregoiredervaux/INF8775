import numpy as np
import random

def getStartData(i, j, k, path='./exemplaires'):
    fichier = open('{}/LEGO_{}_{}_{}'.format(path, i, j, k))
    data = fichier.read().split('\n')
    print(data)
    pieces_par_model = data[4:]
    array_pieces_par_model = []
    for pieces in pieces_par_model:
        array_pieces_par_model.append([int(x) for x in pieces.split()])
    return {"nb_pieces": int(data[0]),
            "nb_pieces_posses": np.array([int(x) for x in data[1].split()]),
            "prix_par_pieces": np.array([int(x) for x in data[2].split()]),
            "nb_models": int(data[3]),
            "pieces_par_model": np.array(array_pieces_par_model)[:-1]}



def getPrice(model, prix):
    prixTotal = 0
    for i in range(len(model)):
        prixTotal += model[i]*prix[i]
    return prixTotal

def gloutonExploration(data):

    arrayPrix = np.array([getPrice(model, data["prix_par_pieces"]) for model in data["pieces_par_model"]])
    arrayPrixProb = arrayPrix/arrayPrix.sum()
    arrayVariance = np.array([np.var(model) for model in data["pieces_par_model"]])
    arrayMaxPieces = []
    for i in range(int(data["nb_pieces"])):
        max = 0
        for j in range(int(data['nb_models'])):
            max =  data['pieces_par_model'][j][i] if data['pieces_par_model'][j][i] > max else max
        arrayMaxPieces.append(max)
    limite_unReached = True
    solution = []
    sumValues = np.zeros(50)
    while limite_unReached:

        sumValues_save = sumValues
        solution_saved = solution
        print("sump: " + str(np.sum(np.array([x/np.sum(arrayVariance) for x in arrayVariance]))))
        index_solution = np.random.choice(list(range(0, data["nb_models"])), p= [x/np.sum(arrayVariance) for x in arrayVariance])
        print("index: " + str(index_solution))
        solution.append(index_solution)
        print("solution " + str(solution))
        print("data['nb_pieces']: " +str(data['nb_pieces']))
        print("len(sumValue): " + str(len(sumValues)))
        print("data['pieces_par_model'][index_solution]: " + str(len(data['pieces_par_model'][index_solution])))
        for i in range(data['nb_pieces']):
            sumValues[i] += data['pieces_par_model'][index_solution][i]
        print("sumValues: " + str(sumValues))
        for i in range(len(solution)):
            if sumValues[i] > data["nb_pieces_posses"][i] - arrayMaxPieces[i]:
                limite_unReached = False
                return solution_saved, sumValues_save

def exploration(data, solution, sumValues, index_added=None):

    if index_added == None:
        print(data['nb_models'])
        for i in range(data['nb_models']):
            exploration(data, solution, sumValues, i)
    else:
        solution.append(index_added)
        print(solution)
        next = False
        for i in range(data['nb_pieces']):
            sumValues[i] += data['pieces_par_model'][index_added][i]
            if sumValues[i] < data['nb_pieces_posses'][i]:
                next = True
        if next != False and max(sumValues) <= 50:
            for i in range(data['nb_models']):
                return exploration(data, solution, sumValues, i)
        #TODO: probleme recurrence



data_dict = getStartData(50,50,1000)
print(data_dict)
result_glouton = gloutonExploration(data_dict)
print("\nglouton: " + str(result_glouton))
print(exploration(data_dict, result_glouton[0], result_glouton[1]))