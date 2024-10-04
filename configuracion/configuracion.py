#IMPORTANTE, La sesión define de que excel (en el caso de source list) ...
# ... o de que directorio en imagenes/fuentes se obtendrá el material.
sesion = 'FixBatch'

#Source list es false porque no viene de una lista de excel si no de un directorio con fotos.
#Future: Cambiar por un concepto más entendible como source = excel, directory.
excel_list = True

#Future: Y por ende el filename solo se calculará si la elección fue excel.
#filename = sesion + '.xlsx'

creacion = "Superhero" #o Hotgirl.

#Importante, aunque no se usa, debes indicar que no está apagada para que no éntre a ese checador.
api_apagada = False

# #FUTURE: Features Futuros
# wait_awake = False #Lo dejaré en false pq en realidad, esperando o no, termina Full Process y hay que correr de nuevo.
# waited = False

# wait_time = 500

#Future: Que se puedan tener varias configuraciones a la vez, porque en el futuro se trabajará con varios archivos.
#Future: Ya no hay necesidad de que se agregue el nombre de la foto donde se cortó el proceso.
#Future: Hacer un log de las configuraciones o batches que haz hecho.