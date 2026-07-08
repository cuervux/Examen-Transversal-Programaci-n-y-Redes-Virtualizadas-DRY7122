import requests


while True:

    origen = input("Ciudad de origen (s para salir): ")

    if origen.lower() == "s":
        break


    destino = input("Ciudad de destino (s para salir): ")

    if destino.lower() == "s":
        break


    print("\nMedio de transporte")
    print("1. Auto")
    print("2. Bus")

    opcion = input("Seleccione una opción: ")


    if opcion == "1":
        transporte = "Auto"

    elif opcion == "2":
        transporte = "Bus"

    else:
        print("Opción inválida")
        continue



    # Buscar coordenadas

    url = "https://nominatim.openstreetmap.org/search"

    headers = {
        "User-Agent": "DRY7122"
    }


    datos = {
        "format": "json",
        "limit": 1
    }


    datos["q"] = origen + ", Chile"

    respuesta = requests.get(
        url,
        params=datos,
        headers=headers
    )

    origen_json = respuesta.json()



    datos["q"] = destino + ", Argentina"

    respuesta = requests.get(
        url,
        params=datos,
        headers=headers
    )

    destino_json = respuesta.json()



    if not origen_json or not destino_json:
        print("Ciudad no encontrada")
        continue



    lat1 = origen_json[0]["lat"]
    lon1 = origen_json[0]["lon"]

    lat2 = destino_json[0]["lat"]
    lon2 = destino_json[0]["lon"]



    # Calcular ruta con OSRM

    ruta = (
        "https://router.project-osrm.org/route/v1/"
        f"driving/{lon1},{lat1};{lon2},{lat2}"
        "?steps=true"
    )


    respuesta = requests.get(ruta)

    datos_ruta = respuesta.json()



    if "routes" not in datos_ruta:
        print("No se pudo calcular la ruta")
        continue



    distancia_km = datos_ruta["routes"][0]["distance"] / 1000

    distancia_millas = distancia_km * 0.621371


    tiempo = datos_ruta["routes"][0]["duration"]


    horas = int(tiempo / 3600)

    minutos = int((tiempo % 3600) / 60)



    print("\n========== Resultado ==========")

    print("Origen:", origen)

    print("Destino:", destino)

    print("Transporte:", transporte)

    print("Kilómetros:", round(distancia_km, 2))

    print("Millas:", round(distancia_millas, 2))

    print("Duración:", horas, "horas", minutos, "minutos")



    print("\nNarrativa del viaje:")


    traduccion = {
        "new name": "Continuar por",
        "turn": "Girar hacia",
        "roundabout": "Entrar a la rotonda en",
        "exit roundabout": "Salir de la rotonda en",
        "merge": "Incorporarse a",
        "fork": "Tomar bifurcación en",
        "off ramp": "Tomar salida hacia",
        "arrive": "Llegar a",
        "depart": "Salir desde"
    }



    pasos = datos_ruta["routes"][0]["legs"][0]["steps"]


    for paso in pasos:

        tipo = paso["maneuver"]["type"]

        mensaje = traduccion.get(tipo, tipo)

        nombre = paso["name"]

        print("-", mensaje, nombre)


    print("==============================\n")

    print("======================\n")