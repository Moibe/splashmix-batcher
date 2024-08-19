import time
import pretools
import configuracion

#FUTURE: Todos los procesos, incluído ciclo inicial, intermedio y final deberían ir en una sola hoja?

#CICLO INICIAL: OBTENCIÓN DE IMAGENES Y CREACIÓN DE EXCEL DINÁMICO
#Las imagenes se pueden obtener ya sea de una lista de excel o de un directorio que ya contenga las imagenes.

#Nombra la sesión para tener un nuevo directorio por cada sesión.
sesion = configuracion.sesion
directorio = configuracion.sesion
filename = configuracion.filename

#Si se usa EXCEL.
if configuracion.excel_list == True:
    #Si se usará un excel con urls, entonces creará un directorio para recibirlos.
    #Ésto solo crea el directorio de fotos source.
    pretools.creaDirectorioInicial(sesion)

    #Crea el excel donde se registrarán los atributos y las difusiones con los campos necesarios.
    dataframe = pretools.creaDataframe(filename)
    
    #Descarga las imagenes source indicadas en el excel(dataframe) y las baja.
    pretools.descargaImagenes(sesion, dataframe)
    
    #FUTURE, IMPORTANTE cuando todos los procesos tengan su df2Excel, ya no será necesario incluirlo al final.
    pretools.df2Excel(dataframe, filename)

#Si se usa BULK.
else:
    #Si se usará un bulk de subido de imagenes, el directorio ya existirá y lo que creará es el excel!
    pretools.directoriador(directorio)