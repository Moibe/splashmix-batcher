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
import globales

#Future: Quitar todos los imports innecesarios.
def subirTodo(excel, sesion, directorio_remoto):
    #Future: ¿Volver uno solo a subirTodo y sube? ¿o cuál es la razón para separarlo?

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
    carpeta_local = globales.imagenes_folder_resultados + sesion + '-results'
    
    #Subir el resultado al servidor y esperar respuesta que se guardará en la var resultado.
    servidor.sube(sftp, dataframe, carpeta_local, directorio_receptor, directorio_remoto)
    print("Salí de sube...")
    time.sleep(1)
    #FUTURE: Poner un while para que después de fallo continue el ciclo de seguir subiendo.

    #Future: que la conexión también se cierre ante interrupciones de excel.
    print("Cerrando conexión...")
    servidor.cierraConexion(ssh, sftp)
    time.sleep(1)

    return dataframe