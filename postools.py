import os
import data
import time
import random
import pandas as pd
import gradio_client
import servidor
import nycklar.nodes as nodes
import configuracion

def creaDirectorioResults(sesion):
    """
    Crea el directorio donde se recibirán los resultados en caso de no existir. El directorio llevará el nombre de la sesión + "results".

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.

    """
    results_dir = os.path.join('imagenes', 'fuentes', 'resultados', sesion + "-results" )   
    
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

def preparaDataframe(filename):

    df = pd.read_excel(filename)

    return df

def fullProcess(sesion, dataframe):

    """
    Ciclo completo de toma de imagen, llevado a HF, guardado en disco y actualización de archivo de Excel.

    Parameters:
    sesion
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.
    """
    #Origen
    ruta_origen = os.path.join('imagenes', 'fuentes', sesion)
    ruta_destino = sesion + "-results"

    #Destino
    target_dir = os.path.join('imagenes', 'resultados', ruta_destino)
    print("This is the target: ", target_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Filtra las filas donde 'Download Status' es igual a 'Success'
    # Son las imagenes con las que trabajaremos.
    df_images_ok = dataframe[dataframe['Download Status'] == 'Success']

    # Crea una nueva columna 'columna_imagenes' a partir de la columna 'Nombre'
    columna_imagenes = df_images_ok['Name']

    contador = 0
    cuantos = len(columna_imagenes)
    print("La cantidad de resultados son: ", cuantos)

    # Recorre cada URL de foto en la columna
    for i, foto_path in enumerate(columna_imagenes):

        #FOTO
        foto = os.path.join(ruta_origen, foto_path)
        
        #Prepara la imagen para gradio.
        imagenSource = gradio_client.handle_file(foto)
        #Poner una excepeción aquí para cuando no pudo procesar la imagen como por ejemplo por que no es una imagen.
       
        #ESTO SERÁ LO QUE AHORA QUEREMOS EJECUTAR 4 VECES:

        #Cuantos samples por foto querremos.
        cantidad_resultados = 4

        for j in range(cantidad_resultados):

            take = j + 1

            print(f"Estamos en la take número: {j} de tantos: {cantidad_resultados}")            

            #POSICIÓN
            ruta_posicion, shot = getPosition()
            print(f"Ruta_posicion: {ruta_posicion} y shot: {shot}...")
            #Prepara la posición para gradio.
            imagenPosition = gradio_client.handle_file(ruta_posicion)
            #Poner una excepeción aquí para cuando no pudo procesar la imagen como por ejemplo por que no es una imagen.        

            #PROMPT
            lista_estilos = data.lista_estilos
            lista_subjects = data.lista_subjects
            style = random.choice(lista_estilos)
            subject = random.choice(lista_subjects)
            prompt = f"A {style} of a superhero like {subject} " #agregar otros atributos random aquí posteriormente.
            print("Building prompt: ", prompt)


            #STABLE DIFFUSION
            print("Iniciando Stable Difussion...")
            resultado = stableDiffuse(imagenSource, imagenPosition, prompt, shot)

            #-->Aquí es donde llegan los breaks cuando la API estaba apagada.
            
            #Aquí cambiaremos a que también pueda regresar PAUSED, que significa que nada adicional se puede hacer.  
            if resultado == "api apagada":
                print("La api está apagada, esperando a que reinicie.")
                configuracion.api_apagada = True
                #Se definirá si esperar a que reinicie o no.
                if configuracion.wait_awake == True: 
                    print("Esperando 500 segundos a que reinicie...")
                    time.sleep(configuracion.wait_time)
                    configuracion.waited = True
                    break #Se va a donde acaba el for de 4.
                else: 
                    time.sleep(1)
                    configuracion.waited = False
                    break                
            else: 
                print("Se fue al else porque type(resultado) es: ", type(resultado))

            time.sleep(2)
           
            #SI PROCESO CORRECTAMENTE SERÁ UNA TUPLA.        
            if isinstance(resultado, tuple):
                print("Es una tupla: ", resultado)
                print("Vamos a guardar el resultado, y la ruta_final o destino es: ", target_dir)
                guardarResultado(dataframe, resultado, foto_path, take, shot, style, subject, target_dir)

            #NO PROCESO CORRECTAMENTE NO GENERA UNA TUPLA.
            else:
                print("No es una tupla: ", resultado)
                print("El tipo del resultado cuando no fue una tupla es: ", type(resultado))
                time.sleep(3)
                texto = str(resultado)
                segmentado = texto.split('exception:')
                print("Segmentado[1] es: ", segmentado[1])
                
                print("Si no la pudo procesar, no la guarda, solo actualiza el excel.")
                actualizaRow(dataframe, 'Name', foto_path, 'Diffusion Status', segmentado[1])
                #Aquí haremos un break porque no tiene caso intentarlo 4 veces. 
                break
                
            print("Salí del if instance...")

            #AQUÍ TERMINA EL PROCESO QUE BIEN PODRÍAMOS REPETIR 4 VECES.

        #Revisa si éste for debería tener un try-except.
        print("Salí del for de 4....")
        #Aquí llega el break si la API estaba apagada, habiendo esperado o no."        
        
        if configuracion.api_apagada == True:
            if configuracion.waited == True: 
            #Si estaba apagada, pero esperó, ya no hagas el segundo break.
                configuracion.waited = False #Solo regresa a waited al estado normal. (quizá no es necesario pq no llega aquí.)
            else: 
                #Si estaba apagada y no esperaste, salte totalmente con el segundo break...
                print("Como el problema fue que la API estaba apagada, volveré a saltar hacia un break.")
                break
        else:
            #Si la API no estaba apagada, éste es el camino normal.
            contador =+ 1
        
def getPosition():

    """
    Regresa una posición del cuerpo humano para ser utilizada por el proceso de Stable Diffusion.

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.

    """

    ruta_carpeta = os.path.join("imagenes", "posiciones")
    #ruta_carpeta = "imagenes\\posiciones"

    lista_archivos = os.listdir(ruta_carpeta)
    
    if not lista_archivos:
        print("La carpeta está vacía o no existe.")
        exit()

    #Selecciona una imagen aleatoriamente.
    imagen_aleatoria = random.choice(lista_archivos)
    posicion_actual = os.path.join(ruta_carpeta, imagen_aleatoria)

    nombre_archivo = os.path.basename(posicion_actual)
    shot, extension = nombre_archivo.split(".")
    print("Posición elegida: ", shot)
    
    return posicion_actual, shot

def stableDiffuse(imagenSource, imagenPosition, prompt, shot):

    """
    Stable Diffusion directo en HF.

    Parameters:
    imagenSource
    imagenPosition
    prompt
    shot

    Returns:
    bool: True si se guardó el archivo correctamente.
    """
    #Los dos iguales.
    #Revisar si se puede subir el hf_token.

    #Hacer primer contacto con API, ésto ayudará a saber si está apagada y prenderla automáticamente.
    try: 

        client = gradio_client.Client("Moibe/splashmix", hf_token=nodes.splashmix_token)

    except Exception as e:
        print("API apagada o pausada...", e)
        #Analiza e para definir si está apagada o pausada, cuando está pausada, no debes esperar pq nada cambiará.
        #Si e tiene la palabra PAUSED.
        print("Reiniciandola, vuelve a correr el proceso en 10 minutos.")
        print("ZZZZZZZ")
        print("ZZZZZZZ")
        print("ZZZZZZZ")
        #No podemos hacer break porque no es un loop.
        #Por eso hago un return para que se salga de stablediffuse.
        return "api apagada" # o regresa api pausada.



    
    #Ahora correr el proceso central de Stable Diffusion.
    try:

        result = client.predict(
                imagenSource,
                imagenPosition,
                prompt=prompt,
                negative_prompt="(lowres, low quality, worst quality:1.2), (text:1.2), watermark, (frame:1.2), deformed, ugly, deformed eyes, blur, out of focus, blurry, deformed cat, deformed, photo, anthropomorphic cat, monochrome, pet collar, gun, weapon, blue, 3d, drones, drone, buildings in background, green",
                style_name="(No style)", #ver lista en styles.txt
                num_steps=30,
                identitynet_strength_ratio=0.8,
                adapter_strength_ratio=0.8,
                pose_strength=0.4,
                canny_strength=0.4,
                depth_strength=0.4,
                controlnet_selection=["pose"], #pueden ser ['pose', 'canny', 'depth']
                guidance_scale=5,
                seed=42,
                scheduler="EulerDiscreteScheduler",
                enable_LCM=False,
                enhance_face_region=True,
                api_name="/generate_image"
        )
        return result

    except Exception as e:
        print("Hubo un error, recuerda éste prompt...", e)
        print("Aquí llega cuando la imagen no existe, no cuando no se pudo procesar, revisar si eso llega al excel, la e sería: ", e)
        print(f"La imagen era: {imagenSource}, la posición era {shot}")
        print("XXXXX")
        print("XXXXX")
        print("XXXXX")
        print("XXXXX")
        return e
    
def guardarResultado(dataframe, result, foto_dir, take, shot, style, subject, ruta_final):

    """
    Guarda el resultado con una nomenclatura específica. Y lo guarda en disco.

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.
    result
    foto_dir
    take
    shot
    estilo
    ruta_final

    Returns:
    bool: True si se guardó el archivo correctamente.
    """
    
    profile_split = foto_dir.split('.')
    nombre_sin_extension = profile_split[0]
    nombre_archivo = nombre_sin_extension + "-Take=" + str(take) + "-Shot=" + shot + "-Style=" + style + "-Subject=" + subject + ".png"
    ruta_total = os.path.join(ruta_final, nombre_archivo)
           
    ruta_imagen_local = result[0]  

    with open(ruta_imagen_local, "rb") as archivo_lectura:
        contenido_imagen = archivo_lectura.read()	

    with open(ruta_total, "wb") as archivo_escritura:
        archivo_escritura.write(contenido_imagen)
        print(f"Imagen guardada correctamente en: {ruta_total}")
        print("Estamos por actualizar excel...")
        #actualizaExcel(dataframe, 'C4D03AQEi0TQ389Qscw.png')
        #Diffusion Status (Se agrega + 'take' al nombre de cada columna para distinguirlas y ordenarlas.)

        actualizaRow(dataframe, 'Name', foto_dir, 'Diffusion Status', 'Image processed')
        #Take
        actualizaRow(dataframe, 'Name', foto_dir, 'Take' + str(take), take)
        #Shot
        actualizaRow(dataframe, 'Name', foto_dir, 'Shot' + str(take), shot)
        #Style
        actualizaRow(dataframe, 'Name', foto_dir, 'Style' + str(take), style)
        #Hero
        actualizaRow(dataframe, 'Name', foto_dir, 'Hero' + str(take), style)


def actualizaRow(dataframe, index_col, imagen, receiving_col, contenido): 
    """
    Función general que recibe una columna indice y una columna receptora para actualizar la información.

    Parameters:
    archivo (str): Contenido que será agregado a esa celda.

    Returns:
    dataframe:Regresa dataframe.
    """
    # Find the index of the row where the 'Nombre' column value matches 'C4D03AQEi0TQ389Qscw.png'
    # Por lo tanto index_col = 'Nombre'
    #index_col = 'Nombre'
    #receiving_col = 'Diffusion Status'
    
    print("Estamos en actualizaRow...")
    print("El nombre de la imagen es: ", imagen)
    index = dataframe[dataframe[index_col] == imagen].index
    print("Esto es index: ", index)
    
    # If the value exists, get the corresponding cell value
    if not index.empty:
        print("El index no estuvo empty...")
        
        cell_value = dataframe.loc[index[0], index_col]  # Get the value at the first matching index
        print("Para la revisión de Warning, valor de contenido es: ", contenido)
        print("y tipo de contenido es: ", type(contenido))
        print(f"Valor de la celda que coincide: {cell_value}")
        print("-------")
        print("-------")
        print("-------")
        dataframe.loc[index, receiving_col] = contenido
       
    else:
        print("No se encontró la celda coincidente.")        

def subirTodo(dataframe, sesion, foto_complete_url):

    print("Entramos a subir todo, la sesión es: ", sesion) 

    #Conexión al servidor.
    ssh, sftp = servidor.conecta()
        
    #Define ruta de la carpeta remota
    carpeta_remota = nodes.avaimentekijä
    print(f"La carpeta remota es: {carpeta_remota} y su tipo es: {type(carpeta_remota)}.")
    directorio_receptor = carpeta_remota + sesion
    print(f"El directorio receptor será entonces: {directorio_receptor} y su tipo es: {type(directorio_receptor)}")
    
    #Define ruta de la carpeta local.
    carpeta_local = 'imagenes\\resultados\\' + sesion + '-results'


    resultado = servidor.sube(sftp, dataframe, carpeta_local, directorio_receptor, foto_complete_url)
    #Checar si aquí tendría que regresar el dataframe para tener sus modificaciones.
    print(resultado)

    servidor.cierraConexion(ssh, sftp)

    return dataframe