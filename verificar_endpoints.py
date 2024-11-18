import requests

# Lista de endpoints de la API de Coursera
endpoints = {
    "Cursos": "https://api.coursera.org/api/courses.v1",
    "Detalles de un Curso Específico": "https://api.coursera.org/api/courses.v1/{course_id}",
    "Socios": "https://api.coursera.org/api/partners.v1",
    "Especializaciones": "https://api.coursera.org/api/specializations.v1",
    "Proyectos": "https://api.coursera.org/api/projects.v1",
    "Tipos de Cursos": "https://api.coursera.org/api/courseTypes.v1",
}

# ID de un curso de ejemplo para el endpoint de detalles
course_id = "l31la3mKEe-zFg7heHyXOQ"

# Función para verificar los endpoints
def verificar_endpoints():
    resultados = {}

    for nombre, url in endpoints.items():
        # Reemplazar el {course_id} si es necesario
        url_a_probar = url.replace("{course_id}", course_id) if "{course_id}" in url else url

        try:
            respuesta = requests.get(url_a_probar)
            resultados[nombre] = {
                "codigo_estado": respuesta.status_code,
                "respuesta": respuesta.json() if respuesta.status_code == 200 else None
            }
        except requests.exceptions.RequestException as e:
            resultados[nombre] = {
                "codigo_estado": "Error",
                "respuesta": str(e)
            }

    return resultados

# Ejecutar la verificación
resultados = verificar_endpoints()

# Imprimir los resultados
for nombre, resultado in resultados.items():
    print(f"Endpoint: {nombre}")
    print(f"Código de Estado: {resultado['codigo_estado']}")
    if resultado['codigo_estado'] == 200:
        print("Respuesta (primeros 100 caracteres):", str(resultado['respuesta'])[:100])
    else:
        print("Mensaje de error:", resultado['respuesta'])
    print("\n")
