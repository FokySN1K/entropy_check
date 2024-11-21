from cryptography.fernet import Fernet
from entropy import (BIN, ENCRYPT, TXT, STEP,
                             ADDING_PART, ALGO, PATH_TO_ARRAY)
import random
from ast import literal_eval


def convert_file_to_bin(directory_path, file_path):

    with open(file_path, mode='r+', encoding='utf-8') as f_src:
        with open(directory_path + BIN + TXT, mode='w+', encoding='utf-8') as f_dest:
            for char in f_src.read():
                byte = ord(char)
                f_dest.write(str(byte) + '\n')

def encrypt_file_convert_to_bin(directory_path, file_path) -> str:

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    with open(file_path, mode='r+', encoding='utf-8') as f_src:
        with open(directory_path + ENCRYPT + TXT, mode='w+', encoding='utf-8') as f_dest:
            data = bytes(f_src.read(), encoding='utf8')
            encrypted_data = cipher_suite.encrypt(data).decode('utf-8')
            f_dest.write(encrypted_data)

    convert_file_to_bin( directory_path + ENCRYPT, directory_path + ENCRYPT + TXT)

    return directory_path + ENCRYPT + TXT

def low_entropy_algorithm_convert_to_bin(directory_path, file_path):

    def binarySearch(arr, low, high, x):

        while low <= high:

            mid = low + (high - low) // 2

            # Check if x is present at mid
            if arr[mid] >= x > arr[mid - 1]:
                return mid

            # If x is greater, ignore left half
            elif arr[mid] < x:
                low = mid + 1

            # If x is smaller, ignore right half
            else:
                high = mid - 1

        # If we reach here, then the element
        # was not present
        return 0

    def f1(array):
        n = len(array)

        part_sums = [0] * n
        part_sums[0] = array[0]
        for i in range(1, n):
            part_sums[i] = array[i] + part_sums[i - 1]

        x = random.random()

        k = binarySearch(part_sums, 0, n - 1, x)

        return k

    def norm(p):
        s = sum(p)
        return [p[i] / s for i in range(len(p))]

    def next_steps(a=10, b=10):
        return (a, b)

    def add_symbols(text_in, step, adding_part, array, alph):
        i = 0
        n = len(text_in)
        m = int(n * adding_part)
        a = step
        b = int(a * adding_part)
        while (i < n):
            for j in range(a):
                if i < n:
                    g.write(text_in[i].to_bytes(1, 'big'))
                    i += 1
            for j in range(b):
                if i < n:
                    g.write(alph[f1(array)])
            (a, b) = next_steps(a, b)


    with open(PATH_TO_ARRAY, 'r') as dump:
        P = literal_eval(dump.read())

    # Alphabet
    alph = [i.to_bytes(1, 'big') for i in range(256)]

    P = norm(P)

    f = open(file_path, 'rb')
    g = open(directory_path + ALGO + TXT, 'wb')

    add_symbols(f.read(), STEP, ADDING_PART, P, alph)

    f.close()
    g.close()

    convert_file_to_bin(directory_path + ALGO, directory_path + ALGO + TXT)


if __name__ == '__main__':
    print(14//3)
