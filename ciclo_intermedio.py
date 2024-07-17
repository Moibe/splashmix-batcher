import pretools, postools, configuracion, time

#CICLO INTERMEDIO = STABLE DIFFUSION

base_url = configuracion.base_url
sesion = configuracion.sesion
foto_complete_url = base_url + sesion
#Por ejemplo https://dominio.com/results/minitest
filename = configuracion.filename

#Crea los directorios necesarios.
postools.creaDirectorioResults(sesion)

#Crea el dataframe necesario con el excel designado en configuración.
dataframe = postools.preparaDataframe(configuracion.filename)

#Hacer el Stable Diffusion.
postools.fullProcess(sesion, dataframe)

#Finaliza Excel después de preproducción.
pretools.df2Excel(dataframe, configuracion.filename)