import time
import pretools
import configuracion.configuracion as configuracion

#FUTURE: Todos los procesos, incluído ciclo inicial, intermedio y final deberían ir en una sola hoja o api?

#CICLO INICIAL: OBTENCIÓN DE IMAGENES Y CREACIÓN DE EXCEL DINÁMICO
#Las imagenes se pueden obtener ya sea de una lista de excel o de un directorio que ya contenga las imagenes.

#Nombra la sesión para tener un nuevo directorio por cada sesión.
sesion = configuracion.sesion
#directorio = configuracion.sesion
#filename = configuracion.filename

print("Bienvenido, iniciaremos el proceso de cargado.")
print(f"La sesión es: {sesion}.")
time.sleep(1)

#Si se usa una lista de EXCEL.
if configuracion.excel_list == True:
    filename = sesion + '.xlsx'
    
    #A. Crea el directorio donde se recibirán las imagenes.
    #Si se usará un excel con urls, entonces creará un directorio para recibirlos.
    #pretools.creaDirectorioInicial(sesion)
    #Crea el excel con sus campos respectivos e importante, la última adición:
    #primero creo aquí la columna con los nombres, para que sea más fácil de ubicar al descargar imagenes y reiniciar el proceso.
    #Future: Considerar si ejecutamos aquí creaExcel o siempre lo hacemos desde descargaImagenes si se requiere.
    
    #B.- Éste proceso creará el archivo de excel con los Ids necesarios para cada imagen que procesaremos.
    # print("A continuación crearemos el archivo de excel que contendrá los resultados...")
    # respuesta = input("Presiona cualquier tecla para continuar: ")
    # pretools.creaExcel(filename)

    #Descarga las imagenes source indicadas en el excel(dataframe) y las baja al directorio en disco.
    #Ya no usamos el dataframe creado arriba, descargamos el nuevo archivo que está en results.
    #Porque si no siempre estaría iniciando desde cero.
    print("A continuación descargaremos las imagenes del lote...")
    respuesta = input("Presiona cualquier tecla para continuar: ")
    pretools.descargaImagenes(sesion)

#Si se usa BULK.
else:
    #Si se usará un bulk de subido de imagenes, el directorio ya existirá y lo que creará es el excel!
    pretools.directoriador(sesion)

#Finalmente crea los directorios necesarios.
pretools.creaDirectorioResults(sesion)

#Crear una función que suba las imagenes de perfil de Linkedin a un servidor propio.