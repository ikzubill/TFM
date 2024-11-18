import requests
import json

access_token = "VtgO9rJR19PPDjJqntH1MaWtxPSRTIwwq1dCAQbuqOg:WClKPz1/OwZbLognk+azICW1/xJBj0UwbXxNjEq8DK8"

def obtener_cursos(limit=1100):
    url = "https://www.udemy.com/api-2.0/courses/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    todos_cursos = []
    next_url = url
    total_cursos = 0

    while next_url and total_cursos < limit:
        response = requests.get(next_url, headers=headers, params={"page_size": 100})
        
        if response.status_code != 200:
            print("Error:", response.status_code, response.json())
            return  # Termina si hay un error en la respuesta
        
        data = response.json()
        
        # Verificar si 'results' está vacío
        if 'results' not in data or not data['results']:
            print("No se encontraron cursos en esta página o estructura de datos inesperada.")
            break
        
        todos_cursos.extend(data['results'])
        total_cursos += len(data['results'])
        
        next_url = data.get("next")

    # Guardar todos los cursos en un archivo JSON
    with open("1100_cursos_udemy.json", "w", encoding="utf-8") as f:
        json.dump(todos_cursos, f, ensure_ascii=False, indent=4)
    
    print(f"Se han obtenido un total de {total_cursos} cursos.")
    return todos_cursos

# Ejecuta la función
obtener_cursos()
