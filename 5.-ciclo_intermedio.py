import pretools, intertools, postools, configuracion, time, globales
import pandas as pd

#CICLO INTERMEDIO = STABLE DIFFUSION

base_url = globales.base_url
sesion = configuracion.sesion
foto_complete_url = base_url + sesion
#Por ejemplo https://dominio.com/results/minitest
filename = configuracion.sesion + '.xlsx'

#Future, que cheque si en la carpeta hay archivos nuevos y actualice el excel con sus samples.

#Hacer el Stable Diffusion.
#Future: Las características importantes deberían pasarse desde aquí... (que objeto, etc.)
#inicial indica el archivo desde donde debe empezar.

#Importante: Preprocess es la que llena los ATRIBUTOS!!!!
#inicial="nombre_imagen.jpg" cuando quieras empezar desde uno en particular.
intertools.sampler(sesion, inicial='C4D03AQFOR1F2Z5GmeA-t1.png')

#FULL ES LA QUE HACE EL STABLE DIFF
#Future: Corregir para que empiece exacto.
#Debes de poner en inicial LA ULTIMA QUE SI SE HIZO... si quieres inicial va así: inicial="IsaRomo-t1.jpg"
#FUTURE: Que samples venga de configuración para evitar discrepancias entre preProcess y fullProcess.
#IMPORTANTE: Una alternativa a empezar desde un archivo en particular, es correr mi función missing...
#... que generará una columna de imagenes de todas aquellas que no han sido procesadas (dejando fuera a las complete
#... y a las que tuvieron errores.)
#postools.fullProcess(sesion, dataframe)
#FUTURE: Cuando se apaga la API, full process se queda trabado en ocasiones.

#Finaliza Excel después de preproducción.
#print("Y aquí vamos a guardar el excel porque es lo correcto, porque YA TERMINAMOS!!!!...")
#pretools.df2Excel(dataframe, configuracion.filename)