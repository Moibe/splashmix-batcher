#El dominio donde se presentan las imagenes guardadas.
base_url = "https://euroglitter.com/results/"

#IMPORTANTE, La sesión define de que excel (en el caso de source list) o de que directorio en imagenes/fuentes se obtendrá el material.
sesion = 'girlsPositions'
#Source list es false porque no viene de una lista de excel si no de un directorio con fotos.
source_list = False
#filename = 'iteracionesTest.xlsx' #El filename podría salir del nombre de la sesión.
filename = sesion + '.xlsx'
creacion =  "Hotgirl" #o "Superhero"

#Features Futuros
wait_awake = False #Lo dejaré en false pq en realidad, esperando o no, termina Full Process y hay que correr de nuevo.
waited = False
api_apagada = False
wait_time = 500

foto_path = 'Mila-t1.jpg'
