import os
import data.data_girls as data_girls
import time
import random
import pretools
import pandas as pd
import gradio_client
import servidor
import nycklar.nodes as nodes
import configuracion
from prompts import Prompt, Superhero, Hotgirl

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

    #Primero extraemos el dataframe:
    dataframe = pd.read_excel(filename)

    #Después vemos cuales son Success:

     # Filtra las filas donde 'Download Status' es igual a 'Success'
    df_images_ok = dataframe[dataframe['Download Status'] == 'Success']

    # Crea una nueva columna 'columna_imagenes' a partir de la columna 'Nombre'
    columna_imagenes = df_images_ok['Name']
    print("Esto es columna imagenes Name: ", columna_imagenes)

        #Crea un filename:

    for imagen in columna_imagenes:

        nombre, extension = imagen.split(".")
        filename = nombre + "-" + "t" + str(1) + "." + extension
        actualizaRow(dataframe, 'Name', imagen, 'File', filename)

    return dataframe

def fullProcess(sesion, dataframe, samples, inicial=None, ronda=None):

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

    #Destino
    ruta_destino = sesion + "-results"
    target_dir = os.path.join('imagenes', 'resultados', ruta_destino)

    #En caso de no existir el directorio destino, lo creará.
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    #Va todo en un try para que podamos guardar el dataframe en un excel en caso de interrupción del ciclo:
    try: 

        # Filtra las filas donde 'Download Status' es igual a 'Success'
        df_images_ok = dataframe[dataframe['Download Status'] == 'Success']

        # Crea una nueva columna 'columna_imagenes' a partir de la columna 'Nombre'
        columna_imagenes = df_images_ok['Name']
        print("Esto es columna imagenes Name: ", columna_imagenes)

        #Si se le pasó el valor como parámetro entonces hace la búsqueda desde donde empezará.
        if inicial is not None: 
            #PROCESO PARA INICIAR DONDE NOS QUEDAMOS
            
            # Ésta es la foto donde iniciará, que se pasa como parámetro a fullProcess.
            texto_fila_objetivo = inicial  # Replace with your actual search text
            print("El archivo en el que iniciaremos es: ", inicial)
            
            # Create a boolean mask to identify the row matching the text
            mascara_fila_objetivo = df_images_ok['Name'].str.contains(texto_fila_objetivo)
            # Get the index of the matching row
            indice_fila_objetivo = mascara_fila_objetivo.idxmax()  # Assumes only one match
            print("Su índice idmax es: ", indice_fila_objetivo)
            
            # If the text is found, get the names from that row onward
            if indice_fila_objetivo is not None:
                nombres_a_partir_fila_objetivo = columna_imagenes.iloc[indice_fila_objetivo:]
                print("Objetivo encontrado: ", nombres_a_partir_fila_objetivo)
                columna_imagenes = nombres_a_partir_fila_objetivo
            else:
                # Handle the case where the text is not found (no matching row)
                print(f"No se encontró la fila con el texto: {texto_fila_objetivo}")
                print("Esto es nombres_a_partor_fila_objetivo: ", nombres_a_partir_fila_objetivo)
                #Finalmente vacia las series.
                nombres_a_partir_fila_objetivo = pd.Series([])  # Empty Series

        contador = 0
        cuantos = len(columna_imagenes)
        print("La cantidad de resultados son: ", cuantos)
        
        #IMPORTANTE, A VER CREA EL CLIENTE AQUÍ, Y QUE SEA EL MISMO PARA CADA OCASIÓN
        print("Estoy entrando a éste cliente una vez...")
        #client = gradio_client.Client("Moibe/splashmix", hf_token=nodes.splashmix_token)

        # Recorre cada URL de foto en la columna
        for i, foto_path in enumerate(nombres_a_partir_fila_objetivo):

            print(f"El valor de i es: {i} y su tipo es: {type(i)}...")

            print("Por cierto, empezaré en la ronda....", ronda)
            time.sleep(3)

            #FOTO
            foto = os.path.join(ruta_origen, foto_path)
            
            #Prepara la imagen para gradio.
            imagenSource = gradio_client.handle_file(foto)
            #Poner una excepeción aquí para cuando no pudo procesar la imagen como por ejemplo por que no es una imagen.
        
            #ESTO SERÁ LO QUE AHORA QUEREMOS EJECUTAR 4 VECES:

            #La cantidad de resultados faltantes se basará en donde se quedará, o 4 si inicia.


            #Cuantos samples por foto querremos.
            cantidad_resultados = samples

            for j in range(cantidad_resultados):

                take = j + 1

                print(f"Estamos en la take número: {j} de tantos: {cantidad_resultados}")            

                #POSICIÓN
                ruta_posicion, shot = getPosition()
                print(f"Ruta_posicion: {ruta_posicion} y shot: {shot}...")
                #Prepara la posición para gradio.
                imagenPosition = gradio_client.handle_file(ruta_posicion)
                #Poner una excepeción aquí para cuando no pudo procesar la imagen como por ejemplo por que no es una imagen.        

                #Creación será el objeto que contiene todos los atributos de lo que vamos a crear.

                #PROMPT PARA CHICA
                creacion = Hotgirl(style="anime", adjective="surprised")
                prompt = f"A {creacion.style} of a {creacion.adjective} {creacion.type_girl} {creacion.subject} with {creacion.boobs} and {creacion.hair_style} wearing {creacion.wardrobe_top}, {creacion.wardrobe_accesories}, {creacion.wardrobe_bottom}, {creacion.wardrobe_shoes}, {creacion.situacion} at {creacion.place} {creacion.complemento}"           

                #PROMPT PARA HEROE
                # creacion = Superhero()
                # prompt = f"A {creacion.style} of a superhero like {creacion.subject} " #agregar otros atributos random aquí posteriormente.
                
                print(prompt)

                # #AQUÍ VAMOS A CREAR EL DATAFRAMA AHORA...
                # #Ahora aquí crearemos las columnas necesarias.
                # #Quizá no sea necesario crear las columnas ahora, que mejor la vaya creando conforme escribe!
                # dataframe = pretools.createColumns(dataframe, 4, diccionario_atributos)
                # print("Creo que la creación fue exitosa...")
                # print(dataframe)

                print("Estoy por entrar a guardar registro, el foto_path es: ", foto_path)
                time.sleep(1)

                #Antes de iniciar el stablediffusion vamos a guardar nuestro registro: 
                guardarRegistro(dataframe, foto_path, creacion, take, shot)


                #STABLE DIFFUSION
                print("Iniciando Stable Difussion...")
                #Los valores ya estarán guardados en el excel, resultado solo reportará si hay imagen o no.
                #resultado = stableDiffuse(client, imagenSource, imagenPosition, prompt, shot)

                #-->Aquí es donde llegan los breaks cuando la API estaba apagada.
                
                #Aquí cambiaremos a que también pueda regresar PAUSED, que significa que nada adicional se puede hacer.  
                if resultado == "api apagada":
                    print("Me quedé en la foto_path: ", foto_path)
                    print("Y la ronda número: ", j)
                    with open("configuracion.py", "a") as archivo:
                        # Escribir los valores en el archivo
                        archivo.write(f"\n foto_path = {foto_path}\n")
                        archivo.write(f"ronda = {j}\n")
                    
                    print("La api está apagada, esperando a que reinicie.")
                    print("Aquí vamos a guardar el excel, porque se apago la API...")
                    
                    pretools.df2Excel(dataframe, configuracion.filename)
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

                #SI PROCESO CORRECTAMENTE SERÁ UNA TUPLA.        
                if isinstance(resultado, tuple):
                    print("Es una tupla: ", resultado)
                    print(f"IMPORTANTE: Vamos a guardar el resultado, y la ruta_final o destino es {target_dir} y es del tipo: {type(target_dir)}...")
                    
                    #Future: guardar Resultado ahora debe pasar el diccionario de atributos y después usarlo adentro en actualiza Row.
                    print("Vamos a guardar un resultado existoso:")
                    time.sleep(6)
                    guardarResultado(dataframe, resultado, foto_path, take, shot, creacion.style, creacion.subject, target_dir, 'Image processed')

                #NO PROCESO CORRECTAMENTE NO GENERA UNA TUPLA.
                #CORRIGE IMPORTANTE: QUE NO SE SALGA DEL CICLO DE ESA IMAGEN AL ENCONTRAR ERROR.
                else:
                    print("No es una tupla: ", resultado)
                    print("El tipo del resultado cuando no fue una tupla es: ", type(resultado))
                    
                    texto = str(resultado)
                    segmentado = texto.split('exception:')
                    print("Segmentado es una posible causa de error, analiza segmentado es: ", segmentado)
                    ###FUTURE: Agregar que si tuvo problemas con la imagen de referencia, agregue en un 
                    #Log de errores porque ya no lo hará en el excel, porque le dará la oportunidad con otra 
                    #imagen de posición.
                    try:
                        #Lo pongo en try porque si no hay segmentado[1], suspende toda la operación. 
                        print("Segmentado[1] es: ", segmentado[1])
                        mensaje = segmentado[1]
                    except Exception as e:
                        print("Error en el segmentado: ", e)
                        mensaje = "concurrent.futures._base.CancelledError"
                    finally: 
                        pass
                    
                    print("Si no la pudo procesar, no la guarda, solo actualiza el excel.")
                    #Cuando no dio un resultado, la var resultado no sirve y mejor pasamos imagenSource, si no sirviera, ve como asignar la imagen.
                    print("Vamos a guardar un resultado no exitoso:")
                    time.sleep(5)
                    guardarResultado(dataframe, imagenSource, foto_path, take, shot, creacion.style, creacion.subject, target_dir, mensaje)
                    
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
    except KeyboardInterrupt:
        print("Me quedé en la foto_path: ", foto_path)
        print("Y la ronda número: ", j)
        # Abrir el archivo configuracion.py en modo append
        with open("configuracion.py", "a") as archivo:
            # Escribir los valores en el archivo
            archivo.write(f"foto_path = '{foto_path}'\n")
            archivo.write(f"ronda = {j}\n")
        
        print("Interrumpiste el proceso, guardaré el dataframe en el excel, hasta donde ibamos.")
        print("Aquí vamos a guardar el excel porque interrumpí el proceso...")
        #IMPORTANTE: Quizá no se necesita hacer ésta escritura pq si hace la escritura final. Prueba.
        #pretools.df2Excel(dataframe, configuracion.filename)

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


def stableDiffuse(client, imagenSource, imagenPosition, prompt, shot):

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

        #Usando Moibe Splashmix
        print("Estoy adentro, donde se usaba el cliente...")
        # client = gradio_client.Client("Moibe/splashmix", hf_token=nodes.splashmix_token)

        #Usando Moibe InstantID
        #client = gradio_client.Client("Moibe/InstantID", hf_token=nodes.splashmix_token)

        #Usando original
        #client = gradio_client.Client("InstantX/InstantID")

        #Usando recién clonado.
        #client = gradio_client.Client("Moibe/superheroes", hf_token=nodes.splashmix_token)


    except Exception as e:
        print("API apagada o pausada...", e)
        print("Revisar si el datafame está vivo a éstas alturas...:", )
    
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

        print("Ahora estoy ya en el predict...")
        time.sleep(1)
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

def guardarRegistro(dataframe, foto_dir, creacion, take, shot):

    """
    Guarda el registro de lo que se va a hacer en excel.

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.
    result
    foto_dir
    take
    shot
    estilo
    ruta_final
    message: el mensaje textual que irá en la columna stable diffusion: si fue error el error, si no: Image Processed.

    Returns:
    bool: True si se guardó el archivo correctamente.
    """


    #Primero agrega la take:
    actualizaRow(dataframe, 'Name', foto_dir, 'Take', take)

    #Después cada atributo
    for nombre_atributo in dir(creacion):
        # Verificar si el nombre es un atributo real
        if not nombre_atributo.startswith("__"):
            valor_atributo = getattr(creacion, nombre_atributo)
            print(f"Atributo: {nombre_atributo}, Valor: {valor_atributo}")
            actualizaRow(dataframe, 'Name', foto_dir, nombre_atributo, valor_atributo)

    #Y al final el shot: 
    actualizaRow(dataframe, 'Name', foto_dir, 'Shot', shot)

    #Es esto la línea universal para guardar el excel? = Si, si lo es :) 
    pretools.df2Excel(dataframe, configuracion.filename)

    print("Me detuve porque terminé, deténme...")
    time.sleep(29)
    


    
def guardarResultado(dataframe, result, foto_dir, take, shot, style, subject, ruta_final, message):

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
    message: el mensaje textual que irá en la columna stable diffusion: si fue error el error, si no: Image Processed.

    Returns:
    bool: True si se guardó el archivo correctamente.
    """
    
    #Aquí guardará la imagen.
    #Ésta parte solo debe hacerla si no viene de error. 

    print("HOY: Estamos en guardar Resultado, y el mensaje que recibimos como parámetro es: ", message)

    if message == "Image processed":

        #Crear el nombre que tendrá el archivo.
        #Quieres todo lo que va antes del punto de la extensión.
        #Ve si existe otra forma de separar la extensión, más específica, porque esto se presta a errores si el archivo tuviera punto en su nombre.
        profile_split = foto_dir.split('.')
        nombre_sin_extension = profile_split[0]
        #nombre_archivo = nombre_sin_extension + "-Take=" + str(take) + "-Shot=" + shot + "-Style=" + style + "-Subject=" + subject + ".png"
        #Ahora ya se hará nombre corto pq las características están en el excel: 
        nombre_archivo = nombre_sin_extension + "-Take" + str(take) + ".png"
        ruta_total = os.path.join(ruta_final, nombre_archivo)

        ruta_imagen_local = result[0]  

        with open(ruta_imagen_local, "rb") as archivo_lectura:
            contenido_imagen = archivo_lectura.read()	

        with open(ruta_total, "wb") as archivo_escritura:
            archivo_escritura.write(contenido_imagen)
            print(f"Imagen guardada correctamente en: {ruta_total}")
            print("Estamos por actualizar excel...")
            #actualizaExcel(dataframe, 'C4D03AQEi0TQ389Qscw.png')
            #Diffusion Status (Se agrega + str(take) al nombre de cada columna para distinguirlas y ordenarlas.)

    #FUTURE: Ésto se tiene que hacer dinámicamente.


    #actualiza Row actualiza una sola row.
    print("Estoy por actualizarRow y el mensaje es:", message)
    print("y su foto_dir (índice) es: ", foto_dir)
    print("Y la take es es: ", take)
    time.sleep(3)
    #Sin problema ya puede actualizar el respectivo DiffusionStatus porque siempre está presente.
    actualizaRow(dataframe, 'Name', foto_dir, 'DiffusionStatus' + str(take), message)

    #La cosa es actualizar los valores dinámicos.
    columnas = ["Take", "Shot", "Style", "Hero"]

    for columna in columnas:
        print("Hola, de la lista de atributos estoy en la columna/atributo: ", columna)
        print("Lo voy a actualizar.")
        actualizaRow(dataframe, 'Name', foto_dir, columna + str(take), shot)
   
    # #Take
    # actualizaRow(dataframe, 'Name', foto_dir, 'Take' + str(take), take)
    # #Shot
    # actualizaRow(dataframe, 'Name', foto_dir, 'Shot' + str(take), shot)
    # #Style
    # actualizaRow(dataframe, 'Name', foto_dir, 'Style' + str(take), style)
    # #Hero
    # actualizaRow(dataframe, 'Name', foto_dir, 'Hero' + str(take), subject)


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
    print("El nombre de la imagen buscada es: ", imagen)
    index = dataframe[dataframe[index_col] == imagen].index
    print("Esto es index: ", index)
    print("Y la receiving_col es: ", receiving_col)
        
    # If the value exists, get the corresponding cell value
    if not index.empty:
        print("El index no estuvo empty...")
        
        cell_value = dataframe.loc[index[0], index_col]  # Get the value at the first matching index
        print(f"Valor de la celda que coincide: {cell_value}")
        

        print("Para la revisión de Warning, valor de contenido es: ", contenido)
        print("y tipo de contenido es: ", type(contenido))
                       
        dataframe.loc[index, receiving_col] = contenido
        #dataframe.loc['last', receiving_col] = contenido
       
    else:
        print("No se encontró la celda coincidente.")        

def subirTodo(dataframe, sesion, foto_complete_url_dir):

    print("Entramos a subir todo, la sesión es: ", sesion)

    #Conexión al servidor.
    ssh, sftp = servidor.conecta()
        
    #Define ruta de la carpeta remota
    carpeta_remota = nodes.avaimentekijä
    print(f"La carpeta remota es: {carpeta_remota} y su tipo es: {type(carpeta_remota)}.")
    directorio_receptor = carpeta_remota + sesion
    print(f"El directorio receptor será entonces: {directorio_receptor} y su tipo es: {type(directorio_receptor)}")
    
    #Define ruta de la carpeta local donde se encuentran los resultados.
    carpeta_local = 'imagenes\\resultados\\' + sesion + '-results'

    #Subir el resultado al servidor y esperar respuesta que se guardará en la var resultado.
    resultado = servidor.sube(sftp, dataframe, carpeta_local, directorio_receptor, foto_complete_url_dir)
    #Checar si aquí tendría que regresar el dataframe para tener sus modificaciones.
    print(resultado)

    servidor.cierraConexion(ssh, sftp)

    return dataframe