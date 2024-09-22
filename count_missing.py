import postools, configuracion.configuracion as configuracion, time
import pandas as pd

filename = configuracion.filename

dataframe = pd.read_excel('results_excel/' + 'girlsPositions.xlsx')

# Filter rows where 'Download Status' is 'Success' and 'Diffusion Status' is empty
df_images_ok = dataframe[dataframe['Download Status'] == 'Success'] 
#df_images_ok = dataframe[dataframe['Download Status'] == 'Success']

# Print the filtered DataFrame
print(df_images_ok)
print(len(df_images_ok))

#concurrent.futures._base.CancelledError

# Filter rows where 'Diffusion Status' is NaN and print them
#nan_df = df_images_ok[df_images_ok['Diffusion Status'].isna()]
#nan_df = df_images_ok[df_images_ok['Diffusion Status'] == 'concurrent.futures._base.CancelledError' & df_images_ok['Diffusion Status'].isna()]
nan_df = df_images_ok[(df_images_ok['Diffusion Status'].isna()) | (df_images_ok['Diffusion Status'] == 'concurrent.futures._base.CancelledError')]
print(nan_df)
print(len(nan_df))

columna_imagenes = nan_df['File'].to_list()

# Print the columna_imagenes list
print(columna_imagenes)
print(len(columna_imagenes))
