import pretools, postools, time, configuracion

#CICLO FINAL: ALTA EN SERVER
excel = "results_excel\\" + configuracion.filename
print("La ruta correcta del excel es: ", excel)

base_url = configuracion.base_url
print("Baseurl es: ", base_url)

sesion = configuracion.sesion
print("Sesión es: ", sesion)

directorio_remoto = base_url + sesion
print("Directorio remoto es: ", directorio_remoto)

print("Iniciando proceso de subida...")

#Sube todo
dataframe = postools.subirTodo(excel, sesion, directorio_remoto)

#Finaliza excel después de postproducción.
print("Si llegó al final, imprimiendo excel, donde excel es: ", configuracion.filename)
pretools.df2Excel(dataframe, configuracion.filename)