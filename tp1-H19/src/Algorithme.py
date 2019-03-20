import sys
import csv
from multiprocessing import Process


class Algorithme:
    """
    classe mère de tous les algorithmes
    """

    def __init__(self):
        self.name = "Algo_defaut"
        self.racine_exe_files = "/home/gregoire/Documents/INF8775/TP/tp1-H19/exemplaires"

    def sort(self, array):
        pass

    def InsertionSort(self, array, first, last):

        for i in range(first, last):
            key = array[i]
            j = i-1
            while j >=0 and key < array[j] :
                    array[j+1] = array[j]
                    j -= 1
            array[j+1] = key

    def printArray(self, array):
        """
        affichage d'un array comme demandé dans l'énonce
        :param array: array a afficher
        :return: void
        """
        string = ""
        for i in range(len(array)):
            string = string + str(array[i]) + ' '
        print(string)

    def dataToArray(self, array):
        """
        transformation d'un array de string en un array d'int
        :param array: array a transformer
        :return: array de int
        """
        for i in range(len(array)):
            array[i] = int(array[i])
        return array

    def sortFile(self, i, j, options = {}, path=None if len(sys.argv) != 2 else sys.argv[1]):
        """
        selectionne un fichier avec i et j et le trie selon l'algo de l'instance, puis sauvegarde
        :param i: nombre d'élement dans le fichier
        :param j: série
        :param path: le chemin, par défaut celui de la classe mère
        """
        if path == None:
            path = self.racine_exe_files
        with open("data.csv", mode='a') as csvfile:
            c = csv.writer(csvfile)
            fichier = open('{}/testset_{}_{}.txt'.format(path, j, i))
            data = fichier.readlines()
            fichier.close()
            try:
                c.writerow([self.name, str(i), str(j), "" if "seuil" not in options else options["seuil"], str(self.sort(self.dataToArray(data), options)[1])])
                print("\rfait pour: " + 'testset_{}_{}.txt'.format(j, i))
            except MemoryError:
                print("La memoire n'est pas suffisante")
                raise Exception("")

            csvfile.close()


    def execute(self, array, options = {"default": True}):

        """
        execute l'algoritme sur en ensemble de fichier
        :param array: l'array des fichers à trier : [1000, 5000, 10 000, ... ]
        """
        print("depuis " + str(array[0]) + " jusqu'a " + str(array[len(array) - 1]))
        with open("data.csv", mode='a') as csvfile:
            c = csv.writer(csvfile)
            c.writerow(['algorithme', 'exemplaire', 'taille du tableau', 'seuil', 'temps d\'exécution'])

        for j in array:
            for i in range(30):
                self.sortFile(i, j, options)


    def paralExecute(self, array, options = {"nb_core": 4,
                                             "default": True}):
        """
        execute l'algoritme sur l'ensemble des données
        :param array: l'array des fichers à trier : [1000, 5000, 10 000, ... ]
        :param options: options d'exécution
        :return:
        """
        print("depuis " + str(array[0]) + " jusqu'a " + str(array[len(array) - 1]))

        for j in array:
            for i in range(0 if "first_ite" not in options else options["first_ite"],
                        29 if "last_ite" not in options else options["last_ite"],
                        options["nb_core"]):

                if i + options["nb_core"] < 30:
                    p_list = []
                    # on essai la version parallele
                    try:
                        for k in range(options["nb_core"]):
                            p_list.append(Process(target=self.sortFile, args=(i + k, j, options)))
                            p_list[k].start()

                        for k in range(options["nb_core"]):
                            p_list[k].join()
                    except Exception as error:
                        # on essai la version sequentielle
                        for k in range(options["nb_core"]):
                            print("test sequentiel: " + str(k))
                            p_list.append(Process(target=self.sortFile, args=(i + k, j, options)))
                            try:
                                p_list[k].start()
                                p_list[k].join()
                                print("done pour " + str(k))
                            except MemoryError:
                                print("la memoire n'est toujours pas suffisante")

                else:
                    while i < 30:
                        self.sortFile(i, j)
                        i += 1

    def optionsHandler(self, options=None):

        """
        fonction prenant en compte les différentes options envoyées depuis le script shell
        :param options: l'options du script
        """

        if options == None:
            options = sys.argv[2:]

        if '-p' in options or '-t' in options:
            fichier = open(sys.argv[1], "r")
            data = fichier.readlines()
            fichier.close()
            arrayRetour = self.sort(self.dataToArray(data))

            if '-p' in options:  # On imprime les nombres triés

                self.printArray(arrayRetour[0])

            if '-t' in options:  # On imprime le temps d'exécution
                print(arrayRetour[1])

        if '--all' in options:
            print("on execute : " + self.name)
            self.paralExecute([1000, 5000, 10000, 50000, 100000, 500000])
