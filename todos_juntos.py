import json
import os
import pandas as pd

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
                combined_courses.append(course)

# Si combined_courses es una lista de diccionarios, conviértelo en DataFrame
if isinstance(combined_courses, list):
    combined_courses = pd.DataFrame(combined_courses)

# Prefijo de la URL de Udemy
udemy_base_url = "https://www.udemy.com"
combined_courses["url"] = udemy_base_url + combined_courses["url"]

# Guardar el DataFrame en JSON sin caracteres escapados en las URLs
output_file = "todos_juntos.json"
combined_courses.to_json(output_file, orient="records", indent=4, force_ascii=False)

# Leer el archivo JSON y eliminar las barras invertidas de las URLs
with open(output_file, "r", encoding="utf-8") as file:
    json_content = file.read().replace("\\/", "/")  # Reemplaza "\/" por "/"

# Sobrescribir el archivo con las URLs corregidas
with open(output_file, "w", encoding="utf-8") as file:
    file.write(json_content)

print(f"JSON combinado guardado en {output_file} sin barras invertidas en las URLs.")
