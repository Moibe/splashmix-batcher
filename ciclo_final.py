import pretools, postools, time, configuracion

#CICLO FINAL: ALTA EN SERVER

filename = configuracion.filename
base_url = configuracion.base_url
sesion = configuracion.sesion
foto_complete_url = base_url + sesion

#Crea el dataframe necesario.
dataframe = postools.preparaDataframe(filename)

#Sube todo
dataframe = postools.subirTodo(dataframe, sesion, foto_complete_url)

#Finaliza excel después de postproducción.
pretools.df2Excel(dataframe, filename)