import numpy as np

def eliminacion_gaussiana(A, b):
    """
    Método de Eliminación Gaussiana para resolver el sistema Ax = b.
    Devuelve la solución x, así como los pasos realizados.
    """
    n = len(b)
    A_aug = np.hstack((A, b.reshape(-1, 1)))
    steps = []

    # Eliminación hacia adelante para convertir A en una matriz triangular superior
    for i in range(n):
        # Encontrar el pivote máximo en la columna actual
        max_row = np.argmax(abs(A_aug[i:, i])) + i
        if A_aug[max_row, i] == 0:
            raise ValueError("La matriz es singular y no tiene solución única")

        # Intercambiar filas si el pivote no está en la fila actual
        if max_row != i:
            A_aug[[i, max_row]] = A_aug[[max_row, i]]
            steps.append({
                "matrix": A_aug.copy(),
                "description": f"Intercambiar fila {i+1} con fila {max_row+1}"
            })

        # Dividir la fila pivote por el elemento pivote
        pivot = A_aug[i, i]
        A_aug[i] = A_aug[i] / pivot
        steps.append({
            "matrix": A_aug.copy(),
            "description": f"Dividir fila {i+1} entre {pivot:.6f}"
        })

        # Eliminar los elementos debajo del pivote
        for j in range(i + 1, n):
            factor = A_aug[j, i]
            A_aug[j] = A_aug[j] - factor * A_aug[i]
            steps.append({
                "matrix": A_aug.copy(),
                "description": f"Eliminar elemento en fila {j+1}, columna {i+1}"
            })

    # Sustitución hacia atrás para resolver el sistema
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = A_aug[i, -1] - np.dot(A_aug[i, i+1:n], x[i+1:n])
        steps.append({
            "matrix": A_aug.copy(),
            "description": f"Sustitución hacia atrás para x_{i+1}"
        })

    return x, steps
