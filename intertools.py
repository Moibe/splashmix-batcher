import os
import time
import pretools
import pandas as pd
import nycklar.nodes as nodes
import configuracion.configuracion as configuracion
from objetosCreacion import Prompt, Superhero, Hotgirl
import tools
import configuracion.globales as globales
import importlib
import data.prompts

def sampler(sesion, inicial=None):

    #Auxiliar para archivo excel de resultados.
    #La ruta sirve con diagonal normal / o con doble diagonal \\
    dataframe = pd.read_excel(globales.excel_results_path + sesion + '.xlsx')

    #IMPORTANTE, Asigna los atributos a cada sample.
    
    #Destino donde irán las imágenes resultantes.
    ruta_destino = sesion + "-results"
    target_dir = os.path.join('imagenes', 'resultados', ruta_destino)

    #En caso de no existir el directorio donde se recibirán las imagenes destino, lo creará.
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    #Va todo en un try para que podamos guardar el dataframe en un excel en caso de interrupción del ciclo:
    try:

        #Filtra las filas donde 'Download Status' es igual a 'Success'
        #Importante: O para ésta caso especial, solamente los 'From Archive' no todos!
        df_images_ok = tools.funcionFiltradora(dataframe, 'Download Status', 'Success', 'From Archive')

        #Future haz una función creadora de Columnas.
        # Crea un dataset 'columna_imagenes' a partir de la columna que contiene el nombre del archivo individual.
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
            #IMPORTANTE: Se quitará de momento el no usar posición, porque se concluyó que siempre es necesaria.
            #Se deja comentada, para otros casos de uso.
            ###
            # numero_random = random.random()
            # #La probabilidad de que no usemos imagen de posición se designa desde globales, ahora es 0.1
            # if numero_random < globales.prob_position:
            #     ruta_posicion, shot = "", ""
            #     print("Random dice que sin posición.")
            #     print("Ruta posición guardo: ", ruta_posicion)
            # else:
            #     ruta_posicion, shot = tools.getPosition()
            #Future: Checar si en realidad se usa ruta_posicion, si no, quitarlo de la función get Position()
            
            ruta_posicion, shot = tools.getPosition()
            
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
                #Future: Creo que ya no se usará la variable prompt.
                prompt = f"A {creacion.style} of a {creacion.adjective} {creacion.type_girl} {creacion.subject} with {creacion.boobs} and {creacion.hair_style} wearing {creacion.wardrobe_top}, {creacion.wardrobe_accesories}, {creacion.wardrobe_bottom}, {creacion.wardrobe_shoes}, {creacion.situacion} at {creacion.place} {creacion.complemento}"           
            
            print("Entrará a guardarRegistro cada que haya un objeto nuevo...")
            print(f"Estámos entrando con el objeto {creacion}, y la shot {shot}...")
            tools.guardarRegistro(dataframe, foto_path, creacion, shot)

    except KeyboardInterrupt:
        print("Me quedé en la foto_path: ", foto_path)
        
        #Estoy quitando ésto porque ya no necesitamos guardar el nombre del archivo en el que vamos en config.
        # # Abrir el archivo configuracion.py en modo append
        # with open("configuracion.py", "a") as archivo:
        #     # Escribir los valores en el archivo
        #     archivo.write(f"\nfoto_path = '{foto_path}'\n")
        
        print("Interrumpiste el proceso, guardaré el dataframe en el excel, hasta donde ibamos.")
        print("Aquí vamos a guardar el excel porque interrumpí el proceso...")
        #IMPORTANTE: Quizá no se necesita hacer ésta escritura pq si hace la escritura final. Prueba.
        tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')


#Future, creo que Samples es irrelevante, checas.
def fullProcess(sesion):
    """
    Ciclo completo de toma de imagen, llevado a HF, guardado en disco y actualización de archivo de Excel.

    Parameters:
    sesion
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.
    """
    dataframe = pd.read_excel(globales.excel_results_path + sesion + '.xlsx')

    #FUTURE: Incluir espera por excel abierto también aquí. OK!!!
    #Future, que el proceso detecte si no hay internet para no quedarse ciclado.

    #FUTURE: Ruta origen y destino que vengan de globales.
    #Origen
    ruta_origen = os.path.join('imagenes', 'fuentes', sesion)
    #Destino
    ruta_destino = sesion + "-results"
    target_dir = os.path.join('imagenes', 'resultados', ruta_destino)

    #En caso de no existir el directorio destino, lo creará.
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # columna_imagenes = tools.preparaColumnaImagenes(dataframe, inicial)
    # print("Ya estoy de nuevo afuera, Tengo el resultado de columna_imagenes, que es:")
    # print(columna_imagenes)

    #Count Missing también devuelve una columna de imagenes, pero basada en las que no han sido procesadas.
    #Dejando fuera a las completadas y a las que tuvieron error. Ésto evita tener que hacer el proceso de preparar...
    #...columnas basado en el archivo donde se quedó. Simplemente hará todas aquellas que no se han procesado!
    columna_imagenes = tools.getMissing() 

    #El carrusel ya entra con las columnas especificas con las que va a trabajar.
    #Future: Analizar los Neg Prompt del programa, si te son útiles, si son útiles y/o si se deben editar.
    tools.carruselStable(columna_imagenes, ruta_origen, target_dir, dataframe)