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

print("Bienvenido, iniciaremos el proceso de cargado.")
print(f"La sesión es: {sesion}.")
time.sleep(1)

#Si se usa EXCEL.
if configuracion.excel_list == True:
    
    #Si se usará un excel con urls, entonces creará un directorio para recibirlos.
    pretools.creaDirectorioInicial(sesion)

    #Crea el dataframe donde se registrarán los atributos y las difusiones con los campos necesarios.
    dataframe = pretools.creaDataframe(filename)
    
    #Descarga las imagenes source indicadas en el excel(dataframe) y las baja al directorio en disco.
    pretools.descargaImagenes(sesion, dataframe)
    
    #FUTURE, IMPORTANTE cuando todos los procesos tengan su df2Excel, ya no será necesario incluirlo al final.
    pretools.df2Excel(dataframe, filename)

#Si se usa BULK.
else:
    #Si se usará un bulk de subido de imagenes, el directorio ya existirá y lo que creará es el excel!
    pretools.directoriador(directorio)

#Crea los directorios necesarios.
pretools.creaDirectorioResults(sesion)

#Crea el dataframe necesario con el excel designado en configuración.
#ÉSTA ES LA QUE CREA LOS SAMPLES!!
#Y ASIGNA LOS ATRIBUTOS A CADA SAMPLE.
dataframe = pretools.preparaSamples(configuracion.filename, 2)