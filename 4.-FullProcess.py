import intertools, configuracion.configuracion as configuracion, time
import configuracion.globales as globales
import pandas as pd

#CICLO INTERMEDIO = STABLE DIFFUSION

#Si varios ciclos comparten éstas variables, házlas globales.
base_url = globales.results_url
sesion = configuracion.sesion
foto_complete_url = base_url + sesion
filename = configuracion.sesion + '.xlsx'

#Hacer el Stable Diffusion.
#Future: Las características importantes deberían pasarse desde aquí... (que objeto, etc.)
#inicial indica el archivo desde donde debe empezar.

#FULL ES LA QUE HACE EL STABLE DIFF
#Future: Corregir para que empiece exacto.
#Debes de poner en inicial LA ULTIMA QUE SI SE HIZO... si quieres inicial va así: inicial="IsaRomo-t1.jpg"
#FUTURE: Que samples venga de configuración para evitar discrepancias entre preProcess y fullProcess.
#IMPORTANTE: Una alternativa a empezar desde un archivo en particular, es correr mi función missing...
#... que generará una columna de imagenes de todas aquellas que no han sido procesadas (dejando fuera a las complete
#... y a las que tuvieron errores.)
intertools.fullProcess(sesion)
#FUTURE: Cuando se apaga la API, full process se queda trabado en ocasiones.

#Future, hace prueba de si en dos terminales distintas se puede hacer el proceso 6 (stable diffusion) y el proceso 7 upload.
#Future, respaldos automáticos de los exceles en cada etapa.