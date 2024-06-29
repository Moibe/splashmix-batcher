import pretools

#Nombra la sesión para tener un nuevo directorio por cada sesión.
sesion = 'minitest1'
filename = 'minitest.xlsx'

pretools.creaDirectorioInicial(sesion)

dataframe = pretools.creaDataframe(filename)

pretools.procesaImagenes(sesion, dataframe)

pretools.df2Excel(dataframe, filename)