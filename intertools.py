import os
import time
import pretools
import pandas as pd
import nycklar.nodes as nodes
import configuracion
from prompts import Prompt, Superhero, Hotgirl
import tools
import globales
import random
import importlib
import data.prompts

def sampler(sesion, inicial=None):

    #Útil: Auxiliar para obtener dataframe: (como cuando no quieres correr prepararDataFrame de nuevo.)
    #dataframe = pd.read_excel(filename)
    #Auxiliar para archivo excel de resultados.
    #La ruta sirve con diagonal normal / o con doble diagonal \\
    dataframe = pd.read_excel(globales.excel_results_path + sesion + '.xlsx')

    #IMPORTANTE, Asigna los atributos a cada sample.
    
    #Destino donde irán los resultados.
    ruta_destino = sesion + "-results"
    target_dir = os.path.join('imagenes', 'resultados', ruta_destino)

    #En caso de no existir el directorio donde se recibirán las imagenes destino, lo creará.
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    #Va todo en un try para que podamos guardar el dataframe en un excel en caso de interrupción del ciclo:
    try:

        #Filtra las filas donde 'Download Status' es igual a 'Success'
        df_images_ok = tools.funcionFiltradora(dataframe, 'Download Status', 'Success')

        #Future haz una función creadora de Columnas.
        # Crea un dataset 'columna_imagenes' a partir de la columna 'Nombre'
        columna_samples = df_images_ok['File']
        
        #Si se le pasó el valor como parámetro entonces hace la búsqueda desde donde empezará.
        if inicial is not None: 
            
            #PROCESO PARA INICIAR DONDE NOS QUEDAMOS            
            # Ésta es la foto donde iniciará, que se pasa como parámetro a preProcess.
            texto_fila_objetivo = inicial  # Replace with your actual search text
            print("El archivo en el que iniciaremos es: ", inicial)
                        
            # Create a boolean mask to identify the row matching the text
            mascara_fila_objetivo = df_images_ok['File'].str.contains(texto_fila_objetivo)
            # Get the index of the matching row
            indice_fila_objetivo = mascara_fila_objetivo.idxmax()  # Assumes only one match
            print("Su índice idmax es: ", indice_fila_objetivo)            
            
            # If the text is found, get the names from that row onward
            if indice_fila_objetivo is not None:
                nombres_a_partir_fila_objetivo = columna_samples.iloc[indice_fila_objetivo:]
                print("Objetivo encontrado: ", nombres_a_partir_fila_objetivo)
               
                columna_samples = nombres_a_partir_fila_objetivo
            else:
                # Handle the case where the text is not found (no matching row)
                print(f"No se encontró la fila con el texto: {texto_fila_objetivo}")
                print("Esto es nombres_a_partor_fila_objetivo: ", nombres_a_partir_fila_objetivo)
                
                #Finalmente vacia las series.
                nombres_a_partir_fila_objetivo = pd.Series([])  # Empty Series

        #Future: Checar si éste contador está siendo usado.
        contador = 0
        cuantos = len(columna_samples)
        print("La cantidad de resultados son: ", cuantos)
        print("Y ésta es la lista total...", columna_samples)
                
        #Recorre cada URL de foto en la columna
        for i, foto_path in enumerate(columna_samples):

            print(f"Estamos en la imagen: {foto_path}, que es la número i: {i}" )
            #Future genera su ruta con la función que harás de hacer rutas, para desplegarla en consola de manera informativa.
                                
            #POSICIÓN (IMPORTANTE)
            print("Obteniendo la posición...")
            #Quiero que el 20% de las veces no use posición.
            numero_random = random.random()
            if numero_random < 0.2:
                ruta_posicion, shot = "", ""
                print("Random dice que sin posición.")
                print("Ruta posición guardo: ", ruta_posicion)
            else:
                ruta_posicion, shot = tools.getPosition()
            #Future: Checar si en realidad se usa ruta_posicion, si no, quitarlo de la función getPosition()
            
            print(f"Ruta_posicion: {ruta_posicion} y shot: {shot}...")

            clase = getattr(importlib.import_module("prompts"), configuracion.creacion)

            print("Clase quedó así: ", clase)
            creacion = clase()
            #creacion = Hotgirl(style="anime")            

            #Future Importante revisar si el prompt es meramente informativo, mientras lo dejaré comentado.
            #Creación será el objeto que contiene todos los atributos de lo que vamos a crear.
            if configuracion.creacion == "Superhero":                
                pass
                #prompt = f"A {creacion.style} of a superhero like {creacion.subject} " #Future: agregar otros atributos random aquí posteriormente.
                #Future, tener un archivo .py con prompts asociados. Sobre todo ahora que la clase entra directo.
            else:
                #PROMPT PARA CHICA
                prompt = f"A {creacion.style} of a {creacion.adjective} {creacion.type_girl} {creacion.subject} with {creacion.boobs} and {creacion.hair_style} wearing {creacion.wardrobe_top}, {creacion.wardrobe_accesories}, {creacion.wardrobe_bottom}, {creacion.wardrobe_shoes}, {creacion.situacion} at {creacion.place} {creacion.complemento}"           
            #print("Éstos son los atributos que estamos a punto de guardar en el excel...")
            #print(prompt)
            #Antes de iniciar el stablediffusion vamos a guardar nuestro registro: 
            print("Entrará a guardarRegistro cada que haya un objeto nuevo...")
            print(f"Estámos entrando con el objeto {creacion}, y la shot {shot}...")
            tools.guardarRegistro(dataframe, foto_path, creacion, shot)

    except KeyboardInterrupt:
        print("Me quedé en la foto_path: ", foto_path)
        
        # Abrir el archivo configuracion.py en modo append
        with open("configuracion.py", "a") as archivo:
            # Escribir los valores en el archivo
            archivo.write(f"\nfoto_path = '{foto_path}'\n")
        
        print("Interrumpiste el proceso, guardaré el dataframe en el excel, hasta donde ibamos.")
        print("Aquí vamos a guardar el excel porque interrumpí el proceso...")
        #IMPORTANTE: Quizá no se necesita hacer ésta escritura pq si hace la escritura final. Prueba.
        tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')
