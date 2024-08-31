import os, tools, globales
import pandas as pd

def reversor(directorio):
#Éste proceso es para cuando se tiene imagenes bajadas already de ese lote, pero no se tiene un registro de excel, 
#por lo tanto hará el proceso al revés, verá que archivos existen y los escribirá en el excel.
#Quizá sería más práctico bajar todas las imagenes de nuevo, pero para lotes grandes puede consumir más tiempo, 
#Además con la separación de un segundo entre cada imagen, si es un tiempo a considerar.

    dataframe = pd.read_excel(globales.excel_results_path + filename) 

    directory_address = "imagenes/fuentes/" + directorio

    for filename in os.listdir(directory_address):

        tools.obtenIndexRow(dataframe, 'Name', filename )



reversor('newBath')

