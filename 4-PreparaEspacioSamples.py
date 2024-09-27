import configuracion.configuracion as configuracion
import pretools

#Crea el dataframe necesario con el excel designado en configuración.
#ÉSTA ES LA QUE CREA LOS espacios para los SAMPLES.
#Y ASIGNA LOS ATRIBUTOS A CADA SAMPLE.

#parámetros: Archivo de excel a editar, cantidad de samples.
pretools.preparaSamples(configuracion.sesion + '.xlsx', 2)