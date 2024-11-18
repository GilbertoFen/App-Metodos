import numpy as np

import numpy as np

def pivoteo_parcial(A, b):
    n = A.shape[0]
    A_aug = np.hstack((A, b.reshape(-1, 1)))
    steps = []

    for i in range(n):
        # Encontrar el pivote elemento mayor en la columna i
        max_row = np.argmax(np.abs(A_aug[i:, i])) + i
        if max_row != i:
            # Intercambiar filas si es necesario
            A_aug[[i, max_row]] = A_aug[[max_row, i]]
            steps.append({
                "matrix": A_aug.copy(),
                "description": f"Intercambiar  R{i + 1} <-> R{max_row + 1}"
            })

        pivot = A_aug[i, i]
        if pivot == 0:
            raise ValueError("La matriz es singular, no se puede continuar.")

        # Dividir la fila del pivote por el valor del pivote
        A_aug[i] = A_aug[i] / pivot
        steps.append({
            "matrix": A_aug.copy(),
            "description": f"R{i + 1} -> R{i + 1} / {pivot:.6f}"
        })

        # Eliminar los elementos debajo del pivote
        for j in range(i + 1, n):
            factor = A_aug[j, i]
            A_aug[j] = A_aug[j] - factor * A_aug[i]
            steps.append({
                "matrix": A_aug.copy(),
                "description": f"R{j + 1} -> R{j + 1} - ({factor:.6f}) * R{i + 1}"
            })

    # Sustitución hacia atrás para encontrar la solución
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = A_aug[i, -1] - np.dot(A_aug[i, i + 1:n], x[i + 1:n])
        steps.append({
            "matrix": A_aug.copy(),
            "description": f"Sustitución hacia atrás para x_{i + 1}"
        })

    return x, steps


def pivoteo_total(A, b):
    n = A.shape[0]
    A_aug = np.hstack((A, b.reshape(-1, 1)))
    orden_columnas = list(range(n))
    steps = []

    for i in range(n):
        submatriz = np.abs(A_aug[i:, i:n])
        max_pos = np.unravel_index(np.argmax(submatriz), submatriz.shape)
        max_row = max_pos[0] + i
        max_col = max_pos[1] + i

        if max_row != i:
            A_aug[[i, max_row]] = A_aug[[max_row, i]]
            steps.append({"description": f"Intercambiar R{i+1} <-> R{max_row+1}", "matrix": A_aug.copy()})

        if max_col != i:
            A_aug[:, [i, max_col]] = A_aug[:, [max_col, i]]
            orden_columnas[i], orden_columnas[max_col] = orden_columnas[max_col], orden_columnas[i]
            steps.append({"description": f"Intercambiar C{i+1} <-> C{max_col+1}", "matrix": A_aug.copy()})

        pivot = A_aug[i, i]
        if pivot == 0:
            raise ValueError("El sistema no tiene solución única")
        A_aug[i] = A_aug[i] / pivot
        steps.append({"description": f"R{i+1} -> R{i+1} / {pivot:.6f}", "matrix": A_aug.copy()})

        for j in range(i + 1, n):
            factor = A_aug[j, i]
            A_aug[j] = A_aug[j] - factor * A_aug[i]
            steps.append({"description": f"R{j+1} -> R{j+1} - ({factor:.6f}) * R{i+1}", "matrix": A_aug.copy()})

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = A_aug[i, -1] - np.dot(A_aug[i, i + 1:n], x[i + 1:n])

    x_reordenado = np.zeros_like(x)
    for idx, col in enumerate(orden_columnas):
        x_reordenado[col] = x[idx]

    return x_reordenado, A_aug, steps


def pivoteo_escalonado(A, b):
    n = A.shape[0]
    A_aug = np.hstack((A, b.reshape(-1, 1)))
    escala = np.max(abs(A), axis=1)
    steps = []

    for i in range(n):
        razones = abs(A_aug[i:, i]) / escala[i:]
        max_row = np.argmax(razones) + i

        if i != max_row:
            A_aug[[i, max_row]] = A_aug[[max_row, i]]
            escala[[i, max_row]] = escala[[max_row, i]]
            steps.append({"description": f"Intercambiar R{i+1} <-> R{max_row+1}", "matrix": A_aug.copy()})

        pivot = A_aug[i, i]
        if pivot == 0:
            raise ValueError("El sistema no tiene solución única")
        A_aug[i] = A_aug[i] / pivot
        steps.append({"description": f"R{i+1} -> R{i+1} / {pivot:.6f}", "matrix": A_aug.copy()})

        for j in range(i + 1, n):
            factor = A_aug[j, i]
            A_aug[j] = A_aug[j] - factor * A_aug[i]
            steps.append({"description": f"R{j+1} -> R{j+1} - ({factor:.6f}) * R{i+1}", "matrix": A_aug.copy()})

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = A_aug[i, -1] - np.dot(A_aug[i, i + 1:n], x[i + 1:n])

    return x, A_aug, steps
