import pandas as pd
import time
import configuracion.configuracion as configuracion
import gradio_client
import nycklar.nodes as nodes
import os
import pretools, tools
import prompter
import configuracion.globales as globales
import random
import imagesExtractors
import inspect

def obtenerArchivoOrigen(foto_path):
    """
    Obtiene el archivo original (fuente), basado en el archivo destino listado en el excel.

    Parameters:
    foto_path
    
    Returns:
    str: La ruta del archivo origen.
    """
    #foto_path = "203112-t3.webp"

    segmentos_guion = foto_path.split("-")
    cuantos_segmentos = len(segmentos_guion)
    
    #Ahora divide por el punto a ese último segmento: 
    division_puntos = segmentos_guion[cuantos_segmentos-1].split(".")
    quitable = "-" + division_puntos[0]
    resultado_final = foto_path.split(quitable)
    union_final = resultado_final[0] + resultado_final[1]

    return union_final

def preparaColumnaImagenes(dataframe, inicial):
        
        #FUTURE: Ver si ya no es necesaria ésta función.
        
        print("Entré a prepara columna imagenes..., e inicial es: ", inicial)
    
        #Va todo en un try para que podamos guardar el dataframe en un excel en caso de interrupción del ciclo:
        try: 

            # Filtra las filas donde 'Download Status' es igual a 'Success'
            df_images_ok = dataframe[dataframe['Download Status'] == 'Success']

            # Crea un dataset 'columna_imagenes' a partir de la columna 'Nombre'
            #IMPORTANTE: Aquí si debe ser 'Name' ya que solo tenemos una foto origen (aunq tengamos 4 samples).
            #columna_imagenes = df_images_ok['Name'].unique()
            columna_imagenes = df_images_ok['File']
            print("Ésta es la columna de imagenes:")
            print(columna_imagenes)
            print("El len de la columna_imagenes es: ", len(columna_imagenes))
            

            for imagen in columna_imagenes:
                 print(imagen)
                 
                 if imagen == "C4E03AQH183r1z76ATw-t4.png": #Éste es el anterior al que estamos buscando.
                      print("Atención, encontré a la candidata, ve que sigue...")
                                                      
            #Si se le pasó el valor como parámetro entonces hace la búsqueda desde donde empezará.
            if inicial is not None: 
                #PROCESO PARA INICIAR DONDE NOS QUEDAMOS
                
                # Ésta es la foto donde iniciará, que se pasa como parámetro a full Process.
                texto_fila_objetivo = inicial  # Replace with your actual search text
                print("Dentro de inicial...El archivo en el que iniciaremos es: ", inicial)
                                
                # Create a boolean mask to identify the row matching the text
                mascara_fila_objetivo = df_images_ok['File'].str.contains(texto_fila_objetivo)
                print("Ésto es máscara fila objetivo:")
                print(mascara_fila_objetivo)
                print("El len de mascara fila objetivo es: ", len(mascara_fila_objetivo))
                
                print("Ahora voy a repasar la mascara:")
                for mask in mascara_fila_objetivo:
                     print(mask)
                     print("next")
                     
                     if mask == "True":
                          print("Atención, encontré a True.")
                          
                
                # Get the index of the matching row
                indice_fila_objetivo = mascara_fila_objetivo.idxmax()  # Assumes only one match
                print("VIEW: Su índice idmax es: ", indice_fila_objetivo)                
                
                # If the text is found, get the names from that row onward
                #Para cuando llega aquí tenemos que re arreglarle el nombre.
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
            
            print("Voy a volver a repasar la nueva columna de imagenes que mide ahora: ", len(columna_imagenes))
            
            for imagen in columna_imagenes:
                 print(imagen)
                 print("siguiente")
                 if imagen == "C4E03AQH2FsbLl6arEw-t2.png":
                      print("Se encontró el resultado final por fin.")
                                             
            return columna_imagenes

        except KeyboardInterrupt:
            print("Se interrumpió la creación de la columna")

def obtenIndexRow(dataframe, deColumna, indicador):
    index = dataframe[dataframe[deColumna] == indicador].index
    return index

def creaRow(dataframe, imagen, take, filename, lista): 

    #Ready Importante, verifica si creaRow solo participa en la creación de samples. Respuesta: SI!
    #Para imagenes de Sourcelist
    #Ready:, ver si corriges que borra la URL de orígen de los takes 2,3 y 4. Listo OK!!!!
    #Future, haz prueba con más samples.
        
    dataframe.loc[len(dataframe)] = lista  #adding a row

def df2Excel(dataframe, filename):

    print("Entré al excel a guardar...")

    """
    Guarda el Dataframe final en el archivo de excel original.

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.
    filename

    Returns:
    bool: True si se guardó el archivo correctamente.
    
    """

    #IMPORTANTE: df2Excel ya siempre considerará que:
    # 1.- Está guardando el excel de resultados no el excel origen (que nunca se modificará.)
    # 2.- Ese excel siempre estará en la carpeta results_excel 

    #IMPORTANTE: Agrega que si el archivo está abierto, de tiempo para corregir y no mande a error.
     
    # Obtiene la ruta actual del script (directorio raíz del proyecto)

    #Future, df2excel actualmente asume que el excel siempre guardará el excel del directorio de resultados, arreglar...
    #... para que reciba la ruta completa.

    ruta_actual = os.path.dirname(__file__)
    print("Esto es la ruta actual: ", ruta_actual)

    ruta_excel = os.path.join(ruta_actual, globales.excel_results_path)
    print("Esto es la ruta excel: ", ruta_excel)

    # Combina la ruta actual con el nombre del archivo para obtener la ruta relativa
    ruta_archivo = os.path.join(ruta_excel, filename)
    print("Ésto es la ruta archivo: ", ruta_archivo)

    try:
        #Éste try except tiene el proposito de cachar el error de excel abierto desde dentro de df2Excel para que solo exista una vez.

        # Guarda el DataFrame con la nueva columna en el archivo Excel
        dataframe.to_excel(ruta_archivo, index=False)
    except Exception as e:
                print(e)
                print("Es probable que el archivo de excel esté abierto, ciérralo antes de proceder y oprime una tecla.")
                input("Presiona cualquier tecla para continuar: ")
                print(f"Excepción: - {e}, guardaremos el excel hasta donde iba. Reinicia el proceso, continuará donde te quedaste.")
                #FUTURE: Quitar ésto de los otros lados ya que ahora se maneja internamente.
                #¿se podrá ésta autorecursión?
                #Si se puede, pero para que continúe el proceso necesitarías aplicar el while.
                #FUTURE: Poner dicho  while...
                tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')
    return True

def carruselStable(columna_imagenes, ruta_origen, target_dir, dataframe): 
    print("Entré a carruselStable, ")
    print("El len de carrusel stable es: ", len(columna_imagenes))
    
    try:    
        #ÉSTE ES EL CLIENT CORRECTO!!!!
        #Así solo entrará al cliente una vez y no cada que de vuelta el for.
        #FUTURE, importante, aquí es donde se arranca la API cuando está dormida.
        #... hacer función que exclusivamente la despierte.
        client = gradio_client.Client("Moibe/splashmix", hf_token=nodes.splashmix_token)

        # Recorre cada URL de foto en la columna
        for i, foto_path in enumerate(columna_imagenes):

            print(f"{i} de {len(columna_imagenes)}.")  
            print(f"Imagen: {foto_path}.")

            #Obtiene la foto original que transformaremos.            
            source_photo = obtenerArchivoOrigen(foto_path)
                                                     
            #FOTO
            foto = os.path.join(ruta_origen, source_photo)
            
            #Prepara ID la imagen para gradio.        
            imagenSource = gradio_client.handle_file(foto)                      
            
            indice = tools.obtenIndexRow(dataframe, 'File', foto_path)       
                                            
            #Éste contenedor contendrá los atributos que sacó de la respectiva ROW. #Es solo un cascarón.
            contenedor = prompter.creaContenedorTemplate(dataframe, indice, configuracion.creacion) #Superhero o #Hotgirl por ahora.

            print("---")
            print("Iniciando una nueva creación...")
            print(contenedor)                         

            #AHORA CREA EL PROMPT
            print("Configuración. creación es: ", configuracion.creacion)
            prompt = prompter.creaPrompt(contenedor, configuracion.creacion)
            
            #Mini proceso para sacar la ruta de la posición. 
            #Future: Ver si lo haces función o lo combinas con getPosition. 
            #O si haces una función creadora de rutas.
            ruta_carpeta = os.path.join("imagenes", globales.positions_path)
            
            lista_archivos = os.listdir(ruta_carpeta)
            
            if not lista_archivos:
                print("La carpeta está vacía o no existe.")
                exit()
            
            imagen_posicion = contenedor['shot']
            print("Imagen_posicion es: ", imagen_posicion)
            
            try: 
                ruta_posicion = os.path.join(ruta_carpeta, imagen_posicion)
                #Solo haz el gradio de posición, si hay posición:
                imagenPosition = gradio_client.handle_file(ruta_posicion)
            except:                
                print("No hay imagen de posición, continua así...")
                ruta_posicion = ""
                imagenPosition = None
                #IMPORTANTE, Ya no se para pero no guarda registro, ni siquiera hace el SD, revisa por qué.
            #Si la row viniera todo vacío no podrá crear nada, revisa por que.
            #Future: es que debes ponerle una excepción a ruta_posición, puede venir vacía pero que no pase nada si no la forma.

            print("Ésto es el prompt obtenido de creaPrompt: ", prompt)
                            
            #STABLE DIFFUSION
            print("Iniciando Stable Difussion...")
            #Los valores ya estarán guardados en el excel, resultado solo reportará si hay imagen o no.
            resultado = tools.stableDiffuse(client, imagenSource, imagenPosition, prompt)
            print("El resultado de predict fue: ", resultado)
                        
            #Aquí cambiaremos a que también pueda regresar PAUSED, que significa que nada adicional se puede hacer.  
            if resultado == "api apagada":
                print("Me quedé en la foto_path: ", foto_path)
                
                with open("configuracion.py", "a") as archivo:
                    # Escribir los valores en el archivo
                    archivo.write(f"\n foto_path = {foto_path}\n")
                                        
                print("La api está apagada, esperando a que reinicie.")
                print("Aquí vamos a guardar el excel, porque se apago la API...")
                
                pretools.df2Excel(dataframe, configuracion.filename)
                configuracion.api_apagada = True
                #Se definirá si esperar a que reinicie o no.
                if configuracion.wait_awake == True: 
                    print("Esperando 500 segundos a que reinicie...")
                    time.sleep(configuracion.wait_time)
                    configuracion.waited = True
                    #break #Se va a donde acaba el for de 4.
                else: 
                    configuracion.waited = False
                    #break                
            else: 
                print("Se fue al else porque type(resultado) es: ", type(resultado))

            #PROCESO DESPÚES DE QUE YA TERMINÓ EL STABLE DIFUSSE:
            #SI PROCESO CORRECTAMENTE SERÁ UNA TUPLA.        
            if isinstance(resultado, tuple):
                #ES UNA TUPLA:
                print(f"IMPORTANTE: Vamos a guardar el resultado, y la ruta_final o destino es {target_dir} y es del tipo: {type(target_dir)}...")
                
                #Future: guardar Resultado ahora debe pasar el diccionario de atributos y después usarlo adentro en actualiza Row.
                print("Vamos a guardar un resultado existoso:")
                tools.guardarResultado(dataframe, resultado, foto_path, target_dir, 'Completed')

            #NO PROCESO CORRECTAMENTE NO GENERA UNA TUPLA.
            #CORRIGE IMPORTANTE: QUE NO SE SALGA DEL CICLO DE ESA IMAGEN AL ENCONTRAR ERROR.
            else:
                #NO ES UNA TUPLA:
                print("El tipo del resultado cuando no fue una tupla es: ", type(resultado))                
                texto = str(resultado)
                segmentado = texto.split('exception:')
                print("Segmentado es una posible causa de error, analiza segmentado es: ", segmentado)
                #FUTURE: Agregar que si tuvo problemas con la imagen de referencia, agregue en un 
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
                
                tools.guardarResultado(dataframe, imagenSource, foto_path, target_dir, mensaje)
                
            print("Salí del if instance...")
            #AQUÍ TERMINA EL PROCESO QUE BIEN PODRÍAMOS REPETIR 4 VECES.

            #Revisa si éste for debería tener un try-except.
            print("Salí del for de n cantidad de samples....")
            #Aquí llega el break si la API estaba apagada, habiendo esperado o no."        
            
            if configuracion.api_apagada == True:
                if configuracion.waited == True: 
                #Si estaba apagada, pero esperó, ya no hagas el segundo break.
                    configuracion.waited = False #Solo regresa a waited al estado normal. (quizá no es necesario pq no llega aquí.)
                else: 
                    #Si estaba apagada y no esperaste, salte totalmente con el segundo break...
                    print("Como el problema fue que la API estaba apagada, volveré a saltar hacia un break.")
                    #break
            # else:
            #     #Si la API no estaba apagada, éste es el camino normal.
            #     contador =+ 1
            #     #Future: CHecar si éste contador se usa.

    except KeyboardInterrupt:
        print("Me quedé en la foto_path: ", foto_path)
        
        # Abrir el archivo configuracion.py en modo append
        with open("configuracion.py", "a") as archivo:
            # Escribir los valores en el archivo
            archivo.write(f"\nfoto_path = '{foto_path}'\n")           
        
        print("Interrumpiste el proceso, guardaré el dataframe en el excel, hasta donde ibamos.")
        print("Aquí vamos a guardar el excel porque interrumpí el proceso...")
        
def getNotLoaded(dataframe, columna_filtro, texto_filtro, columna_destino, columna_source):
    #Obtiene las imagenes que no se han cargado.

    print("Estamos en la función getNotLoaded()...")
    print("El tamaño del dataframe total con el que vamos a trabajar es: ", len(dataframe))
    
    #IMPORTANTE: El dataframe lo sacará de una COLUMNA y lo filtrará con un TEXTO.
    print(f"El dataframe lo sacará de la columna: {columna_filtro} y lo filtrará con el texto: {texto_filtro}.")
    df_images_ok = dataframe[(dataframe[columna_filtro] == texto_filtro)]
    
    #Lista de las imagenes que subiremos. 
    print("El tamaño del dataframe df_images_ok es: ", len(df_images_ok))
    
    print("Ahora basado en ese filtraremos de nuevo...")
    df_images_toUpload = df_images_ok[(df_images_ok[columna_destino].isnull())]
    
    #Lista de los completados que no tienen aún una URL o sea que no es nula.      
    lista_de_files = df_images_toUpload[columna_source].tolist()
    #Lista de ya los nombres de los archivos. 
    print("El tamaño de la lista fina a imprimir es:", len(lista_de_files))
    
    return lista_de_files

def getMissing():
    print("Estoy ejecutando getMissing...")
    print("Para obtener los archivos que nos falta hacer.")
    #Obtiene todas las faltantes para el proceso de FullProcess.
    filename = configuracion.sesion + '.xlsx'
    dataframe = pd.read_excel(globales.excel_results_path + filename)
        
    # Filter rows where 'Download Status' is 'Success' and 'Diffusion Status' is empty
    #df_images_ok = dataframe[dataframe['Download Status'] == 'Success'] 
    
    df_images_ok = dataframe[(dataframe['Download Status'] == 'Success') | 
                          (dataframe['Download Status'] == 'From Archive')]
    
    #Future: ¿Agregar concurrent.base? OK!
    nan_df = df_images_ok[(df_images_ok['Diffusion Status'].isna()) | (df_images_ok['Diffusion Status'] == 'concurrent.futures._base.CancelledError')]
    print(nan_df)
    print(f"Faltan por hacer: {len(nan_df)} imágenes...")
        
    columna_imagenes = nan_df['File'].to_list()

    return columna_imagenes

def generaIDImagen(foto_url):
    #Será diferente para cada source.
    #IMPORTANTE: Éste es para imagenes de linkedin obtenidas vía Clay.

    # NOMBRANDO EL ARCHIVO
    # Define un indentificador único.
    # Esto será diferente para cada tipo de URL que se te envíe. 
    # Trata de generalizar en el futuro.

    print("Entré a genera id imagen...")
        
    #image_id = imagesExtractors.clayLinkedInV2(foto_url)
    image_id = imagesExtractors.clayLinkedIn(foto_url)
    
    
    print("El nombre de la imagen es: ", image_id)
    

    return image_id

def funcionFiltradora(dataframe, columnaAFiltrar, textoFiltro, textoFiltro2):

    #df_images_ok = dataframe[dataframe[columnaAFiltrar] == textoFiltro] 

    textoFiltro2 = None  # Inicializamos textoFiltro2 a None (opcional)

    df_images_ok = dataframe[(dataframe[columnaAFiltrar] == textoFiltro) |
                          (textoFiltro2 is not None and dataframe[columnaAFiltrar] == textoFiltro2)]
    
    #FUTURE: Agregar el doble filtro a getNotLoaded()


    print(f"La cantidad de imagenes {textoFiltro} son: {len(df_images_ok)}")

    return df_images_ok

def getPosition():
    """
    Regresa una posición del cuerpo humano para ser utilizada por el proceso de Stable Diffusion.

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.

    """
    #FUTURE: Aquí se podrá poner dinámicamente el set de posiciones en el subfolder de la carpeta posiciones.
    #Dentro de globales podemos poner subsets, después, asociarlos a determinados modelos.
    ruta_carpeta = os.path.join("imagenes", globales.positions_path)
    #FUTURE que también arrojé sin posición.

    lista_archivos = os.listdir(ruta_carpeta)
    
    if not lista_archivos:
        print("La carpeta está vacía o no existe.")
        #FUTURE: Revisa si éste éxit corta el flujo y si eso es correcto.
        exit()

    #Selecciona una imagen aleatoriamente.
    posicion_aleatoria = random.choice(lista_archivos)
    ruta_posicion = os.path.join(ruta_carpeta, posicion_aleatoria)

    print("Ruta Posición seleccionada: ", ruta_posicion)    
    nombre_archivo = os.path.basename(ruta_posicion)
    
    #shot, extension = nombre_archivo.split(".")
    #Ahora si necesitamos la extensión: 
    shot = nombre_archivo
    
    print("Posición elegida: ", shot)
        
    return ruta_posicion, shot

def guardarRegistro(dataframe, foto_dir, creacion, shot):
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
    #Future: Poner bandera para que si la celda ya tiene un valor, no lo sustituya éste proceso.
    
    print("Ya dentro de guardar registro repasaremos cada atributo de la creación:")    
    #Después cada atributo
    for nombre_atributo in dir(creacion):
        # Verificar si el nombre es un atributo real
        if not nombre_atributo.startswith("__"):
            valor_atributo = getattr(creacion, nombre_atributo)
            print(f"Atributo: {nombre_atributo}, Valor: {valor_atributo}")   
               
            #File es la columna donde busca, filename lo que está buscando, nombre_atributo la col donde guardará y valor lo que guardará.
            actualizaRow(dataframe, 'File', foto_dir, nombre_atributo, valor_atributo)

    #Y al final el shot: 
    actualizaRow(dataframe, 'File', foto_dir, 'Shot', shot)
    df2Excel(dataframe, configuracion.sesion + '.xlsx')

def actualizaRow(dataframe, index_col, indicador, receiving_col, contenido): 
    """
    Función general que recibe una columna indice y una columna receptora para actualizar la información.

    Parameters:
    archivo (str): Contenido que será agregado a esa celda.

    Returns:
    dataframe:Regresa dataframe.
    """    

    print("Entré a actualizaRow.")           
    #Recibe el dataframe, el nombre y en que columna buscará, regresa el index.
    #Aquí había un error! Indexrow debe recibir una variable en el segundo parámetro y no 'File'
    #Parámetros: dataframe, deColumna, indicador
    index = obtenIndexRow(dataframe, index_col, indicador)   
    
    # If the value exists, get the corresponding cell value
    if not index.empty:
        #print("El index se encontró...")
                
        cell_value = dataframe.loc[index[0], index_col]  # Get the value at the first matching index
        print(f"Valor de la celda que coincide: {cell_value}")        

        print("Para la revisión de Warning, valor de contenido es: ", contenido)
                       
        print(f"Voy a guardar en el index de éste indicador: {indicador} en ésta colúmna: {receiving_col}")
        #Future: Siempre y cuando esté vacía, si no, dejo lo que estaba.
        print("Estoy en actualizaRow y antes de actualizar, quiero ver que contenido tiene:")
        print("Index..... ")
        print(dataframe.loc[index, receiving_col])
        valor = dataframe.loc[index[0], receiving_col]
        print("Éste es el valor: ", valor)

        #En el caso de venir desde carruselStable siempre será Nan porque todas las encontradas tenían ese proposito.
                
        # if pd.isnull(valor):
        #     #Solo si el contenido es Nan escribirá, si no, lo dejará así.
        #     dataframe.loc[index, receiving_col] = contenido
        # else:
        #     print("Había contenido, lo deje así.")

        print("Estoy escribiendo como sucedía antes sin el pd.isnull...")
        print("Lo que escribí fue: ", contenido)
        dataframe.loc[index, receiving_col] = contenido  
       
    else:
        print("No se encontró la celda coincidente.")   

def randomNull(probabilidad, lista):

    # Generamos un número aleatorio entre 0 y 1
    numero_random = random.random()

    # Si la probabilidad es menor a 0.2 (20%), no guardamos el color
    if numero_random < probabilidad:
        result = None  #No habrá heroe.
    else:
        result = random.choice(lista)

    return result

def stableDiffuse(client, imagenSource, imagenPosition, prompt):
 
    #Hacer primer contacto con API, ésto ayudará a saber si está apagada y prenderla automáticamente.
    try:
        #Usando Moibe Splashmix
        print("Estoy adentro, donde se usaba el cliente...")
        #ÉSTE CLIENTE YA NO SE USA PORQUE SE CARGABA CADA VEZ Y CADA VEZ.
        #client = gradio_client.Client("Moibe/splashmix", hf_token=nodes.splashmix_token)


    except Exception as e:
        print("API apagada o pausada...", e)
        print("Revisar si el datafame está vivo a éstas alturas...:", )
    
        #Analiza e para definir si está apagada o pausada, cuando está pausada, no debes esperar pq nada cambiará.
        #Si e tiene la palabra PAUSED.
        print("Reiniciándola, vuelve a correr el proceso en 10 minutos.")
        print("ZZZZZZZ")
        
        #No podemos hacer break porque no es un loop.
        #Por eso hago un return para que se salga de stablediffuse.
        return "api apagada" # o regresa api pausada.
    
    #Ahora correr el proceso central de Stable Diffusion.
    try:

        print("Ahora estoy ya en el predict...")
        
        result = client.predict(
                imagenSource,
                imagenPosition,
                prompt=prompt,
                negative_prompt="(lowres, low quality, worst quality:1.2), (text:1.2), watermark, (frame:1.2), deformed, ugly, deformed eyes, blur, out of focus, blurry, deformed cat, deformed, photo, anthropomorphic cat, monochrome, pet collar, gun, weapon, 3d, drones, drone, buildings in background",
                style_name="(No style)", #ver lista en styles.txt
                num_steps=30,
                identitynet_strength_ratio=0.8,
                adapter_strength_ratio=0.8,
                pose_strength=0.4,
                canny_strength=0.4,
                depth_strength=0.4,
                controlnet_selection=["pose"], #pueden ser ['pose', 'canny', 'depth']
                guidance_scale=5,
                #seed=43,
                seed=42, #Wow deje una seed fija desde siempre, por eso con las mismas características creará lo mismo. Está bien!
                scheduler="EulerDiscreteScheduler",
                enable_LCM=False,
                enhance_face_region=True,
                api_name="/generate_image"
        )
        return result

    except Exception as e:
        print("Hubo un error, recuerda éste prompt...", e)
        print("Aquí llega cuando la imagen no existe, no cuando no se pudo procesar, revisar si eso llega al excel, la e sería: ", e)
        #No está llegando al excel, pero no es necesario porque cuando se sale llega a la línea: 364
        print("XXXXX")
                
        return e
    
def guardarResultado(dataframe, result, filename, ruta_final, message):
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
    ruta_total = ""
    ruta_absoluta = ""

    if message == "Completed":
        #ENTONCES SI HAY UNA IMAGEN QUE GUARDAR EN DISCO DURO.        
        ruta_total = os.path.join(ruta_final, filename)
        print("El resultado del SD fue exitoso, y su ruta total es/será: ", ruta_total)
        raiz_pc = os.getcwd()
        ruta_absoluta = os.path.join(raiz_pc, ruta_total)
        print("Local path:", ruta_absoluta)
                
        ruta_imagen_local = result[0] 
        #print("La ruta de gradio en result[0] es: ", ruta_imagen_local)
        
        #IMPORTANTE, GUARDANDO EN DISCO DURO.
        with open(ruta_imagen_local, "rb") as archivo_lectura:
            contenido_imagen = archivo_lectura.read()	

        with open(ruta_total, "wb") as archivo_escritura:
            archivo_escritura.write(contenido_imagen)
            print(f"Imagen guardada correctamente en: {ruta_total}")
                        
    #FUTURE: Ésto se tiene que hacer dinámicamente.

    #Después, haya o no guardado en disco duro, registrará que terminó en el excel.

    #actualiza Row actualiza una sola row.
    print("Estoy por actualizarRow y el mensaje es:", message)
    print("y su filename (índice) es: ", filename)
    
    #Sin problema ya puede actualizar el respectivo DiffusionStatus porque siempre está presente.
    #Parámetros: dataframe, index_col, indicador, receiving_col, contenido
    tools.actualizaRow(dataframe, 'File', filename, 'Diffusion Status', message)      
    tools.actualizaRow(dataframe, 'File', filename, 'File Path', ruta_absoluta)

    try: 
        tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')  
    except Exception as e:
                print("Es probable que el archivo de excel esté abierto, ciérralo antes de proceder y oprime una tecla.")
                input("Presiona cualquier tecla para continuar: ")
                print(f"Excepción: - {e}, guardaremos el excel hasta donde iba. Reinicia el proceso, continuará donde te quedaste.")
                tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')



def cicloSubidor(sftp, dataframe, resultados, carpeta_local, directorio_receptor, directorio_remoto):
    #Sube todas las imagenes que se le indican después de hacer un getNotLoaded().

    #Para el conteo de avance en subida.
    contador = 0 
    cuantos = len(resultados) #Cantidad de imagenes que hay en ésa carpeta.
    print("La cantidad de resultados son: ", cuantos)

    try:
        print("Inicia ciclo de repaso de cada imagen...")
        
        for imagen in resultados:
            
            print(f"Ahora estámos en la imagen número {contador} de {cuantos}.")                      
            print("La imagen de ésta vuelta es: ", imagen)
                        
            #Origen
            ruta_origen = os.path.join(os.getcwd(), carpeta_local, imagen)
            print(f"La RUTA_ORIGEN después del join quedó así: {ruta_origen}")
           
            #Destino
            nuevo_directorio_receptor = directorio_receptor.replace("/", "\\")
            print("Así quedó el nuevo directorio receptor: ", nuevo_directorio_receptor)
                                               
            #Crear la ruta completa del archivo remoto
            ruta_destino = directorio_receptor + "\\" + imagen
            #ruta_destino = os.path.join(nuevo_directorio_receptor, imagen) #Así se va a moibe pq no encuentra nada.
            #ruta_destino = nuevo_directorio_receptor

            ruta_destino = ruta_destino.replace("\\", "/")
           
            print(f"La RUTA_DESTINO después del join quedó así: {ruta_destino}.")
                      
            #Sube la imagen.
            print(f"La ruta origen es: {ruta_origen}.")
            print(f"La ruta destino es: {ruta_destino}.")
            
            sftp.put(ruta_origen, ruta_destino)
            print(f"¡La imagen {imagen} se ha sido subido al servidor!")
                        
            ruta_completa = directorio_remoto + '/' + imagen
            print("La ruta_completa, la que escribirá en el excel es: ")
            print(ruta_completa)
                        
            #Si se ha subído correctamente, entonces actualiza el archivo de excel.

            funcion = inspect.stack()[1].function
            print(f"Estoy dentro de la función: {funcion}")
            time.sleep(3)

            #Aquí se verifica si estamos subiendo sources o resultados y en consecuencia se actúa.            
            if funcion == "subeSources":
                #dataframe, columna indexadora, index, columna_receptora, url.
                tools.actualizaRow(dataframe, 'Name', imagen, 'Source URL', ruta_completa)
            else:
                #dataframe, columna indexadora, index, columna_receptora, url.
                tools.actualizaRow(dataframe, 'File', imagen, 'URL', ruta_completa)

            contador += 1
            print("Después de la suma el contador está en: ", contador)
            
        # Mensaje de confirmación
        return f"Archivo {ruta_origen} subido correctamente a {ruta_destino}."
    
    except Exception as e:
        # Mensaje de error
        # Creo que aquí se corre el riesgo de que si falla un archivo en subir, se corta la producción. 
        # Revisar y corregir en caso de ser necesario.
        mensaje = f"OJO: Error al subir un archivo: {e}"
        print(mensaje)
        print("Interrumpiste el proceso de subida, guardaré el dataframe en el excel, hasta donde ibamos.")
        tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')

    except KeyboardInterrupt:
        print("KEYBOARD: Interrumpiste el proceso de subida, guardaré el dataframe en el excel, hasta donde ibamos. Y aquí el excel es:", configuracion.sesion + '.xlsx')
        tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')
        
    finally: 
        print("Entré al finally del ciclo que repasa cada imagen. Guardaré el excel.")
        contador += 1
        #Si acabas el ciclo, también guarda el excel!!
        tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')