import os
import servidor 
import nycklar.nodes as nodes

remoto = nodes.avaimentekijä

print(remoto)
print(type(remoto))

# Get the absolute path of the local file 'white.png'
# Assuming the project root is the current working directory
local_path = os.path.join(os.path.dirname(__file__), 'white.png')

print("Ésto es localpath: ", local_path)
print("Y éste es su tipo: ", type(local_path))


#Conexión al servidor.
ssh, sftp = servidor.conecta()

print("ssh: ", ssh)
print("sftp: ", sftp)

sftp.put(local_path, remoto)