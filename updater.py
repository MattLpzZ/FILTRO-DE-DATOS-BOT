import os
import requests
import subprocess

def download_update():
    # URL del repositorio de GitHub
    github_repo_url = "https://api.github.com/repos/MattLpzZ/FILTRO-DE-DATOS-BOT/contents/"
    
    try:
        response = requests.get(github_repo_url)
        response.raise_for_status()
        repo_contents = response.json()
    except requests.exceptions.RequestException as e:
        print("Error al obtener información del repositorio:", e)
        return False
    
    try:
        for item in repo_contents:
            file_url = item["download_url"]
            filename = item["name"]
            if os.path.exists(filename):
                os.remove(filename)
            with requests.get(file_url) as r:
                with open(filename, "wb") as f:
                    f.write(r.content)
    except Exception as e:
        print("Error al descargar la actualización:", e)
        return False
    
    return True

def check_for_updates():
    current_version = "1.0.0"  # Cambia esto según la versión actual
    version_url = "https://raw.githubusercontent.com/MattLpzZ/FILTRO-DE-DATOS-BOT/main/version.txt"
    
    try:
        response = requests.get(version_url)
        response.raise_for_status()
        latest_version = response.text.strip()
    except requests.exceptions.RequestException as e:
        print("Error al obtener la versión más reciente:", e)
        return False

    if latest_version > current_version:
        return True
    else:
        return False

def main():
    if check_for_updates():
        print("Hay una nueva actualización disponible. El bot se actualizará y reiniciará.")
        if download_update():
            subprocess.Popen(["main.exe"])
            exit()
        else:
            print("Error al descargar la actualización.")
    else:
        print("No hay nuevas actualizaciones disponibles.")

if __name__ == "__main__":
    main()