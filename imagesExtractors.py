import os
#Ésta es la biblioteca de extractores, en donde habrá uno diferente para cada tipo de url que estamos extrayendo. 

#Future: Que se acceda cada función como parámetro, revisar repositorios, ya lo haz hecho.

def clayLinkedIn(foto_url):

    filename = os.path.dirname(foto_url)
    partes = filename.split('image/')
    siguiente = partes[1].split('/')
    #siguiente[0] contiene el nombre del archivo, pero queremos quitarle los guiones para evitar problemas más adelante.
    nombre = siguiente[0].replace("-", "")    
    image_id = f"{nombre}.png"

    return image_id

def clayLinkedInV2(foto_url):

    filename = os.path.dirname(foto_url)
    partes = filename.split('image/v2/')
    siguiente = partes[1].split('/')
    #siguiente[0] contiene el nombre del archivo, pero queremos quitarle los guiones para evitar problemas más adelante.
    nombre = siguiente[0].replace("-", "")    
    image_id = f"{nombre}.png"

    return image_id