import numpy as np

def gauss_jordan(A):
    n = A.shape[0]
    A_aug = np.hstack((A, np.eye(n)))
    steps = []

    # Aplicar el método de Gauss Jordan
    for i in range(n):
        pivot = A_aug[i, i]
        if pivot == 0:
            raise ValueError("No se puede dividir por cero")

        # Normalizar la fila del pivote
        A_aug[i] = A_aug[i] / pivot
        steps.append({
            "matrix": A_aug.copy(),
            "description": f"R{i+1} -> R{i+1} / {pivot:.6f}"
        })

        # Eliminar elementos en otras filas
        for j in range(n):
            if i != j:
                factor = A_aug[j, i]

                # Guardar la fila original para el paso
                prev_row = A_aug[j].copy()

                # Realizar la eliminación
                A_aug[j] = A_aug[j] - factor * A_aug[i]

                step_description = f"R{j+1} -> R{j+1} - ({factor:.6f}) * R{i+1}"
                steps.append({
                    "matrix": A_aug.copy(),
                    "description": step_description
                })

    # La matriz inversa 
    A_inv = A_aug[:, n:]

    return A_inv, steps
