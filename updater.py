import os
import requests
import zipfile
import shutil

GITHUB_REPO = "https://github.com/tu_usuario/tu_repositorio"
LOCAL_PATH = "c:\\ruta\\a\\tu\\proyecto"
VERSION_FILE = "version.txt"

def get_latest_version():
    url = f"{GITHUB_REPO}/raw/main/{VERSION_FILE}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    return None

def download_and_extract_latest():
    zip_url = f"{GITHUB_REPO}/archive/refs/heads/main.zip"
    response = requests.get(zip_url)
    if response.status_code == 200:
        with open("latest.zip", "wb") as f:
            f.write(response.content)
        with zipfile.ZipFile("latest.zip", 'r') as zip_ref:
            zip_ref.extractall("latest")
        os.remove("latest.zip")

        # Copiar archivos a la ruta del proyecto
        src_folder = os.path.join("latest", "nombre_del_repositorio-main")
        for item in os.listdir(src_folder):
            s = os.path.join(src_folder, item)
            d = os.path.join(LOCAL_PATH, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)
        shutil.rmtree("latest")

if __name__ == "__main__":
    latest_version = get_latest_version()
    if latest_version and latest_version != current_version:
        print("Nueva versión disponible. Actualizando...")
        download_and_extract_latest()
        print("Actualización completada. Reinicia el programa.")
    else:
        print("No hay nuevas actualizaciones disponibles.")
