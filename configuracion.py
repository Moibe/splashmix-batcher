#El dominio donde se presentan las imagenes guardadas.
base_url = "https://euroglitter.com/results/"

#IMPORTANTE, La sesión define de que excel (en el caso de source list) ...
# ... o de que directorio en imagenes/fuentes se obtendrá el material.
sesion = 'firstBatch'

#Source list es false porque no viene de una lista de excel si no de un directorio con fotos.
#Future: Cambiar por un concepto más entendible como source = excel, directory.
source_list = True

#Future: Y por ende el filename solo se calculará si la elección fue excel.
filename = sesion + '.xlsx'
creacion = "Superhero" #o Hotgirl.

#Features Futuros
wait_awake = False #Lo dejaré en false pq en realidad, esperando o no, termina Full Process y hay que correr de nuevo.
waited = False
api_apagada = False
wait_time = 500
