import pretools, postools, configuracion, time
import pandas as pd

#CICLO INTERMEDIO = STABLE DIFFUSION

base_url = configuracion.base_url
sesion = configuracion.sesion
foto_complete_url = base_url + sesion
#Por ejemplo https://dominio.com/results/minitest
filename = configuracion.filename

#Crea los directorios necesarios.
postools.creaDirectorioResults(sesion)

#Crea el dataframe necesario con el excel designado en configuración.
#ÉSTA ES LA QUE CREA LOS SAMPLES!!
#dataframe = postools.preparaDataframe(configuracion.filename, 4)

#Útil: Auxiliar para obtener dataframe: (como cuando no quieres correr prepararDataFrame de nuevo.)
dataframe = pd.read_excel(filename)

#Hacer el Stable Diffusion.
#Future: Las características importantes deberían pasarse desde aquí... (que objeto, etc.)
#El 4 representa a los samples.
#1 es la ronda.
#inicial indica el archivo desde donde debe empezar.

#Preprocess es la que llena los ATRIBUTOS!!!!
postools.preProcess(sesion, dataframe, inicial="primejb_103662-t1.jpg")

#FULL ES LA QUE HACE EL STABLE DIFF
#postools.fullProcess(sesion, dataframe, samples=4, inicial=None, ronda=None)

#Finaliza Excel después de preproducción.
#print("Y aquí vamos a guardar el excel porque es lo correcto, porque YA TERMINAMOS!!!!...")
pretools.df2Excel(dataframe, configuracion.filename)