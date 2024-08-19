import os 
import requests
import pandas as pd
import time
import configuracion
from openpyxl import Workbook, load_workbook
import globales
import tools

def creaDirectorioInicial(sesion): 
    """
    Crear los directorios donde se guardarán las fotos, con un nombre que se recíbe como parámetro.

    Parameters:
    archivo (str): Nombre y extensión del archivo que procesaremos.

    Returns:
    dataframe:Regresa dataframe que se usará a través de los procesos.

    """

    # Define the desired directory path
    target_dir = os.path.join('imagenes', 'fuentes', sesion)
    print("Directorio para ésta sesión creado en: ", target_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    

def creaDataframe(archivo):
    """
    Lee el archivo Excel en un DataFrame (asumiendo que está en la raíz del proyecto) y
    crea las columnas nuevas que necesitará.

    Parameters:
    archivo (str): Nombre y extensión del archivo que procesaremos.

    Returns:
    dataframe:Regresa dataframe que se usará a través de los procesos.

    """
    #FUTURE, la carpeta de los exceles que se reciba por configuración. 
    df = pd.read_excel(globales.excel_source_path + archivo)
    
    #Importante: Crea las nuevas columnas que necesitará:
    #Future, revisa si podría no crearlas, ya vez que actualizaRow las crea al vuelo.
    df['Name'] = ''
    df['Download Status'] = ''
    df['Take'] = ''
    df['File'] = ''
    df['Diffusion Status'] = ''

    #Ve si afecta actualizar el excel antes de entregar el dataframe.
    #IMPORTANTE: Quizá no se necesita hacer ésta escritura pq si hace la escritura final. Prueba.
    tools.df2Excel(df, configuracion.filename)
    
    return df

#mejor le pasas el objeto completo llamado creación y que de ahí lea cada uno de sus atributos.
def createColumns(dataframe, amount, diccionario_atributos):

    # Set of column names to repeat
    #column_names = ['DiffusionStatus', 'Take', 'Shot', 'Style', 'Hero', 'URL']
    column_names = list(diccionario_atributos)
    # Create a list of desired column order
    #desired_order = ['DiffusionStatus', 'Take', 'Shot', 'Style', 'Hero', 'URL']
    desired_order = ['DiffusionStatus'] + [name for name in column_names if name != 'DiffusionStatus'] + ['URL']

    # Sort column names based on desired order and repeat
    column_groups = [[f"{name}{i + 1}" for name in group] for i in range(amount) for group in zip(*sorted(zip(desired_order, column_names)))]
    
    
    # Flatten the nested list into a single list
    dynamic_columns = [item for sublist in column_groups for item in sublist]

    # Add dynamic columns to the DataFrame
    dataframe[dynamic_columns] = ''

    return dataframe
   
    
def descargaImagenes(sesion, dataframe):

    """
    Recorre cada imagen obteniendo su nombre y guardándolo en el dataframe.
    Posteriormente obteniendo cada una de esas imagenes.

    Parameters:
    columna_fotos(dataframe): El objeto que contiene la columna con los nombres de las fotos.
    dataframe(dataframe): El dataframe final.

    Raises:

    Returns:
    dataframe:Regresa dataframe que se usará a través de los procesos.
    """

    #Objeto que contiene la columna de urls con las fotos.
    #Se asume que el excel recibido tendrá la columna SOurce con todas las url de las imagenes a descargar.
    columna_fotos = dataframe['Source']

    #FUTURE, si es un set de imagenes que ya bajamos en el pasado poder evitar bajarlas de nuevo.

    # Recorre cada URL de foto en la columna
    for i, foto_url in enumerate(columna_fotos):
    
        # NOMBRANDO EL ARCHIVO
        # Define un indentificador único.
        # Esto será diferente para cada tipo de URL que se te envíe. 
        # Trata de generalizar en el futuro.
        filename = os.path.dirname(foto_url)
        partes = filename.split('image/')
        siguiente = partes[1].split('/')
        #siguiente[0] contiene el nombre del archivo, pero queremos quitarle los guiones para evitar problemas más adelante.
        
        nombre = siguiente[0].replace("-", "")
        
        image_id = f"{nombre}.png"

        #Actualiza la columna 'Name' con el nombre del archivo.
        dataframe.loc[i, 'Name'] = image_id

        # Attempt to download the image
        #FUTURE: Si ya existe la imagen en el directorio (por ejemplo si ya se habían bajado en una prueba anterior)...
        #... que no vaya a internet y la vuelva a bajar, que se salte eso.
        try:
            response = requests.get(foto_url)
            if response.status_code == 200:
                with open(f'imagenes/fuentes/{sesion}/{image_id}', 'wb') as f:
                    f.write(response.content)
                download_status = 'Success'
                print(f"Image '{image_id}' downloaded successfully.")
                dataframe.loc[i, 'Download Status'] = download_status
                
            else:
                message = f"Error downloading image: {foto_url} (Status code: {response.status_code})"
                raise Exception(message)
        except Exception as e:
            download_status = f"Error: {response.status_code}"
            dataframe.loc[i, 'Download Status'] = download_status
            print(f"Error downloading image: {foto_url} - {e}")

def directoriador(directorio):

    #FUTURE: Que los exceles iniciales residan en una carpeta exclusiva para eso.
    #FUTURE: Que el directoriador mande la carpeta hecha a un directorio específico.
    #FUTURE: Que source_excel y results_excel, estén en la misma carpeta.

    try:
        excel = globales.excel_results_path + directorio + ".xlsx"
        #Las imagenes tuvieron que haber sido subidas a la ruta correcta previamente.
        directory_address = "imagenes/fuentes/" + directorio
        print("El excel que usaremos es: ", excel)
        print("La ruta completa es: ", directory_address)
        
        workbook = load_workbook(excel)

    except FileNotFoundError:
        workbook = Workbook()

    worksheet = workbook.active

    
    worksheet.cell(row=1, column=1).value = "Name"
    worksheet.cell(row=1, column=2).value = "Download Status"
    worksheet.cell(row=1, column=3).value = "Take"
    worksheet.cell(row=1, column=4).value = "File"
    worksheet.cell(row=1, column=5).value = "Diffusion Status"
    
    row = 2  # Comenzar desde la fila 2 (después del encabezado)

    for filename in os.listdir(directory_address):
        #if filename.endswith(".jpg") or filename.endswith(".png"):
            
            # Agregar nombre de archivo en la primera columna
            worksheet.cell(row=row, column=1).value = filename

            # Agregar "Success" en la segunda columna
            worksheet.cell(row=row, column=2).value = "Success"

            row += 1

    workbook.save(excel)

def creaDirectorioResults(sesion):
    """
    Crea el directorio donde se recibirán los resultados en caso de no existir. El directorio llevará el nombre de la sesión + "results".

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.

    """
    results_dir = os.path.join('imagenes', 'resultados', sesion + "-results" )   
    
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

def preparaSamples(filename, samples):

    #Ésta función prepara el espacio para la cantidad de samples que quieres crear.
    #Creará una row adicional para cada sample que desees.

    #Primero extraemos el dataframe:
    dataframe = pd.read_excel(globales.excel_results_path + filename)    

    #Después vemos cuales son Success:
    #Filtra las filas donde 'Download Status' es igual a 'Success'
    #FUTURE: Hacer una función filtradora donde solo se reciba el nombre de la columna que quieres filtrar y el texto.
    df_images_ok = dataframe[dataframe['Download Status'] == 'Success'] 

    print("Ahora prepararé la columna bidimensional:")
    df_imagenes_seleccionadas = df_images_ok[['Name', 'Source']]
   
    try:

        #Crea las rows para sus samples
        #for imagen in columna_imagenes:
        for index, row in df_imagenes_seleccionadas.iterrows():
            imagen = row['Name']
            source = row['Source']

            #FUTURE: Agrega un contador para saber cuantas faltan. 
            #FUTURE: Ponle un Keyboard Interrupt con guardado de excel también a éste ciclo.
            
            nombre, extension = imagen.split(".")       

            #Cuando encuentra la imagen llena los datos de la primera incidencia.
            indice = tools.obtenIndexRow(dataframe, 'Name', imagen)
            dataframe.loc[indice, 'Take'] = 1
            dataframe.loc[indice, 'File'] = nombre + "-" + "t" + str(1) + "." + extension
            #FUTURE: Aquí causa el error de type de pandas, corrigelo antes de que quede deprecado.
            
            #AQUÍ VA IR LO QUE TENIAMOS DENTRO DEL FOR, que son el resto de los samples:
            if configuracion.excel_list is True:
                #En lugar de esas comillas vas a poner el source.
                lista = [source, imagen, 'Success', "take_placeholder", "filename", ""]  #adding a row
                #Designación de columnas a utilizar.
                a = 3 #Aquí sustituira el índice 3 take_placeholder
                b = 4 
            else:         
                #Para imagenes de directorio.
                lista = [imagen, 'Success', "take_placeholder", "filename", ""]  #adding a row
                #Designación de columnas a utilizar.
                a = 4 #Aquí sustituira el índice 4 take_placeholder
                b = 5

            #Y luego crea tantas rows adicionales como samples fuera a haber.
            for i in range(samples - 1): 
                        
                # Replace the element at the index with the sustituto variable
                #Esto es el Take
                lista[a] = i + 2

                #Empieza desde el 2 porque ya hizo la 1.
                #Esto es el File
                filename = nombre + "-" + "t" + str(i+2) + "." + extension
                
                # Replace the element at the index with the sustituto variable
                lista[b] = filename
                
                print("La lista quedó como: ", lista)
                
                tools.creaRow(dataframe, imagen, i + 2, filename, lista)

    except KeyboardInterrupt:
      print("KEYBOARD: Interrumpiste el proceso, guardaré el dataframe en el excel, hasta donde ibamos. Y aquí el excel es:", configuracion.filename)
      tools.df2Excel(dataframe, configuracion.filename)        
    
    #Reordeno alfabéticamente.
    #FUTURE: Verificar si algo malo pasa si no se hace éste reordenamiento, porque por ejemplo el Keyboard Interrupt...
    #... no lo contempla.
    dataframe = dataframe.sort_values(['Name','Take'])

    #Es esto la línea universal para guardar el excel? = Si, si lo es :) 
    tools.df2Excel(dataframe, configuracion.filename)
      
    return dataframe
