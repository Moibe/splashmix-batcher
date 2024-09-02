import os, tools, globales
import pandas as pd
import time
import pretools
import configuracion

def reversor(directorio):
#Éste proceso es para cuando se tiene imagenes bajadas already de ese lote, pero no se tiene un registro de excel, 
#por lo tanto hará el proceso al revés, verá que archivos existen y los escribirá en el excel.
#Quizá sería más práctico bajar todas las imagenes de nuevo, pero para lotes grandes puede consumir más tiempo, 
#Además con la separación de un segundo entre cada imagen, si es un tiempo a considerar.
#Otra ventaja será poner en el track a las imágenes que en el proceso fueron quitadas por su dueño, y aún podemos usar.

    dataframe = pd.read_excel(globales.excel_results_path + directorio + '.xlsx') 

    print("Voy a imprimir el dataframe: ")
    print(dataframe)
    
    directory_address = "imagenes/fuentes/" + directorio

    contador = 0

    for filename in os.listdir(directory_address):

        indice = tools.obtenIndexRow(dataframe, 'Name', filename )
        
        if not indice.empty:            
            
            cell_value = dataframe.loc[indice[0], 'Download Status']
            cell_name = dataframe.loc[indice[0], 'Name']
            print("Éste es el nombre encontrado:", cell_value)

            #Celda normal, no hay nada que hacer.
            if cell_value == "Success":
                    print("El archivo si tiene un registro en el excel...")
            #Registro de imagen existente pero ausente en el excel.
            elif pd.isnull(cell_value):
                print("Download status está vacío pero la imagen si existe, por lo tanto, guárdala como Recovered.")
                dataframe.loc[indice[0], 'Download Status'] = 'Recovered'
            #Si no tenía Success ni Nan, entonces tiene un eror 404 (o sea que no lo encontró en ésta ocasión).
            #Y si por el contrario, la imagen existe, entonces deberá registrarlo como 'From Archive'
            else:
                print(f"El archivo {cell_name} no tiene un registro en el excel, aunque si existe.")
                print("Deberías registrarlo.")
                dataframe.loc[indice[0], 'Download Status'] = 'From Archive'
                
        contador = contador + 1

    print("El conteo final fue: ", contador)
    tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')

    #FUTURE: Después de hacer una recuperación, quedarán espacios vacios, esos en el pasado no se encontraron, 
    #pero así como pueden desaparecer, pueden aparecer, y por lo tanto, para ésta ocasión podrían estar ahí. 
    #Por lo tanto haz otra ronda que intente recuperar esos vacios, para que si no los encuentra, vuelva a ponerles...
    #La label de 'Error:'

#Aquí es donde lo corre y aquí va el nombre de la sesión que quieres corregir.
reversor('newBatch')

#FUTURE: Realizar más pruebas exhaustivas sobre el recoverer.