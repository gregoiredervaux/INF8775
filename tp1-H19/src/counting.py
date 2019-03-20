import sys
import time
import Algorithme

class Counting(Algorithme.Algorithme):

    def __init__(self):
        super().__init__()
        self.name = "Counting"

    def sort(self, array, options = []):

        """
            trie de l'array de int
            :param array:
            :return:
            """
        array = array[:]
        tpsStart = time.time()
        k = max(array)
        counter = [0] * (k + 1)
        for i in array:
            counter[i] += 1
        ndx = 0
        for i in range(len(counter)):
            while 0 < counter[i]:
                array[ndx] = i
                ndx += 1
                counter[i] -= 1

        temps = time.time() - tpsStart

        return array, temps


if __name__ == "__main__":

    options = sys.argv[2:]
    print("options :" + str(options))
    Counting().optionsHandler(options)




