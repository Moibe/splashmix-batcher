import csv
import os
import requests
import codecs

# Abrir y leer el archivo CSV
with open('archivo.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Ignorar la primera fila (encabezados)

    # Extraer URLs de la columna 29
    column_29 = []

    for row in reader:
        try:
            
            # Verifique si la URL ya está decodificada
            if isinstance(row[0], str):
                # Convierta la cadena a bytes antes de decodificar
                url_bytes = row[0].encode('utf-8')
            else:
                url_bytes = row[0]

            # Decodifica la URL con la codificación UTF-8
            decoded_url = codecs.decode(url_bytes, 'utf-8')
            print(decoded_url)
        except Exception as e:
            print("Caí en un error.")
            print(f"Ocurrió un error: {e}")
            # Maneje el error aquí (registrar, notificar, etc.)

        column_29.append(row[0])  # Asumiendo que la columna 29 es la 29 (índice 28)

# Crear la carpeta 'photos' si no existe
if not os.path.exists('photos'):
    os.makedirs('photos')

# Descargar y guardar imágenes
for i, url in enumerate(column_29):
    filename = os.path.basename(url)  # Extraer nombre de archivo de la URL
    print("Ésto es filename: ", filename)

    partes = filename.split('?')
    # print("Esto es partes: ", partes)
    print("Y ésto es partes[0]", partes[0])
    
    final_filename = f"{i+1}_{partes[0]}"  # Construir nombre de archivo final
    print("Esto es el nombre final: ", final_filename)

    # Descargar imagen y guardarla en la carpeta 'photos'
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'photos/{final_filename}.png', 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error al descargar imagen: {url}")