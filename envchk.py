import os
import sys

if os.getenv('VIRTUAL_ENV'):
    env_name = os.path.basename(sys.prefix)
    print(f"Estás dentro del entorno virtual: {env_name}")
else:
    print("No estás dentro de un entorno virtual.")