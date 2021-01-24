import time

from sequentiel import product_matrix_vector, product_matrix_matrix, product_vector_matrix


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

    begin = time.time()

    matrix_test = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]
    vector_test = [13, 14]

    print(product_matrix_vector(matrix_test, vector_test))
    end = time.time() - begin
    print(end)
    print(product_matrix_matrix(matrix_left, matrix_right))
    print(product_vector_matrix(vector, matrix_right))
    print(product_matrix_matrix(matrix_left, matrix_right2))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
