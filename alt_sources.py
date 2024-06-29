import csv
import os
import requests
import time
from io import BytesIO

# Define a blank image placeholder (replace with your actual blank image data)
imagen_en_blanco = BytesIO(b'')
sesion = "test"

def getImages():
    with open('archivo.csv', 'r') as csvfile, open('resultados.csv', 'w', newline='') as results_file:
        reader = csv.reader(csvfile)
        writer = csv.writer(results_file)

        # Write CSV header row with new "ID" column
        writer.writerow(['ID', 'URL', 'Status'])

        next(reader, None)  # Ignore header row

        for row in reader:
            url = row[0]

            # Extract filename from URL
            filename = os.path.dirname(url)
            partes = filename.split('image/')
            siguiente = partes[1].split('/')
            final_filename = f"{siguiente[0]}"

            # Generate unique ID based on filename
            image_id = final_filename  # Or use a more robust ID generation method

            # Create 'photos' directory if it doesn't exist
            photos_dir = sesion
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)

            # Attempt to download the image
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(f'{sesion}/{final_filename}.png', 'wb') as f:
                        f.write(response.content)
                    download_status = 'Success'
                    print(f"Image '{final_filename}' downloaded successfully.")
                else:
                    raise Exception(f"Error downloading image: {url} (Status code: {response.status_code})")
            except Exception as e:
                download_status = f"Error: {response.status_code}"
                print(f"Error downloading image: {url} - {e}")

            # Write URL, ID, and download status to results.csv
            writer.writerow([image_id, url, download_status])

            # Save a blank image as an alternative if download fails
            if download_status == 'Error':
                with open(f'photos/{final_filename}.png', 'wb') as f:
                    f.write(imagen_en_blanco.read())
                print(f"Blank image '{final_filename}' saved as an alternative.")

            # Add a slight delay to avoid accidental downloads
            #time.sleep(1)

if __name__ == '__main__':
    getImages()