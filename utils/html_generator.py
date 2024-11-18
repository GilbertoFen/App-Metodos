def matrix_to_html_table(matrix, title=None):
    # Añadir un bloque de estilos
    html = """
    <style>
        table {
            border-collapse: collapse;
            width: 80%; /* Reduce el ancho para centrar mejor la tabla */
            margin: 20px auto; /* Centrar la tabla horizontalmente */
            text-align: center; /* Centrar el contenido de las celdas */
        }
        th, td {
            border: 1px solid #5B9BD5;
            padding: 10px;
            text-align: center;
            color: white;
        }
        th {
            background-color: #3A4F6F; /* Fondo del encabezado */
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #2C3E50; /* Color de fondo para filas pares */
        }
        tr:nth-child(odd) {
            background-color: #34495E; /* Color de fondo para filas impares */
        }
        tr:hover {
            background-color: #4A8AC4; /* Color al pasar el ratón */
        }
        h3 {
            margin-top: 20px;
        }
    </style>
    """

    # Añadir el título si está presente
    if title:
        html += f"<h3>{title}</h3>"

    # Generar la tabla en HTML
    html += "<table>"
    for row in matrix:
        html += "<tr>"
        for val in row:
            try:
                html += f"<td>{float(val):.4f}</td>"
            except ValueError:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</table><br>"
    return html


def vector_to_html_table(vector, title=None):
    html = """
    <style>
        table {
            border-collapse: collapse;
            width: 50%;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #5B9BD5;
            padding: 8px;
            text-align: center;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #2F4F6F;
        }
        tr:nth-child(odd) {
            background-color: #3A4F6F;
        }
        tr:hover {
            background-color: #4A8AC4;
        }
    </style>
    """
    if title:
        html += f"<h3>{title}</h3>"

    html += "<table>"
    for val in vector:
        try:
            html += f"<tr><td>{float(val):.4f}</td></tr>"
        except ValueError:
            html += f"<tr><td>{val}</td></tr>"
    html += "</table><br>"
    return html


def vector_comprobacion_table(b_original, b_calculado):
    html = "<h3>Comprobación: A * x = b</h3>"
    html += "<table border='1' cellspacing='0' cellpadding='4'>"
    html += "<tr><th>b Original</th><th>b Calculado (A * x)</th></tr>"
    # Juntamos con zip los elementos de b_original con el calculado
    for original, calculado in zip(b_original, b_calculado):
        try:
            html += f"<tr><td>{float(original):.4f}</td><td>{float(calculado):.4f}</td></tr>"
        except ValueError:
            html += f"<tr><td>{original}</td><td>{calculado}</td></tr>"
    html += "</table><br>"
    return html


# Recibe una lista de pasos de cada metodo que aplicamos
def steps_to_html(steps):
    html = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 15px;
        }
        th, td {
            border: 1px solid #5B9BD5;
            padding: 8px;
            text-align: center;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #2F4F6F;
        }
        tr:nth-child(odd) {
            background-color: #3A4F6F;
        }
        tr:hover {
            background-color: #4A8AC4;
        }
    </style>
    """
    html += "<h3>Pasos del Método</h3>"
    for step in steps:
        description = step.get("description", "")
        matrix = step.get("matrix", None)

        html += f"<h4>{description}</h4>"
        if matrix is not None:
            html += matrix_to_html_table(matrix)
    return html


# Tabla de iteraciones del metodo Jacobi
def iterations_to_html(steps):
    html = "<h3>Iteraciones</h3>"
    html += "<table border='1' cellspacing='0' cellpadding='4'>"
    html += "<tr><th>Iteración</th>" + "".join(f"<th>x{i+1}</th>" for i in range(len(steps[0][0]))) + "<th>Error</th></tr>"

    for idx, (solution, error) in enumerate(steps, start=1):
        html += f"<tr><td>{idx}</td>"
        html += "".join(f"<td>{val:.6f}</td>" for val in solution)
        html += f"<td>{error:.6f}</td></tr>"

    html += "</table><br>"
    return html


# Matriz T para metodo Jacobi
def matrix_T_to_html(T):
    return matrix_to_html_table(T, title="Matriz T")


# Ecuaciones del metodo Jacobi
def equations_to_html(equations):

    html = "<h3>Ecuaciones Despejadas</h3>"
    for eq in equations:
        html += f"<p>{eq}</p>"
    return html


# Pasos del metodo de pivoteo
def pivot_steps_to_html(steps):

    html = "<h3>Pasos de Pivoteo</h3>"
    for step in steps:
        description = step.get("description", "")
        matrix = step.get("matrix", None)

        # Mostrar la descripción del paso
        html += f"<h4>{description}</h4>"

        # Mostrar la matriz si está presente
        if matrix is not None:
            html += matrix_to_html_table(matrix)
    return html


def intercambio_steps_to_html(steps):
    html = "<h3>Pasos del Método de Intercambio</h3>"
    for matrix, description in steps:
        html += f"<h4>{description}</h4>"
        html += matrix_to_html_table(matrix)
    return html


def matrix_result_to_html(matrix, title):
    return matrix_to_html_table(matrix, title=title)


def comprobacion_to_html(b_original, b_computed):
    return vector_comprobacion_table(b_original, b_computed)
