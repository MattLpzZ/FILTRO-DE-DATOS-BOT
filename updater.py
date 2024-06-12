import os
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox

def download_update():
    github_repo_url = "https://github.com/MattLpzZ/FILTRO-DE-DATOS-BOT"
    
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
            if file_url:  # Solo intentar descargar si hay un URL válido
                if os.path.exists(filename):
                    os.remove(filename)
                with requests.get(file_url) as r:
                    r.raise_for_status()  # Asegurarse de que no haya errores en la descarga
                    with open(filename, "wb") as f:
                        f.write(r.content)
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar la actualización: {e}")
        return False
    
    return True

def check_for_updates():
    current_version = "1.0.1"  # Cambia esto según la versión actual
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
            subprocess.Popen(["main.exe"])
            root.destroy()  # Cierra la ventana actual
            exit()  # Sale del proceso actual
        else:
            messagebox.showerror("Error", "Error al descargar la actualización.")
    else:
        messagebox.showinfo("Actualización", "No hay nuevas actualizaciones disponibles.")

def main():
    global root
    root = tk.Tk()
    root.title("Data Filter Bot by@MattLpzZ :>")

    frame = tk.Frame(root)
    frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)

    label = tk.Label(frame, text="Opciones de filtrado:")
    label.pack(anchor='w')

    global domain_var, country_var
    domain_var = tk.BooleanVar()
    country_var = tk.BooleanVar()

    domain_check = tk.Checkbutton(frame, text="Filtrar por Dominio", variable=domain_var)
    domain_check.pack(anchor='w')

    country_check = tk.Checkbutton(frame, text="Filtrar por País", variable=country_var)
    country_check.pack(anchor='w')

    button = tk.Button(frame, text="Filtrar Archivos", command=filter_files)
    button.pack(anchor='w')

    update_button = tk.Button(frame, text="Verificar Actualizaciones", command=check_for_updates)
    update_button.pack(anchor='w')

    version_label = tk.Label(frame, text="Versión: 1.0.1")
    version_label.pack(anchor='w')

    console_label = tk.Label(frame, text="Consola de Progreso:")
    console_label.pack(anchor='w')

    global console
    console = tk.Text(frame, height=15, width=50)
    console.pack(anchor='w')

    root.mainloop()

if __name__ == "__main__":
    main()