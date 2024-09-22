import configuracion.configuracion as configuracion
import pretools

#Crea el dataframe necesario con el excel designado en configuración.
#ÉSTA ES LA QUE CREA LOS SAMPLES!!
#Y ASIGNA LOS ATRIBUTOS A CADA SAMPLE.

pretools.preparaSamples(configuracion.sesion + '.xlsx', 1)