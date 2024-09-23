import time
import pretools
import configuracion.configuracion as configuracion

#CICLO INICIAL: OBTENCIÓN DE IMAGENES Y CREACIÓN DE EXCEL DINÁMICO
#Las imagenes se pueden obtener ya sea de una lista de excel o de un directorio que ya contenga las imagenes.

#Nombra la sesión para tener un nuevo directorio por cada sesión.
#Future: Poner un seguro aquí para que si existe ya un excel para esa sesión, pregunte antes de sobreescribir.
sesion = configuracion.sesion
#directorio = configuracion.sesion

print("Bienvenido, iniciaremos el proceso de cargado.")
print(f"La sesión es: {sesion}.")
time.sleep(1)

#Si se usa una lista de EXCEL.
if configuracion.excel_list == True:
    filename = sesion + '.xlsx'    
    #A. Crea el directorio donde se recibirán las imagenes.
    pretools.creaDirectorioInicial(sesion)
    #Future: Si ya se creo el directorio, no volverlo a crear.
    print("Directorio creado...")
    #Crea el excel con sus campos respectivos.
    #Future: Considerar si ejecutamos aquí creaExcel o siempre lo hacemos desde descargaImagenes si se requiere.
    #Respuesta, yo no lo sacaría porque es un proceso muy largo, se queda aquí.
    
    #B.- Éste proceso creará el archivo de excel con los Ids necesarios para cada imagen que procesaremos.
    print("A continuación crearemos el archivo de excel que contendrá los resultados...")
    respuesta = input("Presiona cualquier tecla para continuar: ")
    pretools.creaExcel(filename)

    #Descarga las imagenes source indicadas en el excel(dataframe) y las baja al directorio en disco.
    print("A continuación descargaremos las imagenes del lote...")
    respuesta = input("Presiona cualquier tecla para continuar: ")
    pretools.descargaImagenes(sesion)

    #Sube imagenes a tu servidor.
    print("A continuación descargaremos las imagenes del lote...")
    respuesta = input("Presiona cualquier tecla para continuar: ")
    pretools.subeSources()
    

#Si se usa BULK.
else:
    #Si se usará un bulk de subido de imagenes, el directorio ya existirá y lo que creará es el excel!
    pretools.directoriador(sesion)
    #Subir los sources de bulk también.

    #Finalmente crea los directorios necesarios.
    pretools.creaDirectorioResults(sesion)