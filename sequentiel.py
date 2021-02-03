#!/bin/python3
import sys
import getopt
import time

from matrix_generate import read_matrix_from_file


def sum_vector(first, second):
    sum_result = 0
    if len(first) != len(second):
        print("Hi")
    else:
        for i in range(0, len(first)):
            sum_result += first[i] * second[i]
        return sum_result


def matrix_tran(matrix):
    column = []
    trans_matrix = []
    for cpt in range(0, len(matrix[0])):
        for line in matrix:
            column.append(line[cpt])
        trans_matrix.append(column)
        column = []
    return trans_matrix


def product_matrix_vector(matrix, vector):
    begin = time.time()
    product_result = []
    if len(vector) is not len(matrix[0]):
        print("matrice-vecteur : Veillez vous rassurer que le nombre de ligne de la \n"
              "matrice est egale au nombre de colone du vecteur")
    else:
        for line in matrix:
            product_result.append(
                sum_vector(line, vector)
            )
        end = time.time() - begin
        return product_result, end


def product_vector_matrix(vector, matrix):
    product_result = []
    if len(vector) is not len(matrix[0]):
        print("vecteur-matrice : Veillez vous rassurer que le nombre de ligne de la \n"
              "matrice est egale au nombre de colone du vecteur")
    else:
        for line in matrix:
            product_result.append(
                sum_vector(vector, line)
            )
        return product_result


def product_matrix_matrix(matrix_left, matrix_right):
    begin = time.time()
    product_result = []
    # print(matrix_tran(matrix_right))
    # print(matrix_left[0], len(matrix_column))
    if len(matrix_left[0]) is not len(matrix_right):
        print("matrix-matrix: Veillez vous rassurer que le nombre de colonne de la \n"
              "premiere matrice est egale au nombre de ligne de la seconde matrice")
    else:
        for line in matrix_left:
            product_result.append(product_vector_matrix(line, matrix_tran(matrix_right)))
        end = time.time() - begin
        return product_result, end


def main(argv):
    row = 0
    column = 0
    try:
        opts, args = getopt.getopt(argv, "rc", ["row=", "column="])
    except getopt.GetoptError:
        sys.exit(2)
    for option, argument in opts:
        if option in ("-r", "--row"):
            row = argument
        elif option in ("-c", "--column"):
            column = argument
    matrix = read_matrix_from_file(n=int(row), m=int(column))

    left_matrix = matrix[0]
    right_matrix = matrix[1]
    vector = matrix[2]

    print(product_matrix_vector(left_matrix, vector))
    print("\n")
    print(product_matrix_matrix(left_matrix, right_matrix))


if __name__ == "__main__":
    main(sys.argv[1:])
