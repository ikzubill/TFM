import requests
import json

# Definir el token de acceso
access_token = "VtgO9rJR19PPDjJqntH1MaWtxPSRTIwwq1dCAQbuqOg:WClKPz1/OwZbLognk+azICW1/xJBj0UwbXxNjEq8DK8"

# Lista de categorías que devuelven:
categorias = [
    "Business", "Development",  "IT & Software", 
    "Marketing", "Office Productivity", "Personal Development", 
     "Design", "Health & Fitness", "Music", "Teaching & Academics",
     "Lifestyle"
]

# Lista de categorías que NO devuelven:
# categorias = [
#     "Arts", "Language Learning", "Science", "Engineering", 
#     "Social Sciences", "Software Development", "Data Science", "Game Development", 
#     "Cybersecurity", "Sales", "Artificial Intelligence", "Web Development", 
#     "Video Editing", "Communication", "Photography", "Finance", "Photography"
# ]


# Función para realizar las llamadas a la API
def obtener_cursos_por_categoria(categoria, page_size=10):
    url = f"https://www.udemy.com/api-2.0/courses/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {"page_size": page_size, "category": categoria}
    
    response = requests.get(url, headers=headers, params=params)
    
    # Comprobamos el estado de la respuesta
    if response.status_code == 200:
        data = response.json()
        if data["count"] > 0:
            # Guardar el resultado en un archivo JSON
            with open(f"cursos_{categoria}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Cursos encontrados para la categoría {categoria}.")
        else:
            print(f"No se encontraron cursos para la categoría {categoria}.")
    else:
        print(f"Error con la categoría {categoria}. Código de estado: {response.status_code}")

# Ejecutar pruebas para cada categoría
for categoria in categorias:
    obtener_cursos_por_categoria(categoria)
