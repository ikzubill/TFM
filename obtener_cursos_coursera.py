import requests
import json

def obtener_cursos_coursera(limite=1000):
    api_url = "https://api.coursera.org/api/courses.v1"
    cursos = []
    pagina = 0  # Coursera API paginación empieza en 0

    while len(cursos) < limite:
        params = {
            "start": pagina * 50,  # 50 cursos por página
            "limit": 50,  # Número de cursos por solicitud
        }
        
        print(f"Solicitando la página {pagina + 1}...")
        respuesta = requests.get(api_url, params=params)

        # Verifica si la solicitud fue exitosa
        if respuesta.status_code != 200:
            print(f"Error en la solicitud: {respuesta.status_code}")
            break
        
        datos = respuesta.json()

        # Verifica si se obtuvieron cursos
        if not datos.get('elements'):
            print("No se encontraron más cursos.")
            break

        for curso in datos['elements']:
            if len(cursos) >= limite:
                break
            
            # Obtención de información adicional
            cursos.append({
                "titulo": curso.get("name", "N/A"),
                "enlace": f"https://www.coursera.org/learn/{curso.get('slug')}",
                "id": curso.get("id"),
                "tipo": curso.get("courseType", "N/A"),
                "descripcion": curso.get("description", "N/A"),
                "partner": curso.get("partner", {}).get("name", "N/A"),
                "imagen": curso.get("photoUrl", "N/A"),
                "idioma": curso.get("language", "N/A"),
                "duracion": curso.get("duration", "N/A"),
                "fecha_inicio": curso.get("startDate", "N/A"),
                "nivel": curso.get("level", "N/A"),
            })

        pagina += 1

    print(f"Total de cursos obtenidos: {len(cursos)}")
    return cursos[:limite]

# Obtener cursos
cursos = obtener_cursos_coursera()

# Guardar en archivo JSON
with open("cursos_coursera.json", "w", encoding="utf-8") as f:
    json.dump(cursos, f, ensure_ascii=False, indent=4)

print("Cursos guardados en cursos_coursera.json")
