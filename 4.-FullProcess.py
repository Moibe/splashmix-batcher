import intertools 
import configuracion.globales as globales
import configuracion.configuracion as configuracion

#CICLO INTERMEDIO = STABLE DIFFUSION

#Si varios ciclos comparten éstas variables, házlas globales.
base_url = globales.results_url
sesion = configuracion.sesion
foto_complete_url = base_url + sesion
filename = configuracion.sesion + '.xlsx'

#Hacer el Stable Diffusion.
#Future: Las características importantes deberían pasarse desde aquí... (que objeto, etc.)

#FUTURE: Que samples venga de configuración para evitar discrepancias entre preProcess y fullProcess.
#IMPORTANTE: Una alternativa a empezar desde un archivo en particular, es correr mi función missing...
#... que generará una columna de imagenes de todas aquellas que no han sido procesadas (dejando fuera a las complete
#... y a las que tuvieron errores.)
intertools.fullProcess(sesion)
#FUTURE: Cuando se apaga la API, full process se queda trabado en ocasiones.

#Future, hace prueba de si en dos terminales distintas se puede hacer el proceso 6 (stable diffusion) y el proceso 7 upload.
#Future, respaldos automáticos de los exceles en cada etapa.