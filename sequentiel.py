import time


def sum_vector(first, second):
    sum_result = 0
    if len(first) != len(second):
        print("Hi")
    else:
        for i in range(0, len(first)):
            sum_result += first[i] * second[i]
        return sum_result


def product_matrix_vector(matrix, vector):
    product_result = []
    if len(vector) is not len(matrix[0]):
        print("Veillez vous rassurer que le nombre de ligne de la matrice est egale au nombre de colone du vecteur")
    else:
        for line in matrix:
            product_result.append(
                sum_vector(line, vector)
            )
        return product_result


def product_vector_matrix(vector, matrix):
    product_result = []
    if len(vector) is not len(matrix[0]):
        print("Veillez vous rassurer que le nombre de ligne de la matrice est egale au nombre de colone du vecteur")
    else:
        for line in matrix:
            product_result.append(
                sum_vector(vector, line)
            )
        return product_result


def product_matrix_matrix(matrix_left, matrix_right):
    product_result = []
    if len(matrix_left[0]) is not len(matrix_right[0]):
        print("Veillez vous rassurer que le nombre de ligne de la matrice est egale au nombre de colone du vecteur")
    else:
        for line in matrix_left:
            product_result.append(product_vector_matrix(line, matrix_right))
        return product_result
