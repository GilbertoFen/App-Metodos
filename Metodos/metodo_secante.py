import numpy as np

def secant_method(f, a, b, tol=1e-6, max_iter=100):
    global xn
    # Almacenamos las iteraciones
    iterations = []
    try:
        x0, x1 = a, b
        # Evaluamos nuestra funcion en el punto a y b / x0, x1
        f_x0, f_x1 = f(x0), f(x1)
        error = np.inf
        iter_count = 0

        while error > tol and iter_count < max_iter:
            # Verificar si se está dividiendo por cero
            if (f_x1 - f_x0) == 0:
                raise ZeroDivisionError("Diferencia entre f(x1) y f(x0) es cero, no se puede continuar")

            # Método de la secante
            xn = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

            # Calcular f(xn)
            f_xn = f(xn)

            if np.isinf(f_xn) or np.isnan(f_xn):
                raise ValueError("f(xn) devuelve un valor no válido")

            error = abs((xn - x1) / (xn if xn != 0 else 1))

            # Guardar todos los valores de la iteracion en la lista
            iterations.append((x0, x1, xn, f_x0, f_x1, f_xn, error))

            # Actualizar los valores para la siguiente iteracion
            x0, x1 = x1, xn
            f_x0, f_x1 = f_x1, f_xn
            iter_count += 1

        return xn, iterations

    except ZeroDivisionError as zde:
        print(f"Error: {zde}")
        return None, []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None, []
