import time
import pretools
import configuracion

#CICLO INICIAL: OBTENCIÓN DE IMAGENES 
#Las imagenes se pueden obtener ya sea de una lista de excel o de un directorio que ya contenga las imagenes.

#Nombra la sesión para tener un nuevo directorio por cada sesión.
sesion = configuracion.sesion
directorio = configuracion.sesion
filename = configuracion.filename

#Si se usa EXCEL.
if configuracion.source_list == True: 

    #Si se usará un excel con urls, entonces creará un directorio para recibirlos.

    #Ésto solo cea el directorio de fotos.
    pretools.creaDirectorioInicial(sesion)

    
    dataframe = pretools.creaDataframe(filename)
    pretools.descargaImagenes(sesion, dataframe)
    pretools.df2Excel(dataframe, filename)

#Si se usa BULK.
else:
    #Si se usará un bulk de subido de imagenes, el directorio ya existirá y lo que creará es el excel!
    print("Analizando las imagenes del directorio...")
    pretools.directoriador(directorio)