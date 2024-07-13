import os
import time
import paramiko
import configuracion 
import pretools, postools
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

def sube(sftp, dataframe, carpeta_local, directorio_receptor, foto_complete_url_dir):

  """
  Sube una carpeta local completa a una carpeta remota.

  Parameters:
    sftp
    dataframe
    carpeta_local
    directorio_receptor
    foto_complete_url_dir: Es la ruta del directorio local donde están todos los resultados, 

  Returns:
  dataframe:Regresa dataframe.
  """ 

  print("Llegamos a servidor.sube y foto_complete_url_dir o dirección donde se subirá todo es:", foto_complete_url_dir)

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
  cuantos = len(resultados) #Cantidad de imagenes que hay en ésa carpeta.
  print("La cantidad de resultados son: ", cuantos)

  try:
        
        for imagen in resultados:
            
            print(f"Ahora estámos en la imagen número {contador} de {cuantos}.")
            time.sleep(1)
           
            print("La imagen de ésta vuelta es: ", imagen)
                        
            #Origen
            ruta_origen = os.path.join(os.getcwd(), carpeta_local, imagen)
            print(f"La RUTA_ORIGEN después del join quedó así: {ruta_origen} y su tipo es: {type(ruta_origen)}.")
            time.sleep(1)

            #Destino
            nuevo_directorio_receptor = directorio_receptor.replace("/", "\\")
            print("Así quedó el nuevo directorio receptor: ", nuevo_directorio_receptor)

            #Ahora extraeremos su ID y su Take: 
            segmentos = imagen.split('-')
            id = segmentos[0] + '.png'  #El segmento 0 es el ID.
            print("Ahora que cambiamos a guión (dash) el id queda bien?: ", id)
            take_textual = segmentos[1] #Take=1
            segmentos_take = take_textual.split('=')
            take = segmentos_take[1] #segmento[1] es el número.

            print("El id con el que estamos trabajando es: ", id)
            print("La take es: ")
                                   
            #Crear la ruta completa del archivo remoto
            ruta_destino = directorio_receptor + "\\" + imagen
            #ruta_destino = os.path.join(nuevo_directorio_receptor, imagen) #Así se va a moibe pq no encuentra nada.
            #ruta_destino = nuevo_directorio_receptor

            ruta_destino = ruta_destino.replace("\\", "/")
           
            print(f"La RUTA_DESTINO después del join quedó así: {ruta_destino} y su tipo es: {type(ruta_destino)}.")
                      
            #Sube la imagen.
            print(f"La ruta origen es: {ruta_origen}, y su tipo es: {type(ruta_origen)}.")
            print(f"La ruta destino es: {ruta_destino}, y su tipo es: {type(ruta_destino)}.")
            
            sftp.put(ruta_origen, ruta_destino)
            print("La imagen ha sido subida al servidor...")
            print("---")
            print("---")
            print("---")
            
            ruta_completa = foto_complete_url_dir + '/' + imagen
            #Si se ha subído correctamente, entonces actualiza el archivo de excel.
            campo_receptor = 'URL'+ take
            print("El campo receptor quedó como: ", campo_receptor)
            postools.actualizaRow(dataframe, 'Name', id, campo_receptor, ruta_completa)

            contador =+ 1 

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
        
        return f"OJO: Error al subir un archivo: {e}"

  except KeyboardInterrupt:
      print("Interrumpiste el proceso de subida, guardaré el dataframe en el excel, hasta donde ibamos.")
      time.sleep(2)
      pretools.df2Excel(dataframe, configuracion.filename)

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