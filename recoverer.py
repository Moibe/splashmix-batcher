import os
import time
import configuracion

#Éste archivo recupera un excel que hayas borrado sin querer.

directorio = configuracion.sesion

excel = "results_excel\\" + directorio + ".xlsx"
#Las imagenes tuvieron que haber sido subidas a la ruta correcta previamente.
directory_address = "imagenes/fuentes/" + directorio

lista = os.listdir(directory_address)

for elemento in lista: 
    print(elemento)
    time.sleep(1)