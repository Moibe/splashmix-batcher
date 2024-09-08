import tools, postools, time, configuracion, globales

#CICLO FINAL: ALTA EN SERVER
excel = globales.excel_results_path + configuracion.sesion + '.xlsx'
print("La ruta correcta del excel es: ", excel)

base_url = globales.base_url
print("Baseurl es: ", base_url)

sesion = configuracion.sesion
print("Sesión es: ", sesion)

directorio_remoto = base_url + sesion
print("Directorio remoto es: ", directorio_remoto)

print("Iniciando proceso de subida...")

#Sube todo
dataframe = postools.subirTodo(excel, sesion, directorio_remoto)

#Finaliza excel después de postproducción.
#Future: Ver si aún es necesario éste excel.
print("Si llegó al final, imprimiendo excel, donde excel es: ", configuracion.sesion + '.xlsx')
tools.df2Excel(dataframe, configuracion.sesion + '.xlsx')