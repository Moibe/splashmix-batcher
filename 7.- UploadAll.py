import postools, configuracion.configuracion as configuracion, configuracion.globales as globales

#CICLO FINAL: ALTA EN SERVER
excel = globales.excel_results_path + configuracion.sesion + '.xlsx'
print("Iniciando proceso de subida...")
#Sube todo
postools.subirTodo(excel)