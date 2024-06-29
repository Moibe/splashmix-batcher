import os
import time
import paramiko 
import postools
import nycklar.nodes as nodes

def conecta(): 

    #Digital Signature.
    ssh = paramiko.SSHClient()
    ssh.load_host_keys("nycklar/itrst")

    #Ahora obtendremos nuestra secret key para poder entrar a ese servidor.
    project_dir = os.getcwd()
    key_filename = os.path.join(project_dir, "nycklar", "go")

    ssh.connect(nodes.realm, username=nodes.master, key_filename=key_filename)
    sftp = ssh.open_sftp()

    print("Servidor conectado...")

    return ssh, sftp

def lee(sftp, caja): 
   
   #Ésta función lee el contenido de un archivo d
   # e texto.
    with sftp.open(caja, 'rb') as archivo:
      # Leer el contenido del archivo como bytes
      contenido_bytes = archivo.read()
      # Decodificar los bytes a Unicode usando la codificación UTF-8
      contenido = contenido_bytes.decode('utf-8')

      return contenido
    
def escribe(sftp, archivo, contenido):

  #Actualiza el nuevo valor en el servidor en modo escritura.
  with sftp.open(archivo, 'w') as archivo:
    # Escribir el contenido final en el archivo
    archivo.write(contenido)

  return "Contenido escrito"

def sube(sftp, dataframe, carpeta_local, directorio_receptor, complete_url):

  """
  Sube una carpeta local completa a una carpeta remota.

  Parameters:
    archivo (str): Contenido que será agregado a esa celda.

  Returns:
  dataframe:Regresa dataframe.
  """ 

  print("Llegamos a servidor.sube y complete_url es:", complete_url)

  try:       
        #Crea directorio
        print("Creando directorio, cuyo nombre será: ", directorio_receptor)
        #Si el directorio no existe, si lo está creando bien, checar después que problemas causa q ya exista.        
        sftp.mkdir(directorio_receptor)
        print("Directorio creado...")

  except Exception as e:
        # Mensaje de error
        print(f"Error al crear el directorio, probablemente ya existe: {e}")
                
  finally:
      pass
  
  # Subir los resultados al servidor remoto
  print("Vamos a repasar los archivos de la carpeta local que se encuentra en: ", carpeta_local)
  resultados = os.listdir(carpeta_local)

  #Para el conteo de avance en subida.
  contador = 0 
  cuantos = len(resultados)
  print("La cantidad de resultados son: ", cuantos)

  try:
        
        for imagen in resultados:
            
            print(f"Ahora estámos en la imagen número {contador} de {cuantos}.")
            time.sleep(1)
           
            print("La imagen de ésta vuelta es: ", imagen)
            print("Y el tipo de dicha imagen es string??: ", type(imagen)) #string?
            time.sleep(5)

            #Ahora extraeremos su ID: 
            segmentos = imagen.split(',')
            id = segmentos[0] + '.png'
            print("El id con el que estamos trabajando es: ", id)
            
            ruta_origen = os.path.join(os.getcwd(), carpeta_local, imagen)
            print(f"La RUTA_ORIGEN después del join quedó así: {ruta_origen} y su tipo es: {type(ruta_origen)}.")
            
            nuevo_directorio_receptor = directorio_receptor.replace("/", "\\")
            print("Así quedó el nuevo directorio receptor: ", nuevo_directorio_receptor)
                                   
            #Crear la ruta completa del archivo remoto
            #ruta_destino = os.path.join(directorio_receptor, imagen) #Así se van a holocards.
            ruta_destino = directorio_receptor + "\\" + imagen
            #ruta_destino = os.path.join(nuevo_directorio_receptor, imagen) #Así se va a moibe pq no encuentra nada.
            #ruta_destino = nuevo_directorio_receptor

            ruta_destino = ruta_destino.replace("\\", "/")
           
            print(f"La RUTA_DESTINO después del join quedó así: {ruta_destino} y su tipo es: {type(ruta_destino)}.")
                      
            #Sube la imagen.
            print(f"La ruta origen es: {ruta_origen}, y su tipo es: {type(ruta_origen)}.")
            print(f"La ruta destino es: {ruta_destino}, y su tipo es: {type(ruta_destino)}.")
            
            conjunto = imagen
            print(f"Ésto es conjunto: {conjunto} y éste es su tipo: {type(conjunto)}...")
            sftp.put(ruta_origen, ruta_destino)
            print("La imagen ha sido subida al servidor...")
            print("---")
            print("---")
            print("---")
            print("---")
            ruta_completa = complete_url + '/' + imagen
            #Si se ha subído correctamente, entonces actualiza el archivo de excel.
            postools.actualizaRow(dataframe, 'Name', id, 'URL', ruta_completa) 

        # Mensaje de confirmación
        return f"Archivo {ruta_origen} subido correctamente a {ruta_destino}."  
    
  except Exception as e:
        # Mensaje de error
        # Creo que aquí se corre el riesgo de que si falla un archivo en subir, se corta la producción. 
        # Revisar y corregir en caso de ser necesario.
        mensaje = f"OJO: Error al subir un archivo: {e}"
        print(mensaje)
        print("XXXXXXXX")
        print("XXXXXXXX")
        print("XXXXXXXX")
        print("XXXXXXXX")
        time.sleep(3)
        return f"OJO: Error al subir un archivo: {e}"
  finally: 
      contador += 1
  
def cierraConexion(ssh, sftp ):

  """
  Sube una carpeta local completa a una carpeta remota.

  Parameters:
    archivo (str): Contenido que será agregado a esa celda.

  Returns:
  dataframe:Regresa dataframe.
  """ 

  sftp.close()
  ssh.close()