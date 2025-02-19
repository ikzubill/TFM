import json
import os

# Carpeta donde están los archivos JSON
json_folder = "udemy"

# Lista para almacenar los cursos combinados
combined_courses = []

# Prefijo de la URL de Udemy
udemy_base_url = "https://www.udemy.com"

# Recorrer los archivos JSON en la carpeta
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        category = filename.replace(".json", "").replace(
            " & ", " and "
        )  # Convertir " & " a "and" para evitar problemas en nombres

        with open(os.path.join(json_folder, filename), "r", encoding="utf-8") as file:
            data = json.load(file)

            # Extraer cursos de la clave "results"
            for course in data.get("results", []):
                course_info = {
                    "id": course.get("id"),
                    "title": course.get("title"),
                    "url": udemy_base_url
                    + course.get("url", ""),  # Concatenar la URL base
                    "price": course.get("price"),
                    "category": category,  # Agregar la categoría basada en el archivo
                    "instructors": [
                        instructor.get("display_name")
                        for instructor in course.get("visible_instructors", [])
                    ],
                }
                combined_courses.append(course_info)

# Guardar el resultado en un nuevo archivo JSON
output_file = "combined_udemy_courses.json"
with open(output_file, "w", encoding="utf-8") as out_file:
    json.dump(combined_courses, out_file, indent=4, ensure_ascii=False)

print(f"JSON combinado guardado en {output_file}")
