import csv
import os
import time
import requests
from io import BytesIO


def getImages():

    # Abrir y leer el archivo CSV
    with open('archivo.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Ignorar la primera fila (encabezados)

        #Se habrá creado un archivo csv cuyo única columna sean las URL de las fotos con las que trabajaremos.

        #Aquí guardaremos esa información.
        urls_photos = []

        for row in reader:       
            urls_photos.append(row[0])  

    # Crear la carpeta 'photos' si no existe
    if not os.path.exists('photos'):
        os.makedirs('photos')

    # Descargar y guardar imágenes
    for i, url in enumerate(urls_photos):
        filename = os.path.dirname(url)  # Extraer nombre de archivo de la URL
        # print("Esto es filename (dirname): ", filename)
        
        partes = filename.split('image/')
        siguiente = partes[1].split('/')
        # print("Siguiente es: ", siguiente[0])
        
        final_filename = f"{siguiente[0]}"  # Construir nombre de archivo final
        # print("Esto es el nombre final: ", final_filename)

        # Descargar imagen y guardarla en la carpeta 'photos'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'photos/{final_filename}.png', 'wb') as f:
                f.write(response.content)
            print("Escritura correcta.")
        else:
            print(f"Error al descargar imagen: {url}")
            # Guardar una imagen en blanco
            imagen_en_blanco = BytesIO()  # Crear un objeto BytesIO vacío
            imagen_en_blanco.write(b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C9AAAAASUVORK5CYII=")  # Datos PNG de una imagen en blanco
            imagen_en_blanco.seek(0)  # Rebobinar el objeto BytesIO al principio

            with open(f'photos/{final_filename}.png', 'wb') as f:
                f.write(imagen_en_blanco.read())
            print(f"Imagen '{final_filename}' en blanco guardada como alternativa.")

            # Puedes agregar un tiempo de espera (por ejemplo, 1 segundo) para evitar descargas accidentales
            time.sleep(1)