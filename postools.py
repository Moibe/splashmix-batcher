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
import prompter
import tools
import globales

   
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
        print("La ruta de gradio en result[0] es: ", ruta_imagen_local)
        
        #IMPORTANTE, GUARDANDO EN DISCO DURO.
        with open(ruta_imagen_local, "rb") as archivo_lectura:
            contenido_imagen = archivo_lectura.read()	

        with open(ruta_total, "wb") as archivo_escritura:
            archivo_escritura.write(contenido_imagen)
            print(f"Imagen guardada correctamente en: {ruta_total}")
            print("Estamos por actualizar excel...")
            
    #FUTURE: Ésto se tiene que hacer dinámicamente.

    #Después, haya o no guardado en disco duro, registrará que terminó en el excel.

    #actualiza Row actualiza una sola row.
    print("Estoy por actualizarRow y el mensaje es:", message)
    print("y su filename (índice) es: ", filename)
    
    #Sin problema ya puede actualizar el respectivo DiffusionStatus porque siempre está presente.
    tools.actualizaRow(dataframe, 'File', filename, 'Diffusion Status', message)      
    tools.actualizaRow(dataframe, 'File', filename, 'Direccion', ruta_absoluta)

    #Es esto la línea universal para guardar el excel? = Si, si lo es :) 
    pretools.df2Excel(dataframe, configuracion.filename)
     

def subirTodo(excel, sesion, directorio_remoto):

    #Primero extraemos el dataframe:
    dataframe = pd.read_excel(excel)  
    
    #Conexión al servidor.
    ssh, sftp = servidor.conecta()
        
    #Define ruta de la carpeta remota
    #Ésta es la carpeta fija de holocards.
    carpeta_remota = nodes.avaimentekijä
    print(f"La carpeta remota es: {carpeta_remota} y su tipo es: {type(carpeta_remota)}.")
    directorio_receptor = carpeta_remota + sesion
    print(f"El directorio receptor será entonces: {directorio_receptor} y su tipo es: {type(directorio_receptor)}")
    
    #Define ruta de la carpeta local donde se encuentran los resultados.
    carpeta_local = 'imagenes\\resultados\\' + sesion + '-results'
    
    #Subir el resultado al servidor y esperar respuesta que se guardará en la var resultado.
    servidor.sube(sftp, dataframe, carpeta_local, directorio_receptor, directorio_remoto)
    print("Salí de sube...")
    
    servidor.cierraConexion(ssh, sftp)

    return dataframe