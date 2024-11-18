import numpy as np

def jacobi(A, b, tol=1e-3, max_iter=50):
    n = len(A)
    x = np.zeros(n)
    D = np.diag(np.diag(A))
    LU = A - D

    D_inv = np.linalg.inv(D)
    T = -D_inv @ LU
    c = D_inv @ b

    # Calcular el radio espectral de la matriz T
    spectral_radius = max(abs(np.linalg.eigvals(T)))

    # Si el radio espectral es mayor o igual a 1, el método no converge
    if spectral_radius >= 1:
        return None, [], spectral_radius, T, [], None

    # Generar las ecuaciones despejadas para cada variable
    equations = []
    for i in range(n):
        equation = f"x{i+1} = "
        for j in range(n):
            if i != j:
                coef = T[i, j]
                sign = "+" if coef >= 0 else "-"
                equation += f" {sign} {abs(coef):.2f}*x{j+1}"
        equation += f" + {c[i]:.2f}"
        equations.append(equation)

    # Realizar las iteraciones del método de Jacobi
    steps = []
    for k in range(max_iter):
        x_new = T @ x + c
        error = np.linalg.norm(x_new - x)
        steps.append((x_new.copy(), error))
        if error < tol:
            break
        x = x_new

    # Verificación final: Ax = b
    Ax = A @ x
    return x, steps, spectral_radius, T, equations, Ax
