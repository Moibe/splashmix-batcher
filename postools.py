import os
import data.data_girls as data_girls
import time
import random
import pretools
import pandas as pd
import gradio_client
import servidor
import nycklar.nodes as nodes
import configuracion
from prompts import Prompt, Superhero, Hotgirl
import prompter
import tools
import globales


#Future, creo que Samples es irrelevante, checas.
def fullProcess(sesion, dataframe):
    """
    Ciclo completo de toma de imagen, llevado a HF, guardado en disco y actualización de archivo de Excel.

    Parameters:
    sesion
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.
    """
    #Future, que los dataframes sean independientes.
    #Primero extraemos el dataframe:
    #dataframe = pd.read_excel(filename)

    #Origen
    ruta_origen = os.path.join('imagenes', 'fuentes', sesion)    

    #Destino
    ruta_destino = sesion + "-results"
    target_dir = os.path.join('imagenes', 'resultados', ruta_destino)

    #En caso de no existir el directorio destino, lo creará.
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # columna_imagenes = tools.preparaColumnaImagenes(dataframe, inicial)
    # print("Ya estoy de nuevo afuera, Tengo el resultado de columna_imagenes, que es:")
    # print(columna_imagenes)

    #Count Missing también devuelve una columna de imagenes, pero basada en las que no han sido procesadas.
    #Dejando fuera a las completadas y a las que tuvieron error. Ésto evita tener que hacer el proceso de preparar ...
    #... Columnas basado en el archivo donde se quedó. Simplemente hará todas aquellas que no se han procesado!
    columna_imagenes = tools.getMissing()
    

    tools.carruselStable(columna_imagenes, ruta_origen, target_dir, dataframe)
 
def stableDiffuse(client, imagenSource, imagenPosition, prompt):
    
    #Los dos iguales.
    #Revisar si se puede subir el hf_token.

    #Hacer primer contacto con API, ésto ayudará a saber si está apagada y prenderla automáticamente.

    try:
        #Usando Moibe Splashmix
        print("Estoy adentro, donde se usaba el cliente...")
        #ÉSTE CLIENTE YA NO SE USA PORQUE SE CARGABA CADA VEZ Y CADA VEZ.
        #client = gradio_client.Client("Moibe/splashmix", hf_token=nodes.splashmix_token)


    except Exception as e:
        print("API apagada o pausada...", e)
        print("Revisar si el datafame está vivo a éstas alturas...:", )
    
        #Analiza e para definir si está apagada o pausada, cuando está pausada, no debes esperar pq nada cambiará.
        #Si e tiene la palabra PAUSED.
        print("Reiniciandola, vuelve a correr el proceso en 10 minutos.")
        print("ZZZZZZZ")
        print("ZZZZZZZ")
        print("ZZZZZZZ")
        #No podemos hacer break porque no es un loop.
        #Por eso hago un return para que se salga de stablediffuse.
        return "api apagada" # o regresa api pausada.
    
    #Ahora correr el proceso central de Stable Diffusion.
    try:

        print("Ahora estoy ya en el predict...")
        
        result = client.predict(
                imagenSource,
                imagenPosition,
                prompt=prompt,
                negative_prompt="(lowres, low quality, worst quality:1.2), (text:1.2), watermark, (frame:1.2), deformed, ugly, deformed eyes, blur, out of focus, blurry, deformed cat, deformed, photo, anthropomorphic cat, monochrome, pet collar, gun, weapon, 3d, drones, drone, buildings in background",
                style_name="(No style)", #ver lista en styles.txt
                num_steps=30,
                identitynet_strength_ratio=0.8,
                adapter_strength_ratio=0.8,
                pose_strength=0.4,
                canny_strength=0.4,
                depth_strength=0.4,
                controlnet_selection=["pose"], #pueden ser ['pose', 'canny', 'depth']
                guidance_scale=5,
                #seed=43,
                seed=42, #Wow deje una seed fija desde siempre, por eso con las mismas características creará lo mismo. Está bien!
                scheduler="EulerDiscreteScheduler",
                enable_LCM=False,
                enhance_face_region=True,
                api_name="/generate_image"
        )
        return result

    except Exception as e:
        print("Hubo un error, recuerda éste prompt...", e)
        print("Aquí llega cuando la imagen no existe, no cuando no se pudo procesar, revisar si eso llega al excel, la e sería: ", e)
        #No está llegando al excel, pero no es necesario porque cuando se sale llega a la línea: 364
        print("XXXXX")
        print("XXXXX")
        print("XXXXX")
        return e
      
def guardarResultado(dataframe, result, filename, ruta_final, message):
    """
    Guarda el resultado con una nomenclatura específica. Y lo guarda en disco.

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.
    result
    foto_dir
    take
    shot
    estilo
    ruta_final
    message: el mensaje textual que irá en la columna stable diffusion: si fue error el error, si no: Image Processed.

    Returns:
    bool: True si se guardó el archivo correctamente.
    """
    
    #Aquí guardará la imagen.
    #Ésta parte solo debe hacerla si no viene de error. 

    print("HOY: Estamos en guardar Resultado, y el mensaje que recibimos como parámetro es: ", message)
    ruta_total = ""
    ruta_absoluta = ""

    if message == "Completed":
        #ENTONCES SI HAY UNA IMAGEN QUE GUARDAR EN DISCO DURO.
        
        ruta_total = os.path.join(ruta_final, filename)
        print("El resultado del SD fue exitoso, y su ruta total es/será: ", ruta_total)
        raiz_pc = os.getcwd()
        ruta_absoluta = os.path.join(raiz_pc, ruta_total)
        print("Local path:", ruta_absoluta)
                
        ruta_imagen_local = result[0] 
        print("La ruta de gradio en result[0] es: ", ruta_imagen_local)
        
        #IMPORTANTE, GUARDANDO EN DISCO DURO.
        with open(ruta_imagen_local, "rb") as archivo_lectura:
            contenido_imagen = archivo_lectura.read()	

        with open(ruta_total, "wb") as archivo_escritura:
            archivo_escritura.write(contenido_imagen)
            print(f"Imagen guardada correctamente en: {ruta_total}")
            print("Estamos por actualizar excel...")
            
    #FUTURE: Ésto se tiene que hacer dinámicamente.

    #Después, haya o no guardado en disco duro, registrará que terminó en el excel.

    #actualiza Row actualiza una sola row.
    print("Estoy por actualizarRow y el mensaje es:", message)
    print("y su filename (índice) es: ", filename)
    
    #Sin problema ya puede actualizar el respectivo DiffusionStatus porque siempre está presente.
    tools.actualizaRow(dataframe, 'File', filename, 'Diffusion Status', message)      
    tools.actualizaRow(dataframe, 'File', filename, 'Direccion', ruta_absoluta)

    #Es esto la línea universal para guardar el excel? = Si, si lo es :) 
    pretools.df2Excel(dataframe, configuracion.filename)
     

def subirTodo(excel, sesion, directorio_remoto):

    #Primero extraemos el dataframe:
    dataframe = pd.read_excel(excel)  
    
    #Conexión al servidor.
    ssh, sftp = servidor.conecta()
        
    #Define ruta de la carpeta remota
    #Ésta es la carpeta fija de holocards.
    carpeta_remota = nodes.avaimentekijä
    print(f"La carpeta remota es: {carpeta_remota} y su tipo es: {type(carpeta_remota)}.")
    directorio_receptor = carpeta_remota + sesion
    print(f"El directorio receptor será entonces: {directorio_receptor} y su tipo es: {type(directorio_receptor)}")
    
    #Define ruta de la carpeta local donde se encuentran los resultados.
    carpeta_local = 'imagenes\\resultados\\' + sesion + '-results'
    
    #Subir el resultado al servidor y esperar respuesta que se guardará en la var resultado.
    servidor.sube(sftp, dataframe, carpeta_local, directorio_receptor, directorio_remoto)
    print("Salí de sube...")
    
    servidor.cierraConexion(ssh, sftp)

    return dataframe