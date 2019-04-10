import numpy as np

def getStartData(i, j, k, path='./exemplaires'):
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

def getMotivation(data, reference = None):

    if reference == None:
        reference = data["nb_pieces_posses"]
    probaEcart=[]
    for model in data["pieces_par_model"]:
        mean = np.mean(model)
        max = np.max(model)
        min = np.min(model)
        probaEcart.append([])
        for i in range(data["nb_pieces"]):
            probaEcart[-1].append(((model[i]-mean) + abs(min)/max))

    mean = np.mean(reference)
    max = np.max(reference)
    min = np.min(reference)
    refProbaEcart=[]
    for i in range(data["nb_pieces"]):
        refProbaEcart.append(((data["nb_pieces_posses"][i]-mean) + abs(min))/max)

    return probaEcart, refProbaEcart




def getPrice(model, prix):
    prixTotal = 0
    for i in range(len(model)):
        prixTotal += model[i]*prix[i]
    return prixTotal

def getSolutionPrice(maxValues, data):
    totalPrice=0
    maxValuesDiff = []
    for i in range(data["nb_pieces"]):
        maxValuesDiff.append(maxValues[i] - data["nb_pieces_posses"][i])
    print("maxValuesDiff: " + str(maxValuesDiff))
    return getPrice(maxValuesDiff, data["prix_par_pieces"])



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
            if sumValues[i] > data["nb_pieces_posses"][i] - arrayMaxPieces[i]:
                return solution_saved, sumValues_save
        print("sumValues: " + str(sumValues))

def exploration(data, solution, sumValues, index_added=None):
    global j
    global bestSolution
    global lenSolutionMax
    j += 1
    print("\r{}: solution: {} sumValues: {}".format(j, str(solution), str(sumValues[:10])), end="", flush=True)
    solution_added = solution[:]
    sumValues_added = sumValues[:]
    if index_added != None:
        solution_added.append(index_added)
        next = False
        for i in range(data['nb_pieces']):
            sumValues_added[i] += data['pieces_par_model'][index_added][i]
            if int(sumValues_added[i]) < int(data['nb_pieces_posses'][i]):
                next = True

    else:
        next = True

    if not next or len(solution_added) > 8:
        #print("return because => not next: " + str(not next) + " max: " + str(max(sumValues_added)))
        #print("solution_added: " + str(solution_added) + "\nsumValues: " + str(sumValues_added))
        if not next:
            print("\getSolutionPrice(sumValues_added, data): " + str(getSolutionPrice(sumValues_added, data)))
            print("getSolutionPrice(sumValues_added, data): " + str(getSolutionPrice(sumValues_added, data)))
            if (getSolutionPrice(sumValues_added, data) < getSolutionPrice(sumValues_added, data)):
                print("\nsolution: " + solution_added)
                print("price: " + str(getSolutionPrice(sumValues, data)))
                bestSolution = solution_added
        return [solution_added], [sumValues_added]


    solutions = []
    sumValuesList = []
    for i in range(data['nb_pieces']):
        new_solutions, new_sumValues = exploration(data, solution_added, sumValues_added, i)
        for solution_item in new_solutions:
            solutions.append(solution_item)

        for sumValues_item in new_sumValues:
            sumValuesList.append(sumValues_item)
    return solutions, sumValuesList



data_dict = getStartData(50,50,1000)
addDataMotivation(data_dict)
print(data_dict)
result_glouton = gloutonExploration(data_dict)
print("\nglouton: " + str(result_glouton))
bestSolution = result_glouton[0]
j=0
lenSolutionMax = 7
try:
    exploration(data_dict, result_glouton[0], result_glouton[1].tolist());
except (MemoryError):
    print("Memory error: ")