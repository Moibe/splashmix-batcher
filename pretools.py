import os 
import requests
import pandas as pd
import time
import configuracion
from openpyxl import Workbook, load_workbook

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
     
    df = pd.read_excel('source_excel\\' + archivo)
    
    #Importante: Crea las nuevas columnas que necesitará:
    #Future, revisa si podría no crearlas, ya vez que actualizaRow las crea al vuelo.
    df['Name'] = ''
    df['Download Status'] = ''
    df['Take'] = ''
    df['File'] = ''
    df['Diffusion Status'] = ''

    #Ve si afecta actualizar el excel antes de entregar el dataframe.
    #IMPORTANTE: Quizá no se necesita hacer ésta escritura pq si hace la escritura final. Prueba.
    df2Excel(df, configuracion.filename)
    
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
    columna_fotos = dataframe['Source']

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

    try:
        excel = "source_excel\\" + directorio + ".xlsx"
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

          

def df2Excel(dataframe, filename):

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

    ruta_excel = os.path.join(ruta_actual, "results_excel")

    # Combina la ruta actual con el nombre del archivo para obtener la ruta relativa
    ruta_archivo = os.path.join(ruta_excel, filename )
    print("Ésto es la ruta archivo: ", ruta_archivo)

    # Guarda el DataFrame con la nueva columna en el archivo Excel
    dataframe.to_excel(ruta_archivo, index=False)

    return True