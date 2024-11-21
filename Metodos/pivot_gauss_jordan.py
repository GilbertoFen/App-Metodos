import numpy as np

import numpy as np

def pivoteo_parcial(A, b):
    n = A.shape[0]
    A_aug = np.hstack((A, b.reshape(-1, 1)))
    steps = []

    for i in range(n):
        # Encontrar el pivote
        max_row = np.argmax(np.abs(A_aug[i:, i])) + i
        if max_row != i:
            # Intercambiar filas si es necesario
            A_aug[[i, max_row]] = A_aug[[max_row, i]]
            steps.append({
                "matrix": A_aug.copy(),
                "description": f"Intercambiar R{i + 1} < - > R{max_row + 1}"
            })

        pivot = A_aug[i, i]
        if pivot == 0:
            raise ValueError("La matriz es singular, no se puede continuar.")

        # Eliminar los elementos debajo del pivote
        for j in range(i + 1, n):
            factor = A_aug[j, i] / pivot  # Factor de eliminación
            A_aug[j] -= factor * A_aug[i]
            steps.append({
                "matrix": A_aug.copy(),
                "description": f"R{j + 1} -> R{j + 1} - ({factor:.6f}) * R{i + 1}"
            })

    # Sustitución hacia atrás para encontrar la solución

    x = np.zeros(n)
    equations = []
    for i in range(n - 1, -1, -1):
        x[i] = (A_aug[i, -1] - np.dot(A_aug[i, i + 1:n], x[i + 1:n])) / A_aug[i, i]

        # Crear la ecuación despejada para la variable x[i]
        terms = " + ".join([f"{-A_aug[i, j]:.4f}*x{j+1}" for j in range(i + 1, n) if A_aug[i, j] != 0])
        equation = f"x{i+1} = ({A_aug[i, -1]:.4f} - ({terms})) / {A_aug[i, i]:.4f}"
        equations.append(equation)

        steps.append({
            "description": f"Ecuación despejada para x{i+1}: {equation}",
            "matrix": None 
        })
    return x, steps



def pivoteo_total(A, b):
    n = A.shape[0]
    # Matriz aumentada A|b
    A_aug = np.hstack((A, b.reshape(-1, 1)))  
    orden_columnas = list(range(n))
    steps = []


    for i in range(n):
        # Selección del mayor pivote
        submatriz = np.abs(A_aug[i:, i:n])
        max_pos = np.unravel_index(np.argmax(submatriz), submatriz.shape)
        max_row = max_pos[0] + i
        max_col = max_pos[1] + i

        # Intercambio de filas si es necesario
        if max_row != i:
            A_aug[[i, max_row]] = A_aug[[max_row, i]]
            steps.append({"description": f"Intercambiar R{i+1} < - > R{max_row+1}", "matrix": A_aug.copy()})

        # Intercambio de columnas si es necesario
        if max_col != i:
            A_aug[:, [i, max_col]] = A_aug[:, [max_col, i]]
            orden_columnas[i], orden_columnas[max_col] = orden_columnas[max_col], orden_columnas[i]
            steps.append({"description": f"Intercambiar C{i+1} < - > C{max_col+1}", "matrix": A_aug.copy()})

        pivot = A_aug[i, i]
        if pivot == 0:
            raise ValueError("El sistema no tiene solución única.")

        # Eliminar los elementos debajo del pivote
        for j in range(i + 1, n):
            factor = A_aug[j, i] / pivot
            A_aug[j] -= factor * A_aug[i]
            steps.append({"description": f"R{j+1} -> R{j+1} - ({factor:.6f}) * R{i+1}", "matrix": A_aug.copy()})

    # Sustitución hacia atras
    x = np.zeros(n)
    equations = []
    for i in range(n - 1, -1, -1):
        x[i] = (A_aug[i, -1] - np.dot(A_aug[i, i + 1:n], x[i + 1:n])) / A_aug[i, i]

        # Crear la ecuación despejada para la variable x[i]
        terms = " + ".join([f"{-A_aug[i, j]:.4f}*x{j+1}" for j in range(i + 1, n) if A_aug[i, j] != 0])
        equation = f"x{i+1} = ({A_aug[i, -1]:.4f} - ({terms})) / {A_aug[i, i]:.4f}"
        equations.append(equation)

        steps.append({
            "description": f"Ecuación despejada para x{i+1}: {equation}",
            "matrix": None 
        })

    # Reordenar el vector solución de acuerdo con el intercambio de columnas
    x_reordenado = np.zeros_like(x)
    for idx, col in enumerate(orden_columnas):
        x_reordenado[col] = x[idx]

    return x_reordenado, A_aug, steps



def pivoteo_escalonado(A, b):

    n = A.shape[0]
    A_aug = np.hstack((A, b.reshape(-1, 1)))
     # Vector de escalas
    escala = np.max(abs(A), axis=1) 
    steps = []

    # Eliminación escalonada
    for i in range(n):
        # Calcular razones para el pivoteo escalonado
        razones = abs(A_aug[i:, i]) / escala[i:]
        max_row = np.argmax(razones) + i

        # Intercambiar filas si es necesario
        if i != max_row:
            A_aug[[i, max_row]] = A_aug[[max_row, i]]
            escala[[i, max_row]] = escala[[max_row, i]]
            steps.append({
                "description": f"Intercambiar R{i+1} < - > R{max_row+1}",
                "matrix": A_aug.copy()
            })

        pivot = A_aug[i, i]
        if pivot == 0:
            raise ValueError("El sistema no tiene solución única.")

        # Eliminar los elementos debajo del pivote
        for j in range(i + 1, n):
            factor = A_aug[j, i] / pivot
            A_aug[j, i:] -= factor * A_aug[i, i:]
            steps.append({
                "description": f"R{j+1} -> R{j+1} - ({factor:.6f}) * R{i+1}",
                "matrix": A_aug.copy()
            })

    # Sustitución hacia atrás para encontrar la solución

    x = np.zeros(n)
    equations = []
    for i in range(n - 1, -1, -1):
        x[i] = (A_aug[i, -1] - np.dot(A_aug[i, i + 1:n], x[i + 1:n])) / A_aug[i, i]

        # Crear la ecuación despejada para la variable x[i]
        terms = " + ".join([f"{-A_aug[i, j]:.4f}*x{j+1}" for j in range(i + 1, n) if A_aug[i, j] != 0])
        equation = f"x{i+1} = ({A_aug[i, -1]:.4f} - ({terms})) / {A_aug[i, i]:.4f}"
        equations.append(equation)

        steps.append({
            "description": f"Ecuación despejada para x{i+1}: {equation}",
            "matrix": None 
        })

    return x, A_aug, steps

