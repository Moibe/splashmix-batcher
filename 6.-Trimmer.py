import tools
import pandas as pd
import configuracion.globales as globales
import configuracion.configuracion as configuracion 

excel = globales.excel_results_path + configuracion.sesion + '.xlsx'
#Primero extraemos el dataframe:
dataframe = pd.read_excel(excel)  

# Eliminar las columnas
columnas_a_eliminar = ['Source Path', 'Name', 'File', 'File Path', 'style', 'subject', 'Shot']
dataframe.drop(columnas_a_eliminar, axis=1, inplace=True)

#Future: Considera que si cambia el objeto de creación, deberás cambiar el trimmer,
#...investiga si se pueden eliminar de un punto en adelante.

# Guardar el DataFrame en un nuevo archivo Excel
tools.df2Excel(dataframe, configuracion.sesion + 'deliver.xlsx')