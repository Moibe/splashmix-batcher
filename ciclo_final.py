import pretools, postools, time, configuracion

#CICLO FINAL: ALTA EN SERVER
excel = "results_excel\\" + configuracion.filename
print("La ruta correcta del excel es: ", excel)
time.sleep(8)
base_url = configuracion.base_url
sesion = configuracion.sesion
directorio_remoto = base_url + sesion

#Sube todo
dataframe = postools.subirTodo(excel, sesion, directorio_remoto)

#Finaliza excel después de postproducción.
pretools.df2Excel(dataframe, excel)