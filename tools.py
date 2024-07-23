def obtenerArchivoOrigen(foto_path):
    """
    Obtiene el archivo original (fuente), basado en el archivo destino listado en el excel.

    Parameters:
    foto_path
    
    Returns:
    str: La ruta del archivo origen.
    """
    #foto_path = "203112-t3.webp"

    segmentos_guion = foto_path.split("-")
    cuantos_segmentos = len(segmentos_guion)
    # print(f"Hay {cuantos_segmentos} en segmentos_guion de la foto {foto_path}")

    # print(f"Presentando el último segmento: {segmentos_guion[cuantos_segmentos-1]}.")

    #Ahora divide por el punto a ese último segmento: 

    division_puntos = segmentos_guion[cuantos_segmentos-1].split(".")

    # print(f"Al que estoy buscando es a éste, el primer segmento: {division_puntos[0]} ")

    quitable = "-" + division_puntos[0]

    resultado_final = foto_path.split(quitable)

    union_final = resultado_final[0] + resultado_final[1]

    print(f"El resultado final es: {union_final} ")