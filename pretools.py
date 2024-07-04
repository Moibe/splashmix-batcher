import os 
import requests
import pandas as pd
import time

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
    print("This is the target: ", target_dir)

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
     
    df = pd.read_excel(archivo)


    #Importante: Crea las nuevas columnas que necesitará:
    df['Name'] = ''
    df['Download Status'] = ''
    df['Diffusion Status']=''
    #Revisar si la cantidad de campos URL la podrías crear dinámicamente.
    df['Take1'] = ''
    df['Shot1'] = ''
    df['Style1'] = ''
    df['Hero1'] = ''
    df['URL1']=''

    df['Take2'] = ''
    df['Shot2'] = ''
    df['Style2'] = ''
    df['Hero2'] = ''
    df['URL2']=''

    df['Take3'] = ''
    df['Shot3'] = ''
    df['Style3'] = ''
    df['Hero3'] = ''
    df['URL3']=''

    df['Take4'] = ''
    df['Shot4'] = ''
    df['Style4'] = ''
    df['Hero4'] = ''
    df['URL4']=''

    #Aquí dinámicamente indico cuantos samples haré.
    max_url_columns = 4

    for i in range(1, max_url_columns + 1):

        column_name = f"URL{i}"  # Create column name dynamically
        df[column_name] = ''  # Create the new column with an empty string

    return df
    
def procesaImagenes(sesion, dataframe):

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
        image_id = f"{siguiente[0]}.png"

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

def df2Excel(dataframe, filename):

    """
    Guarda el Dataframe final en el archivo de excel original.

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.
    
    """
     
    # Obtiene la ruta actual del script (directorio raíz del proyecto)
    ruta_actual = os.path.dirname(__file__)
    print("Esto es la ruta actual: ", ruta_actual)

    # Combina la ruta actual con el nombre del archivo para obtener la ruta relativa
    ruta_archivo = os.path.join(ruta_actual, filename )
    print("Ésto es la ruta archivo: ", ruta_archivo)

    # Guarda el DataFrame con la nueva columna en el archivo Excel
    dataframe.to_excel(ruta_archivo, index=False)

    return True