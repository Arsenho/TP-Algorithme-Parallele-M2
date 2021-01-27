from mpi4py import MPI
import numpy as np
import time

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

    number_of_sub_matrix_per_rank = len(matrix) // size
    matrix_ = None

    if rank == 0:
        matrix_ = np.array(matrix)
        vector_ = np.array(vector)

    # Decoupage de la matrice en ligne et
    # transmission aux differents processeurs
    recvbuf = np.empty([number_of_sub_matrix_per_rank, len(matrix[0])], dtype=int)
    comm.Scatterv(matrix_, recvbuf, root=0)

    # Affichage de chaque processus et sa liste de sous-vecteurs reçu
    # print('Processeur: ', rank, ', Sous_Vecteur: ', recvbuf)
    # print('\n')

    # Allocation d'un espace mémoire pouvant contenir le vecteur sur chaque processus
    if rank != 0:
        vector_ = np.empty([len(vector)], dtype=int)

    # Diffusion du vecteur a tous les processeurs
    # Etant donné que le vecteur à diffuser est un np.array c'est-à-dire un objet
    # du module numpy alors on va utiliser la méthode Bcast(buffer, root=0) pour la diffusion
    # plutôt que bcast(obj=None, root=0).
    comm.Bcast(vector_, root=0)

    # Affichage du vecteur diffusé par chaque processus
    # print('Processeur: ', rank, ', Vecteur: ', vector_)

    # Calcul du produit matrice-vecteur sur chaque processus
    # Bien évidemment chaque processus utilise la sous-matrice qui lui a été envoyé
    result_vector = product_matrix_vector(recvbuf, vector_)

    # Affichage du résultat local par chaque processus
    # print('Processeur: ', rank, ', result: ', result_vector)

    # Allocation mémoire pour le processus maitre qui se chargera
    # de regrouper les vecteurs resultants lovcaux
    recvbuf_ = None
    if rank == 0:
        recvbuf_ = np.empty([1, len(result_vector)], dtype=int)

    # Assemblage des résultats locaux des différents processus au sein du processus maitre 0
    # Ici on va plutôt utiliser la méthode gather() au lieu de Gather() puisque chaque résultat retourné par les
    # processus est de type "list" qui est un type reconnu par python nativement
    res = comm.gather(result_vector, root=0)

    # Fusion des vecteurs locaux pour obtenir le vecteur global
    if rank == 0:
        print('Processeur: ', rank, ', Result global : ', fusion(res))
    end = time.time() - begin
    print("rank ", rank, ", temps d'execution du resulat final: ", end)


def parallel_product_matrix_matrix(left_matrix, right_matrix):
    begin = time.time()
    
    size_sub_right_matrix = len(right_matrix) // size
    size_sub_left_matrix = len(left_matrix) // size

    right_matrix_ = None
    left_matrix_ = None
    if rank == 0:
        left_matrix_ = np.array(left_matrix)
        right_matrix_ = np.array(right_matrix)

    # Diffusion de la matrice de droite à tous les processus
    local_right_matrix = None
    local_right_matrix = comm.bcast(right_matrix, root=0)
    # print('Processeur: ', rank, ', Matrice droite: ', local_right_matrix)

    local_matrix = None
    # print("Matrice de taille : ( ", size_sub_left_matrix, ", ", len(left_matrix[0]), " ) à transmettre à chaque processus")
    # Allocation mémoire d'une matrice dont le nombre de ligne = nombre de ligne de la matrice de gauche
    # à transmettre à chaque processus et le nombre de colone = nombre de colonne de la matrice de gauche
    recvbuf = np.empty([size_sub_left_matrix, len(left_matrix[0])], dtype=int)

    # Decoupage de la matrice de droite en une liste de sous-matrice
    # Et partage à chaque que processus sa sous-matrice correspondante
    comm.Scatterv(left_matrix_, recvbuf, root=0)
    # print('Processeur: ', rank, ', sous-matrice de gauche: ', recvbuf)

    # Calcul du produit matrice-matrice de chaque processus sur ses données reçues
    if len(recvbuf) == 1:
        local_vector = product_vector_matrix(recvbuf[0], local_right_matrix)
    else:
        local_vector = product_matrix_matrix(recvbuf, local_right_matrix)
    # print("rank ", rank, "Local Resultat: ", local_vector)
    # end = time.time() - begin
    # print("rank ", rank, ", temps d'execution après les calculs locaux: ", end)

    global_matrix = comm.gather(local_vector, root=0)
    # end = time.time() - begin
    # print("rank ", rank, ", temps d'execution après assemblabe des resultats locaux: ", end)
    if rank == 0:
        # print("rank ", rank, "Resultat: ", global_matrix)
        print("Resultat du produit est: ", fusion_matrix(global_matrix))
    end = time.time() - begin
    print("rank ", rank, ", temps d'execution du resulat final: ", end)


# parallel_product_matrix_vector([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]], [13, 14])
parallel_product_matrix_matrix([[1, 2], [3, 4], [1, 2], [3, 4]], [[1, 0], [0, 1], [1, 0], [0, 1]])
