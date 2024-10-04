import pretools
import configuracion.configuracion as configuracion

sesion = configuracion.sesion
filename = sesion + '.xlsx'

#Creación de directorio local que recibirá las imagenes resulados.
#Future: ¿Debería ir en éste orden? 
#pretools.creaDirectorioInicial(sesion)

print("Creación de excel que contendrá los resultados.")
respuesta = input("Presiona cualquier tecla para continuar: ")
pretools.creaExcel(filename)

    