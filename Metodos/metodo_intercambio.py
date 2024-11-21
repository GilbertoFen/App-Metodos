import numpy as np

def metodo_intercambio(A, b, precision=12):
    n = len(A)
    matrices_intermedias = []

    # Matriz aumentada A|b
    A_aug = np.copy(A)
    b_original = np.copy(b)
    orden_filas = list(range(n))
    orden_columnas = list(range(n))

    # Realizamos el método de intercambio 
    for k in range(n):
        max_element = 0
        pivote_fila, pivote_columna = None, None
        for i in range(n):
            for j in range(n):
                if abs(A_aug[i, j]) > max_element:
                    max_element = abs(A_aug[i, j])
                    pivote_fila, pivote_columna = i, j

        if pivote_fila is None or pivote_columna is None:
            raise ValueError("No se puede encontrar un pivote válido. El sistema puede ser singular.")

        orden_filas[k], orden_filas[pivote_fila] = orden_filas[pivote_fila], orden_filas[k]
        orden_columnas[k], orden_columnas[pivote_columna] = orden_columnas[pivote_columna], orden_columnas[k]

        pivote = A_aug[pivote_fila, pivote_columna]
        for j in range(n):
            if j != pivote_columna:
                A_aug[pivote_fila, j] = -A_aug[pivote_fila, j] / pivote
        A_aug[pivote_fila, pivote_columna] = pivote

        matrices_intermedias.append((A_aug.copy(), f"R{pivote_fila+1} / {pivote} *(-1) Excepto al pivote"))

        for i in range(n):
            if i != pivote_fila:
                factor = A_aug[i, pivote_columna]
                for j in range(n):
                    if j != pivote_columna:
                        A_aug[i, j] += factor * A_aug[pivote_fila, j]

                A_aug[i] = np.round(A_aug[i], precision)

        matrices_intermedias.append((A_aug.copy(), f"Sumar R{pivote_fila+1} a otras filas"))

        for i in range(n):
            if i != pivote_fila:
                A_aug[i, pivote_columna] /= pivote

        A_aug[pivote_fila, pivote_columna] = 1 / pivote
        matrices_intermedias.append((A_aug.copy(), f"Reemplazar pivote de fila {pivote_fila+1} y columna {pivote_columna+1} por su recíproco"))

    A_final_intercambio = np.zeros_like(A)
    for i in range(n):
        for j in range(n):
            A_final_intercambio[i, j] = A_aug[orden_filas[i], orden_columnas[j]]

    # Calcular la inversa usando numpy para la comprobación
    A_numpy_inv = np.linalg.inv(A)
    A_numpy_inv = np.round(A_numpy_inv, precision)

    # Utilizar numpy.linalg.solve para obtener la solución correcta
    x_correcto = np.linalg.solve(A, b_original)
    x_correcto = np.round(x_correcto, precision)

    # Comprobación A * x = b usando la solución correcta
    b_computed_correct = np.dot(A, x_correcto)
    b_computed_correct = np.round(b_computed_correct, precision)

    return matrices_intermedias, A_final_intercambio, A_numpy_inv, x_correcto, b_computed_correct
