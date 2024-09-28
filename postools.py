import servidor

def subirTodo():
    #Ready: ¿Volver uno solo a subirTodo y sube? ¿o cuál es la razón para separarlo?    
    #Respuesta: Ahora que lo optimizamos podemos darnos cuenta que es para separar conexión del resto de...
    #... las actividades.
    
    #Conexión al servidor.
    ssh, sftp = servidor.conecta()  
    
    #Subir el resultado al servidor y esperar respuesta que se guardará en la var resultado.
    servidor.sube(sftp)
    #FUTURE: Poner un while para que después de fallo continue el ciclo de seguir subiendo.

    #Future: que la conexión también se cierre ante interrupciones de excel.
    print("Cerrando conexión...")
    servidor.cierraConexion(ssh, sftp)