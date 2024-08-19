import pandas as pd
import time
import configuracion
import gradio_client
import nycklar.nodes as nodes
import os
import pretools, postools
import prompter
import globales

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
    # print(f"Hay {cuantos_segmentos} en segmentos_guion de la foto {foto_path}")

    # print(f"Presentando el último segmento: {segmentos_guion[cuantos_segmentos-1]}.")

    #Ahora divide por el punto a ese último segmento: 

    division_puntos = segmentos_guion[cuantos_segmentos-1].split(".")

    # print(f"Al que estoy buscando es a éste, el primer segmento: {division_puntos[0]} ")

    quitable = "-" + division_puntos[0]

    resultado_final = foto_path.split(quitable)

    union_final = resultado_final[0] + resultado_final[1]

    print(f"El resultado final es: {union_final} ")

    return union_final

def preparaColumnaImagenes(dataframe, inicial):
        
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

    print("Estoy en obtenIndexRow...")
       
    index = dataframe[dataframe[deColumna] == indicador].index
    print("Esto es index, es lo que voy a regresar: ", index)
    print("y ésto es el tipo de index: ", type(index))

    return index

def creaRow(dataframe, imagen, take, filename, lista): 

    #Importante, verifica si creaRow solo participa en la creación de samples.   
    
    #Para imagenes de Sourcelist
    #Future, ver si corriges que borra la URL de orígen de los takes 2,3 y 4.
    #Future, haz prueba con más samples.
        
    dataframe.loc[len(dataframe)] = lista  #adding a row

def df2Excel(dataframe, filename):

    print("182: Entré al excel a guardar...")

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

    #Future que si está abierto el excel no arruine el flujo y de tiempo para cerrarlo.

    #IMPORTANTE: Agrega que si el archivo está abierto, de tiempo para corregir y no mande a error.
     
    # Obtiene la ruta actual del script (directorio raíz del proyecto)
    ruta_actual = os.path.dirname(__file__)
    print("Esto es la ruta actual: ", ruta_actual)

    ruta_excel = os.path.join(ruta_actual, globales.excel_results_path)
    print("Esto es la ruta excel: ", ruta_excel)

    # Combina la ruta actual con el nombre del archivo para obtener la ruta relativa
    ruta_archivo = os.path.join(ruta_excel, filename)
    print("Ésto es la ruta archivo: ", ruta_archivo)

    # Guarda el DataFrame con la nueva columna en el archivo Excel
    dataframe.to_excel(ruta_archivo, index=False)

    return True

def carruselStable(columna_imagenes, ruta_origen, target_dir, dataframe): 
     #Try para stablediff...
    try:    
        #ÉSTE ES EL CLIENT CORRECTO!!!!
        #Así solo entrará al cliente una vez y no cada que de vuelta el for.
        client = gradio_client.Client("Moibe/splashmix", hf_token=nodes.splashmix_token)

        # Recorre cada URL de foto en la columna
        for i, foto_path in enumerate(columna_imagenes):

            print(f"El valor de i es: {i} y su tipo es: {type(i)}...")  
            print(f"VIEW: La primer foto con la que estaremos trabajando será: {foto_path} y su tipo es: {type(foto_path)}...")
                        
            #Aquí debes darle la correcta original (2.jpg), y no la incorrecta (2-t1.jpg)
            #Como el archivo podría tener otros guiones, el que nos interesa a nosotros es
            source_photo = obtenerArchivoOrigen(foto_path)
            print(f"La source_photo que obtuvimos es: {source_photo} y su tipo es: {type(source_photo)}...")
                                         
            #FOTO
            foto = os.path.join(ruta_origen, source_photo)
            print("La ruta de Foto quedó despues de obtener su original como: ", foto)
            
        
            #Prepara ID la imagen para gradio.        
            imagenSource = gradio_client.handle_file(foto)                      
            
            indice = postools.obtenIndexRow(dataframe, 'File', foto_path) 
            print(f"El índice de foto_path: {foto_path} la row u objeto de donde sacaremos los atributos es: ", indice)
            
                                            
            #Éste contenedor contendrá los atributos que sacó de la respectiva ROW.
            #Es solo un cascarón.
            contenedor = prompter.creaContenedorTemplate(dataframe, indice, configuracion.creacion) #Superhero o #Hotgirl por ahora.

            print("Esto es el contenedor que me regreso...>")
            print(contenedor)                         

            #AHORA CREA EL PROMPT
            print("Creando prompt después de meterle el contenedor...")
            print("El contenedor es: ", contenedor)
            print("Configuración. creación es: ", configuracion.creacion)
            prompt = prompter.creaPrompt(contenedor, configuracion.creacion)
            
            #Mini proceso para sacar la ruta de la posición. 
            #Future: Ver si lo haces función o lo combinas con getPosition. 
            #O si haces una función creadora de rutas.
            ruta_carpeta = os.path.join("imagenes", "positions\\posiciones")
            #ruta_carpeta = "imagenes\\posiciones"

            lista_archivos = os.listdir(ruta_carpeta)
            
            if not lista_archivos:
                print("La carpeta está vacía o no existe.")
                exit()
            
            imagen_posicion = contenedor['shot']
            try: 
                ruta_posicion = os.path.join(ruta_carpeta, imagen_posicion)
            except:
                print("No hay imagen de posición, continua así...")
                ruta_posicion = ""
                #IMPORTANTE, Ya no se para pero no guarda registro, ni siquiera hace el SD, revisa por qué.
            #Si la row viniera todo vacío no podrá crear nada, revisa por que.
            #Future: es que debes ponerle una excepción a ruta_posición, puede venir vacía pero que no pase nada si no la forma.

            print("Ésta es la ruta_posicion que se meterá al cliente de gradio, verifica si es correcta:", ruta_posicion)
                                                    
            imagenPosition = gradio_client.handle_file(ruta_posicion)
            #Poner una excepeción aquí para cuando no pudo procesar la imagen como por ejemplo por que no es una imagen.

            print("Ésto es el prompt obtenido de creaPrompt: ", prompt)
                            
            print("LISTO PARA STABLE DIFFUSION!!!!!") 
            
            #STABLE DIFFUSION
            print("Iniciando Stable Difussion...")
            #Los valores ya estarán guardados en el excel, resultado solo reportará si hay imagen o no.
            resultado = postools.stableDiffuse(client, imagenSource, imagenPosition, prompt)
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
                print("Es una tupla: ", resultado)
                print(f"IMPORTANTE: Vamos a guardar el resultado, y la ruta_final o destino es {target_dir} y es del tipo: {type(target_dir)}...")
                
                #Future: guardar Resultado ahora debe pasar el diccionario de atributos y después usarlo adentro en actualiza Row.
                print("Vamos a guardar un resultado existoso:")
                postools.guardarResultado(dataframe, resultado, foto_path, target_dir, 'Completed')

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
                
                postools.guardarResultado(dataframe, imagenSource, foto_path, target_dir, mensaje)
                
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
                    #break
            else:
                #Si la API no estaba apagada, éste es el camino normal.
                contador =+ 1
    except KeyboardInterrupt:
        print("Me quedé en la foto_path: ", foto_path)
        
        # Abrir el archivo configuracion.py en modo append
        with open("configuracion.py", "a") as archivo:
            # Escribir los valores en el archivo
            archivo.write(f"\nfoto_path = '{foto_path}'\n")           
        
        print("Interrumpiste el proceso, guardaré el dataframe en el excel, hasta donde ibamos.")
        print("Aquí vamos a guardar el excel porque interrumpí el proceso...")
        
def getNotLoaded(dataframe):

    print("Estamos en la función getNotLoaded()...")
    print("EL tamaño del dataframe total con el que vamos a trabajar es: ", len(dataframe))
    time.sleep(3)  
    
    df_images_ok = dataframe[(dataframe['Diffusion Status'] == 'Completed')]
    print("El tamaño del dataframe df_images_ok es: ", len(df_images_ok))
    time.sleep(3)

    print("Ahora basado en ese filtraremos de nuevo...")
    df_images_toUpload = df_images_ok[(df_images_ok['URL'].isnull())]
    print("Y su tamaño es de df_images_toUpload es: ", len(df_images_toUpload) )
    time.sleep(3)

    lista_de_files = df_images_toUpload['File'].tolist()
    print("El tamaño de la lista fina a imprimir es:", len(lista_de_files))

    return lista_de_files

def getMissing():    

    filename = configuracion.filename

    dataframe = pd.read_excel('results_excel/' + filename)

    print("Tamaño del dataframe: ", len(dataframe))
    time.sleep(1)
    
    # Filter rows where 'Download Status' is 'Success' and 'Diffusion Status' is empty
    df_images_ok = dataframe[dataframe['Download Status'] == 'Success'] 
    #df_images_ok = dataframe[dataframe['Download Status'] == 'Success']

    # Print the filtered DataFrame
    print(df_images_ok)
    print(len(df_images_ok))

    nan_df = df_images_ok[(df_images_ok['Diffusion Status'].isna()) | (df_images_ok['Diffusion Status'] == 'concurrent.futures._base.CancelledError')]
    print(nan_df)
    print(f"Faltan por hacer: {len(nan_df)} imagenes...")
    
    columna_imagenes = nan_df['File'].to_list()

    # Print the columna_imagenes list
    print(columna_imagenes)
    print(len(columna_imagenes))

    return columna_imagenes
