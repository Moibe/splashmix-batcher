import pretools, intertools, postools, configuracion.configuracion as configuracion, time
import configuracion.globales as globales
import pandas as pd

#CICLO INTERMEDIO = STABLE DIFFUSION

base_url = globales.results_url
sesion = configuracion.sesion
#FUTURE: Que exista la opción de si poner la imagen source de local o de URL (o cambio en automático).
foto_complete_url = base_url + sesion
#Por ejemplo https://dominio.com/results/minitest
filename = configuracion.sesion + '.xlsx'

#Future, que cheque si en la carpeta hay archivos nuevos y actualice el excel con sus samples.

#Future: Las características importantes deberían pasarse desde aquí... (que objeto, etc.)

#Importante: Preprocess es la que llena los ATRIBUTOS!!!!
#inicial="nombre_imagen.jpg" cuando quieras empezar desde uno en particular.
intertools.blueprint(sesion)

