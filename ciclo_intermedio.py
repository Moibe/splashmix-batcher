import pretools, postools, time, configuracion

#CICLO INTERMEDIO = STABLE DIFFUSION
base_url = configuracion.base_url
sesion = configuracion.sesion
foto_complete_url = base_url + sesion
filename = configuracion.filename

#Crea los directorios necesarios.
postools.creaDirectorioResults(sesion)

#Crea el dataframe necesario.
dataframe = postools.preparaDataframe(filename)

#Hacer el Stable Diffusion.
postools.fullProcess(sesion, dataframe)

#Finaliza Excel después de preproducción.
pretools.df2Excel(dataframe, filename)