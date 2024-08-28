import time
import pretools, tools
import configuracion

#FUTURE: Todos los procesos, incluído ciclo inicial, intermedio y final deberían ir en una sola hoja?

#CICLO INICIAL: OBTENCIÓN DE IMAGENES Y CREACIÓN DE EXCEL DINÁMICO
#Las imagenes se pueden obtener ya sea de una lista de excel o de un directorio que ya contenga las imagenes.

#Nombra la sesión para tener un nuevo directorio por cada sesión.
sesion = configuracion.sesion
#directorio = configuracion.sesion
#filename = configuracion.filename

print("Bienvenido, iniciaremos el proceso de cargado.")
print(f"La sesión es: {sesion}.")

#Si se usa EXCEL.
if configuracion.excel_list == True:

    filename = sesion + '.xlsx'
    
    #Si se usará un excel con urls, entonces creará un directorio para recibirlos.
    pretools.creaDirectorioInicial(sesion)    

    #Crea el excel con sus campos respectivos e importante, la última adición:
    #primero creo aqió la columna con los nombres, para que sea más fácil de ubicar al descargar imagenes y reiniciar el proceso.
    #pretools.creaExcel(filename)
    
    #Descarga las imagenes source indicadas en el excel(dataframe) y las baja al directorio en disco.
    #Ya no usamos el dataframe creado arriba, descargamos el nuevo archivo que está en results.
    #Porque si no siempre estaría iniciando desde cero.
    pretools.descargaImagenes(sesion)   

#Si se usa BULK.
else:
    #Si se usará un bulk de subido de imagenes, el directorio ya existirá y lo que creará es el excel!
    pretools.directoriador(sesion)

#Crea los directorios necesarios.
pretools.creaDirectorioResults(sesion)