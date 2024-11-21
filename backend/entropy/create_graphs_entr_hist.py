import matplotlib.pyplot as plt
import math
from entropy import (BIN, ENCRYPT, TXT, ALGO, ENTROPY, PNG, HISTOGRAM)


def create_graphs(DIRECTORY_PATH):

    DIRECTORY_PATH = DIRECTORY_PATH

    FILES = [
        DIRECTORY_PATH + BIN + TXT,
        DIRECTORY_PATH + ENCRYPT + BIN + TXT,
        DIRECTORY_PATH + ALGO + BIN + TXT
    ]

    ENTROPY_FILES_NAME = [
        DIRECTORY_PATH + ENTROPY + BIN + PNG,
        DIRECTORY_PATH + ENTROPY + ENCRYPT + PNG,
        DIRECTORY_PATH + ENTROPY + ALGO + PNG,
    ]

    HISTOGRAM_FILES_NAME = [
        DIRECTORY_PATH + HISTOGRAM + BIN + PNG,
        DIRECTORY_PATH + HISTOGRAM + ENCRYPT + PNG,
        DIRECTORY_PATH + HISTOGRAM + ALGO + PNG,
    ]


    '''
        Entropy func
    '''
    def entropy_for_arr(arr: list):

        # arr -> arr_chance
        arr_chance = []
        lis = dict()

        for i in range(len(arr)):
            if arr[i] in lis:
                lis[arr[i]] += 1
            else:
                lis[arr[i]] = 1

        for key, value in lis.items():
            arr_chance.append(value / len(arr))

        return entropy_for_arr_chance(arr_chance)
    def entropy_for_arr_chance(arr_chance: list):
        entropy = 0

        suma = sum(arr_chance)
        if ( (suma > 1) and (suma <= 1-1e-4) ):
            return None

        for i in arr_chance:
            entropy -= i * math.log(i, 2)

        return entropy
    def create_entropy_graph(FILES_PATH: str, FILE_NAME: str, size: int):


        arr = []

        with open(FILES_PATH, mode='r+', encoding='utf-8') as f:
            for char in f.readlines():
                try:
                    index = int(char)
                except:
                    continue

                arr.append(index)

        # print(len(arr))
        y = []
        x = []
        if (len(arr) < size):
            size = len(arr)
        for i in range(0, len(arr), size):
            entropy = entropy_for_arr(arr[i:i + size])
            if i == 0:
                y.append(entropy)
                x.append(i)

            y.append(entropy)
            x.append(i + size)

        fig = plt.figure(figsize=(20, 20))
        plt.plot(x, y, label=f"Entropy. The shift step {size}")
        plt.grid()
        plt.legend()
        # plt.show()
        plt.savefig(FILE_NAME, dpi=fig.dpi)
    def create_entropy_graphs(size = 500):

        for i in range(len(FILES)):
            create_entropy_graph(FILES[i], ENTROPY_FILES_NAME[i], size)


    '''
        Histogram func
    '''

    def create_database_for_grapf_UTF_8(FILES_PATH):

        arr_size = 0
        arr = []

        with open(FILES_PATH, mode='r+', encoding='utf-8') as f:
            for char in f.readlines():
                try:
                    index = int(char)
                    # print(char)
                except:
                    continue

                # print(chr(index))
                if index >= arr_size:
                    arr += [0] * (index - arr_size + 1)
                    arr_size = index + 1
                # print(chr(index))
                arr[index] += 1

        total_arr = []
        # иначе очень плохая картинка
        for i in range(len(arr)):
            if arr[i] != 0:
                total_arr.append([arr[i], str(chr(i))])

        return total_arr
    def create_histogram_graph(FILES_PATH: str, FILE_NAME: str):

        database = create_database_for_grapf_UTF_8(FILES_PATH)


        total_sum = sum([i[0] for i in database])
        y = [i[0] / total_sum for i in database]
        x = [str(i[1]) for i in database]

        entropy = entropy_for_arr_chance(y)

        y = [i * 100 for i in y]
        fig = plt.figure(figsize=(20, 20))
        plt.bar(x, y,
                label=f'Количество символов: {total_sum}. Entropy: {entropy}')  # Параметр label позволяет задать название величины для легенды
        plt.xlabel('Символ')
        plt.ylabel('Появление символа в процентах')
        plt.title('Гистограмма')
        plt.legend()
        plt.grid(color='blue', linestyle='--', linewidth=0.1)
        # plt.show()
        plt.savefig(FILE_NAME, dpi=fig.dpi)
    def create_histogram_graphs():

        for i in range(len(FILES)):
            create_histogram_graph(FILES[i], HISTOGRAM_FILES_NAME[i])


    create_entropy_graphs()
    create_histogram_graphs()