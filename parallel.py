#!/bin/python3

from mpi4py import MPI
import numpy as np
import time
import sys
import getopt

from matrix_generate import read_matrix_from_file

from sequentiel import product_matrix_vector, product_matrix_matrix, product_vector_matrix


def get_communicator():
    comm = MPI.COMM_WORLD
    return comm


comm = get_communicator()
size = comm.Get_size()
rank = comm.Get_rank()


def fusion(matrix):
    result_vector = []
    for line in matrix:
        for value in line:
            result_vector.append(value)
    return result_vector


def fusion_matrix(global_matrix):
    result_matrix = []
    for matrix in global_matrix:
        for vector in matrix:
            result_matrix.append(vector)
    return result_matrix


def parallel_product_matrix_vector(matrix, vector):
    begin = time.time()
    # Variable qui contiendra le resultat final
    result = None

    number_of_sub_matrix_per_rank = len(matrix) // size
    matrix_ = None

    if rank == 0:
        matrix_ = np.array(matrix)
        vector_ = np.array(vector)

    # Decoupage de la matrice en ligne et
    # transmission aux differents processeurs
    recvbuf = np.empty([number_of_sub_matrix_per_rank, len(matrix[0])], dtype=int)
    comm.Scatterv(matrix_, recvbuf, root=0)

    # Allocation d'un espace mémoire pouvant contenir le vecteur sur chaque processus
    if rank != 0:
        vector_ = np.empty([len(vector)], dtype=int)

    # Diffusion du vecteur a tous les processeurs
    # Etant donné que le vecteur à diffuser est un np.array c'est-à-dire un objet
    # du module numpy alors on va utiliser la méthode Bcast(buffer, root=0) pour la diffusion
    # plutôt que bcast(obj=None, root=0).
    comm.Bcast(vector_, root=0)

    # Calcul du produit matrice-vecteur sur chaque processus
    # Bien évidemment chaque processus utilise la sous-matrice qui lui a été envoyé
    result_vector = product_matrix_vector(recvbuf, vector_)

    # Allocation mémoire pour le processus maitre qui se chargera
    # de regrouper les vecteurs resultants lovcaux
    recvbuf_ = None
    if rank == 0:
        recvbuf_ = np.empty([1, len(result_vector[0])], dtype=int)

    # Assemblage des résultats locaux des différents processus au sein du processus maitre 0
    # Ici on va plutôt utiliser la méthode gather() au lieu de Gather() puisque chaque résultat retourné par les
    # processus est de type "list" qui est un type reconnu par python nativement
    res = comm.gather(result_vector[0], root=0)

    # Fusion des vecteurs locaux pour obtenir le vecteur global
    if rank == 0:
        result = fusion(res)
    else:
        result = result_vector

    end = time.time() - begin
    return rank, result, end


def parallel_product_matrix_matrix(left_matrix, right_matrix):
    begin = time.time()
    # Variable qui contiendra le resultat final
    result = None

    size_sub_left_matrix = len(left_matrix) // size

    left_matrix_ = None
    if rank == 0:
        left_matrix_ = np.array(left_matrix)

    # Diffusion de la matrice de droite à tous les processus
    local_right_matrix = comm.bcast(right_matrix, root=0)

    # Allocation mémoire d'une matrice dont le nombre de ligne = nombre de ligne de la matrice de gauche
    # à transmettre à chaque processus et le nombre de colone = nombre de colonne de la matrice de gauche
    recvbuf = np.empty([size_sub_left_matrix, len(left_matrix[0])], dtype=int)
    #print("rank ", rank, ", matrix : ", recvbuf)

    # Decoupage de la matrice de droite en une liste de sous-matrice
    # Et partage à chaque que processus sa sous-matrice correspondante
    comm.Scatterv(left_matrix_, recvbuf, root=0)
    # print('Processeur: ', rank, ', sous-matrice de gauche: ', recvbuf)

    # Calcul du produit matrice-matrice de chaque processus sur ses données reçues
    if len(recvbuf) == 1:
        local_vector = product_vector_matrix(recvbuf[0], local_right_matrix)
    else:
        local_vector = product_matrix_matrix(recvbuf, local_right_matrix)

    global_matrix = comm.gather(local_vector[0], root=0)

    if rank == 0:
        result = fusion_matrix(global_matrix)
    else:
        result = local_vector

    end = time.time() - begin
    return rank, result, end


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

    print(parallel_product_matrix_vector(left_matrix, vector)[2])
    print("\n")
    print(parallel_product_matrix_matrix(left_matrix, right_matrix)[2])


if __name__ == "__main__":
    main(sys.argv[1:])
