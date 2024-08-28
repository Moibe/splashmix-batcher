import configuracion
import pretools


#Crea el dataframe necesario con el excel designado en configuración.
#ÉSTA ES LA QUE CREA LOS SAMPLES!!
#Y ASIGNA LOS ATRIBUTOS A CADA SAMPLE.

dataframe = pretools.preparaSamples(configuracion.sesion + '.xlsx', 1)