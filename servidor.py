import os
import configuracion.globales as globales
import tools
import paramiko
import configuracion.configuracion as configuracion 
import tools
import pandas as pd
import nycklar.nodes as nodes

#Future: Revisar cuanto se parece servidor a SulkuPypi para que lo conviertas en ello.
def conecta(): 

    #Digital Signature.
    ssh = paramiko.SSHClient()
    ssh.load_host_keys("nycklar/itrst")

    #Ahora obtendremos nuestra sk para poder entrar a ese servidor.
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

def sube(sftp):

  excel = globales.excel_results_path + configuracion.sesion + '.xlsx'
  #Primero extraemos el dataframe:
  dataframe = pd.read_excel(excel)  
 
  sesion = configuracion.sesion
  base_url = globales.base_url
  directorio_remoto = base_url + sesion

  print("Llegamos a servidor.sube y el directorio remoto o dirección donde se subirá todo es:", directorio_remoto)

  #Define ruta de la carpeta remota
  #Ésta es la carpeta fija de holocards.
  carpeta_remota = nodes.avaimentekijä
  print(f"La carpeta remota es: {carpeta_remota} y su tipo es: {type(carpeta_remota)}.")
  directorio_receptor = carpeta_remota + sesion
  print(f"El directorio receptor será entonces: {directorio_receptor} y su tipo es: {type(directorio_receptor)}")
  
  #Define ruta de la carpeta local donde se encuentran los resultados.
  carpeta_local = globales.imagenes_folder_resultados + sesion + '-results'


  try:       
        #Crea directorio
        print("Creando directorio, cuyo nombre será: ", directorio_receptor)
        #Si el directorio no existe, si lo está creando bien, checar después que problemas causa q ya exista.        
        sftp.mkdir(directorio_receptor)
        print("Directorio creado...")

  except Exception as e:
        # Mensaje de error
        print(f"Error al crear el directorio, probablemente ya existe: {e}")
  
  #AHORA NECESITAMOS QUE LA LISTA SALGA DEL EXCEL...
  print("Ahora vamos a obtener los resultados via la nueva función getNotLoaded()...")
  #Parámetros: dataframe, columna_filtro, texto_filtro, columna_destino, columna_source.
  #IMPORTANTE: getNotLoaded ya se puede usar para la subida de imagenes source.
  resultados = tools.getNotLoaded(dataframe, 'Diffusion Status', 'Completed', 'URL', 'File')

  tools.cicloSubidor(sftp, dataframe, resultados, carpeta_local, directorio_receptor, directorio_remoto)  
  
  
def cierraConexion(ssh, sftp):
  """
  Sube una carpeta local completa a una carpeta remota.

  Parameters:
    archivo (str): Contenido que será agregado a esa celda.

  Returns:
  dataframe:Regresa dataframe.
  """ 
  sftp.close()
  ssh.close()