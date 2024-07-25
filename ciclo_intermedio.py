import pretools, postools, configuracion, time
import pandas as pd

#CICLO INTERMEDIO = STABLE DIFFUSION

base_url = configuracion.base_url
sesion = configuracion.sesion
foto_complete_url = base_url + sesion
#Por ejemplo https://dominio.com/results/minitest
filename = configuracion.filename

#Crea los directorios necesarios.
#postools.creaDirectorioResults(sesion)

#Crea el dataframe necesario con el excel designado en configuración.
#ÉSTA ES LA QUE CREA LOS SAMPLES!!
#Y ASIGNA LOS ATRIBUTOS A CADA SAMPLE.
#dataframe = postools.preparaSamples(configuracion.filename, 4)

#Future, que cheque si en la carpeta hay archivos nuevos y actualice el excel con sus samples.

#Útil: Auxiliar para obtener dataframe: (como cuando no quieres correr prepararDataFrame de nuevo.)
#dataframe = pd.read_excel(filename)
#Auxiliar para archivo excel de resultados.
#La ruta sirve con diagonal normal / o con doble diagonal \\
dataframe = pd.read_excel('results_excel/' + filename)

#Hacer el Stable Diffusion.
#Future: Las características importantes deberían pasarse desde aquí... (que objeto, etc.)
#inicial indica el archivo desde donde debe empezar.

#Preprocess es la que llena los ATRIBUTOS!!!!
#inicial="primejb_23104-t2.jpg" cuando quieras empezar desde uno en particular.
#postools.preProcess(sesion, dataframe)

#FULL ES LA QUE HACE EL STABLE DIFF
#Inicial debe ser basado en 'Name' no en 'File'
#Future: Corregir para que empiece exacto.
#Debes de poner en inicial LA ULTIMA QUE SI SE HIZO... si quieres inicial va así: inicial="IsaRomo-t1.jpg"
#FUTURE: Que samples venga de configuración para evitar discrepancias entre preProcess y fullProcess.
postools.fullProcess(sesion, dataframe, samples=4)

#Finaliza Excel después de preproducción.
print("Y aquí vamos a guardar el excel porque es lo correcto, porque YA TERMINAMOS!!!!...")
pretools.df2Excel(dataframe, configuracion.filename)