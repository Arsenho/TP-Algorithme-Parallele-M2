from mpi4py import MPI
import numpy as np
import time

from sequentiel import product_matrix_vector


def get_communicator():
    comm = MPI.COMM_WORLD
    return comm


def point_to_point_comm(matrix, communicator):
    comm = communicator
    rank = comm.Get_rank()
    print('My rank is', rank)

    if rank == 0:
        comm.send(matrix[2:], dest=1)
    elif rank == 1:
        sub_matrix = comm.recv(source=0)
        print('la sous matrice sur le processeur 1 vaut : ', sub_matrix)


def scatter_comm(matrix, communicator):
    comm = communicator
    rank = comm.Get_rank()
    size = comm.Get_size()
    number_of_sub_matrix_per_rank = len(matrix) // size
    data = None

    if rank == 0:
        data = np.array(matrix)
        # print(type(np.array(matrix)))
        # print(np.array(matrix))

    recvbuf = np.empty([number_of_sub_matrix_per_rank, len(matrix[0])], dtype=int)
    recvbuf1 = np.empty([number_of_sub_matrix_per_rank * size, len(matrix[0])], dtype=int)
    print(recvbuf)
    comm.Scatterv(data, recvbuf, root=0)

    print('Processeur: ', rank, ', Vecteur: ', recvbuf)


def fusion(matrix):
    result_vector = []
    for line in matrix:
        for value in line:
            result_vector.append(value)
    return result_vector


def parallel_product_matrix_vector(matrix, vector):
    begin = time.time()

    comm = get_communicator()
    size = comm.Get_size()
    rank = comm.Get_rank()
    number_of_sub_matrix_per_rank = len(matrix) // size
    matrix_ = None

    if rank == 0:
        matrix_ = np.array(matrix)
        vector_ = np.array(vector)

    # Decoupage de la matrice en ligne et transmission aux differents processeurs
    recvbuf = np.empty([number_of_sub_matrix_per_rank, len(matrix[0])], dtype=int)
    comm.Scatterv(matrix_, recvbuf, root=0)
    print('Processeur: ', rank, ', Sous_Vecteur: ', recvbuf)
    print('\n')

    # Diffusion du vecteur a tous les processeurs
    if rank != 0:
        vector_ = np.empty([len(vector)], dtype=int)

    comm.Bcast(vector_, root=0)
    print('Processeur: ', rank, ', Vecteur: ', vector_)

    # if rank == 0:
    #    recvbuf_gather = np.empty([number_of_sub_matrix_per_rank*size, len(matrix[0])], dtype=int)

    vector_ = product_matrix_vector(recvbuf, vector_)
    print('Processeur: ', rank, ', result: ', vector_)

    recvbuf_ = None
    if rank == 0:
        recvbuf_ = np.empty([1, len(vector_)], dtype=int)

    res = comm.gather(vector_, root=0)

    if rank == 0:
        print('Processeur: ', rank, ', Result: ', res)
        result_vector = fusion(res)
        print(result_vector)

    end = time.time() - begin
    print(end)


parallel_product_matrix_vector([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]], [13, 14])
