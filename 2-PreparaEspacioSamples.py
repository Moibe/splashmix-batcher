import pretools
import configuracion.configuracion as configuracion

#Crea el dataframe necesario con el excel designado en configuración.
#ÉSTA ES LA QUE crea los espacios para los samples.

#parámetros: Archivo de excel a editar, cantidad de samples.
pretools.preparaSamples(configuracion.sesion + '.xlsx', 2)