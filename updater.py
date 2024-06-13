import os
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox

def download_update():
    github_repo_url = "https://api.github.com/repos/MattLpzZ/FILTRO-DE-DATOS-BOT/contents/"
    
    try:
        response = requests.get(github_repo_url)
        response.raise_for_status()
        repo_contents = response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error al obtener información del repositorio: {e}")
        return False
    
    try:
        for item in repo_contents:
            file_url = item.get("download_url")
            filename = item["name"]
            if file_url:
                if os.path.exists(filename):
                    os.remove(filename)
                with requests.get(file_url) as r:
                    r.raise_for_status()
                    with open(filename, "wb") as f:
                        f.write(r.content)
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar la actualización: {e}")
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
        messagebox.showerror("Error", f"Error al obtener la versión más reciente: {e}")
        return False

    if latest_version > current_version:
        messagebox.showinfo("Actualización disponible", "Hay una nueva actualización disponible. El bot se actualizará y reiniciará.")
        if download_update():
            subprocess.Popen(["python", "main.py"])
            root.destroy()  # Cierra la ventana actual
            exit()  # Sale del proceso actual
        else:
            messagebox.showerror("Error", "Error al descargar la actualización.")
    else:
        messagebox.showinfo("Actualización", "No hay nuevas actualizaciones disponibles.")

#XXXXXXXXXXXXXXX


def main():
    global root
    root = tk.Tk()
    root.title("Actualizador del Data Filter Bot")

    frame = tk.Frame(root)
    frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)

    update_button = tk.Button(frame, text="Verificar Actualizaciones", command=check_for_updates)
    update_button.pack(anchor='w')

    root.mainloop()

if __name__ == "__main__":
    main()