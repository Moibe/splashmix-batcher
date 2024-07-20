import pandas as pd

# Carga del Excel
archivo_excel = "xcel/origenjsons.xlsx" # Reemplaza con la ruta de tu archivo
df = pd.read_excel(archivo_excel)

#Primero obtengo todos los encabezados.
lista_encabezados = df.columns.to_list()

lista_columnas = []  
lista_columnas_individuales = {}  # Diccionario para almacenar las listas individuales

# Recorre la lista de encabezados
for encabezado in lista_encabezados:
    # Obtiene la columna usando la indexación
    columna = df[encabezado]
    # Convierte la columna a lista (opcional)
    columna_como_lista = columna.to_list()
    # Crea una nueva lista para la columna actual
    lista_columna_actual = []
    # Agrega los valores de la columna a la lista
    for valor in columna:
        lista_columna_actual.append(valor)
    # Almacena la lista individual en el diccionario
    lista_columnas_individuales[encabezado] = lista_columna_actual

with open("data.py", "w") as archivo:

    # Recorrer el diccionario de listas individuales
    for nombre_columna, lista_valores in lista_columnas_individuales.items():
        # Crear una cadena con la definición de la variable
        definicion_variable = f"lista_{nombre_columna} = {str(lista_valores)}\n"

        # Escribir la definición de la variable en el archivo
        archivo.write(definicion_variable)

