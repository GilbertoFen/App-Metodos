import numpy as np

def gauss_jordan_partitioned(A, b):

    n = A.shape[0]

    # Determinar el tamaño de los bloques en función de n
    if n == 6:
        block_size = 2
    elif n == 9:
        block_size = 3
    else:
        raise ValueError("La matriz debe ser de tamaño 6x6 o 9x9.")

    # Crear la matriz aumentada A|I|b
    A_aug = np.hstack((A, np.eye(n), b.reshape(-1, 1)))
    steps = []

    def get_block(matrix, row, col, block_size=block_size):
        return matrix[row*block_size:(row+1)*block_size, col*block_size:(col+1)*block_size]

    # Inversión y eliminación en bloques
    for k in range(n // block_size):
        # Obtener el bloque diagonal A_kk
        A_kk = get_block(A_aug, k, k)

        # Verificar si el bloque es invertible
        if np.linalg.det(A_kk) == 0:
            raise ValueError(f"El bloque {k+1} no es invertible.")

        # Invertir el bloque A_kk
        A_kk_inv = np.linalg.inv(A_kk)
        steps.append({"matrix": A_kk_inv, "description": f"Invertir bloque A{k+1}{k+1}"})

        # Premultiplicar la fila correspondiente por A_kk_inv
        A_aug[k*block_size:(k+1)*block_size, :] = A_kk_inv @ A_aug[k*block_size:(k+1)*block_size, :]
        steps.append({"matrix": A_aug.copy(), "description": f"Premultiplicar fila {k+1} por A_kk^-1"})

        # Eliminar elementos en otras filas usando el bloque invertido
        for i in range(n // block_size):
            if i != k:
                factor = get_block(A_aug, i, k)

                # Guardar la copia antes de la eliminación para el paso
                prev_block = A_aug[i*block_size:(i+1)*block_size, :].copy()

                # Realizar la eliminación
                A_aug[i*block_size:(i+1)*block_size, :] -= factor @ A_aug[k*block_size:(k+1)*block_size, :]

                # Construir la descripción en forma de operación elemental
                step_description = f"R{i+1} -> R{i+1} - ({factor}) * R{k+1}"
                steps.append({
                    "matrix": A_aug.copy(),
                    "description": step_description
                })

    # La columna más a la derecha de A_aug contiene la solución
    solution = A_aug[:, -1]

    # Las columnas intermedias de A_aug contienen la matriz inversa
    inverse_matrix = A_aug[:, n:2*n]

    # Comprobación Ax = b
    b_computed = np.dot(A, solution)
    if not np.allclose(b_computed, b):
        print("Advertencia: La comprobación Ax != b")

    return solution, steps, inverse_matrix
