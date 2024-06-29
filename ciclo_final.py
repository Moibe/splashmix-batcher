import pretools, postools, time

base_url = "https://euroglitter.com/results/"
sesion = 'minitest1' #Nombra la sesión para tener un nuevo directorio por cada sesión.
foto_complete_url = base_url + sesion
filename = 'minitest.xlsx'

# #Crea los directorios necesarios.
# postools.creaDirectorioResults(sesion)

#Crea el dataframe necesario.
dataframe = postools.preparaDataframe(filename)

# #Hacer el Stable Diffusion.
# postools.fullProcess(sesion, dataframe)
# print("Terminé full process...")
# time.sleep(3)

# #Finaliza Excel después de preproducción.
# pretools.df2Excel(dataframe, filename)

#Sube todo
dataframe = postools.subirTodo(dataframe, sesion, foto_complete_url)

#Finaliza excel después de postproducción.
pretools.df2Excel(dataframe, filename)