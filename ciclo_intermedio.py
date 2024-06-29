import pretools, postools, time, configuracion

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
print("Terminé full process...")
time.sleep(2)

#Finaliza Excel después de preproducción.
pretools.df2Excel(dataframe, filename)

