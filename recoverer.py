import os
import time
import postools
import configuracion.configuracion as configuracion
import pandas as pd

#Éste archivo recupera un excel que hayas borrado sin querer.

directorio = configuracion.sesion

excel = "results_excel\\" + directorio + ".xlsx"

dataframe = pd.read_excel(excel)
print("Se extrajo el dataframe, que es éste.")
print(dataframe)

#Las imagenes tuvieron que haber sido subidas a la ruta correcta previamente.
directory_address = "imagenes\\resultados\\" + directorio + "-results"

lista = os.listdir(directory_address)

for elemento in lista: 
    print(elemento)
    raiz_pc = os.getcwd()
    ruta_completa = os.path.join(raiz_pc, directory_address, elemento)
    print(ruta_completa)
    postools.actualizaRow(dataframe, 'File', elemento, 'Direccion', ruta_completa)
    postools.actualizaRow(dataframe, 'File', elemento, 'Diffusion Status', 'Complete')  