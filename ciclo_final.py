import pretools, postools, time, configuracion

#CICLO FINAL: ALTA EN SERVER

filename = configuracion.filename
base_url = configuracion.base_url
sesion = configuracion.sesion
foto_complete_url_dir = base_url + sesion

#Crea el dataframe necesario.
#¿Por qué volver a hacer dataframe? Porque la subida se puede hacer en algún momento separado al ciclo intermedio.
#DEFINITIVAMENTE NO QUIERES PREPARAR SAMPLES.
#dataframe = postools.preparaSamples(filename)

#Sube todo
dataframe = postools.subirTodo(dataframe, sesion, foto_complete_url_dir)

#Finaliza excel después de postproducción.
pretools.df2Excel(dataframe, filename)