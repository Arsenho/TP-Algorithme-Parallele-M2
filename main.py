#!/bin/python3

import time

from sequentiel import product_matrix_vector, product_matrix_matrix, product_vector_matrix, matrix_tran
from parallel import parallel_product_matrix_vector, parallel_product_matrix_matrix
from matrix_generate import matrix_generate, generate_matrix_vector


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    restart = True
    #while restart:
        # welcome_text = """
        #   BIENVENUE AU PROJET D'ALGORITHME PARALLELE

        # Note: Ce programme fait le produit matrice-vecteur et matrice-matrice
        #     avec la taille des matrices et vecteurs égale à n
    # """

        #print(welcome_text)
        #proposition = """
        #Différentes opérations:
        #    0- Définir les caracteristiques de votre matrice
        #    1- Calcul séquentiel du produit matrice-vecteur
         #   2- Calcul séquentiel du produit matrice-matrice
         #   3- Calcul parallèle du produit matrice-vecteur
         #   4- Calcul parallèle du produit matrice-matrice
        #"""
        #print(proposition)
        #choices = [1, 2, 3, 4]
        #cpt = 1

        #loop = True

        #while loop:
    # while cpt != 0:
        # try:
            #    choice = int(input("Que aimeriez-vous faire comme calcul ? "))
                    # cpt = 0
                    #    except ValueError:
                    #        print("Svp veuillez faire un choix entre 1 et 4.")

            # try:
        # if choice == 0:
            #    row = int(input("Veuillez entrer le nombre de ligne de la matrice : "))
                    #   column = int(input("Veuillez entrer le nombre de colonne de la matrice : "))
                    #    my_matrix = matrix_generate(n=row, m=column)
                    #    print(my_matrix)
                    #elif choice == 1:
                    #pass
                    #          elif choice == 2:
                #                print(product_matrix_matrix(my_matrix[0], my_matrix[1]))
            #            elif choice == 3:
            #                pass
                    #             elif choice == 4:
                    #                print(parallel_product_matrix_matrix(my_matrix[0], my_matrix[1]))
                    #        except ValueError:
        #            pass
            #        response = input("Voulez-vous recommencer ? ( Oui / Non )").lower()
            #        if response == "non":
        #            loop = False
        #    response = input("Voulez-vous rentrer au départ ? ( Oui / Non )").lower()
    #    if response == "non":
    #        restart = False

    #goodbye = """
    #    Nous vous remercions d'avoir bien voulu utiliser notre programme
    #        En espérant vous revoir, nous vous disons à plus !!!
    #"""
    # print(goodbye)

    my_matrix = matrix_generate(n=6, m=5)
    #print(product_matrix_matrix(my_matrix[0], my_matrix[1])[1])
    print("\n")
    print(parallel_product_matrix_matrix(my_matrix[0], my_matrix[1])[2])

