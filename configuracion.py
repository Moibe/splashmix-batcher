#El dominio donde se presentan las imagenes guardadas.
base_url = "https://euroglitter.com/results/"
sesion = 'finalTest'
#Source list es false porque no viene de una lista de excel si no de un directorio con fotos.
source_list = True
#filename = 'iteracionesTest.xlsx' #El filename podría salir del nombre de la sesión.
filename = sesion + '.xlsx'


#Features Futuros
wait_awake = False #Lo dejaré en false pq en realidad, esperando o no, termina Full Process y hay que correr de nuevo.
waited = False
api_apagada = False
wait_time = 500