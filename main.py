#!/bin/python3

import time

from sequentiel import product_matrix_vector, product_matrix_matrix, product_vector_matrix, matrix_tran
from parallel import parallel_product_matrix_vector, parallel_product_matrix_matrix

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    vector = [1, 2]
    matrix_left = [[1, 2], [3, 4]]
    matrix_right = [[1, 0], [0, 1]]
    matrix_right2 = [[1, 1], [1, 1]]

    matrix_left3 = [[1, 2, 7, 2], [3, 4, 9, 7], [1, 9, 7, 8], [3, 4, 2, 7]]
    matrix_right3 = [[1, 8, 5, 6], [3, 6, 4, 8], [1, 14, 9, 2], [3, 6, 9, 23]]

    matrix_test = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]
    vector_test = [13, 14]

    restart = True
    while restart:
        welcome_text = """
            BIENVENUE AU PROJET D'ALGORITHME PARALLELE
            
        Note: Ce programme fait le produit matrice-vecteur et matrice-matrice
            avec la taille des matrices et vecteurs égale à n
        """

        print(welcome_text)
        proposition = """
        Différentes opérations:
        
            1- Calcul séquentiel du produit matrice-vecteur
            2- Calcul séquentiel du produit matrice-matrice
            3- Calcul parallèle du produit matrice-vecteur
            4- Calcul parallèle du produit matrice-matrice
        """
        print(proposition)
        choices = [1, 2, 3, 4]
        cpt = 1

        loop = True

        while loop:
            while cpt != 0:
                try:
                    choice = int(input("Que aimeriez-vous faire comme calcul ? "))
                    cpt = 0
                except ValueError:
                    print("Svp veuillez faire un choix entre 1 et 4.")

            try:
                dimension = int(input("Veuillez entrer la dimension de la matrice : "))
                if choice == 1:
                    begin = time.time()
                    print(product_matrix_vector(matrix_test, vector_test))
                    end = time.time() - begin
                    print(end)
                elif choice == 2:
                    print(product_matrix_matrix(matrix_left, matrix_right2))
                    print(product_matrix_matrix(matrix_left3, matrix_right3))
                    print(product_matrix_matrix(matrix_left, matrix_right))
                elif choice == 3:
                    parallel_product_matrix_vector([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]], [13, 14])
                elif choice == 4:
                    parallel_product_matrix_matrix([[1, 2], [3, 4], [1, 2], [3, 4]], [[1, 0], [0, 1], [1, 0], [0, 1]])
            except ValueError:
                pass
            response = input("Voulez-vous recommencer ? ( Oui / Non )").lower()
            if response == "non" or "n":
                loop = False
        response = input("Voulez-vous rentrer au départ ? ( Oui / Non )").lower()
        if response == "non" or "n":
            restart = False

    goodbye = """
        Nous vous remercions pour d'avoir utilisé notre programme
        En espérant vous revoir, nous vous disons à plus !!!
    """
    print(goodbye)