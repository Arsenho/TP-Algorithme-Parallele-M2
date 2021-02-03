import numpy as np
import csv


def matrix_generate(n, m):
    left_matrix = np.random.randint(10, size=(n, m))
    right_matrix = np.random.randint(10, size=(m, n))

    return left_matrix, right_matrix


def generate_matrix_vector(n, m):
    matrix = np.random.randint(10, size=(n, m))
    vector = np.random.randint(10, size=m)

    return matrix, vector


def gen_matrix_file(n, m):
    mat = matrix_generate(n, m)
    left_matrix = mat[0]
    right_matrix = mat[1]
    with open('matrixleftfile.csv', 'w', newline="\n") as file_1:
        matwriter = csv.writer(file_1, delimiter='\t')
        for row in left_matrix:
            matwriter.writerow(row)
    with open('matrixrightfile.csv', 'w', newline="\n") as file_2:
        matwriter = csv.writer(file_2, delimiter='\t')
        for row in right_matrix:
            matwriter.writerow(row)


def convert_string_to_int(list_of_string):
    for i in range(0, len(list_of_string)):
        list_of_string[i] = int(list_of_string[i])
    return list_of_string


def read_matrix_from_file(n, m):
    left_matrix = []
    right_matrix = []
    vector = []

    with open('matrixleftfile.csv', 'r', newline="\n") as file_1:
        data = csv.reader(file_1, delimiter='\t')
        cpt = 0
        for row in data:
            left_matrix.append(convert_string_to_int(row[:m]))
            cpt += 1
            if cpt == n:
                break
    with open('matrixrightfile.csv', 'r', newline="\n") as file_2:
        data = csv.reader(file_2, delimiter='\t')
        cpt = 0
        for row in data:
            right_matrix.append(convert_string_to_int(row[:n]))
            vector = convert_string_to_int(row[:m])
            cpt += 1
            if cpt == m:
                break
    return left_matrix, right_matrix, vector


# print(generate_matrix_vector(n=5, m=5))
# gen_matrix_file(10000, 1000)
# print(read_matrix_from_file(4, 5))
