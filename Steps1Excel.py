import pretools
import configuracion.configuracion as configuracion

sesion = configuracion.sesion
filename = sesion + '.xlsx'

#Creación de directorio local que recibirá las imagenes resulados.
#Future: ¿Debería ir en éste orden? 
#pretools.creaDirectorioInicial(sesion)

# print("Creación de excel que contendrá los resultados.")
# respuesta = input("Presiona cualquier tecla para continuar: ")
# pretools.creaExcel(filename)

# print("A continuación descargaremos las imagenes del lote...")
# respuesta = input("Presiona cualquier tecla para continuar: ")
# pretools.descargaImagenes(sesion)

print("A continuación subiremos las imagenes SOURCES a mi servidor...")
respuesta = input("Presiona cualquier tecla para continuar: ")
#Future: Debería tener dos procesos separados: SUBIR/REGISTRAR.
pretools.subeSources()    
    