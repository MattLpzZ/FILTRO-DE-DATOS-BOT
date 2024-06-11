import tkinter as tk
import tkinter.filedialog as filedialog
import os
import re
import smtplib
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import subprocess

def download_update():
    # URL del repositorio de GitHub
    github_repo_url = "https://api.github.com/repos/MattLpzZ/FILTRO-DE-DATOS-BOT/contents/"
    
    # Obtener información sobre los archivos en el repositorio
    try:
        response = requests.get(github_repo_url)
        response.raise_for_status()
        repo_contents = response.json()
    except requests.exceptions.RequestException as e:
        print("Error al obtener información del repositorio:", e)
        return False
    
    # Descargar y sobrescribir los archivos locales con los archivos de la última versión en GitHub
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
    if download_update():
        subprocess.Popen(["python", "tu_aplicacion.py"])
        exit()

# Código de envío de correo electrónico

def send_email(filename):
    fromaddr = "boredoeleazar@gmail.com"  # Reemplaza con tu dirección de correo
    toaddr = "mantooscurogremio@gmail.com"  # Dirección de correo de destino
    password = "@Charlie.1962"  # Reemplaza con tu contraseña de correo

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Archivo filtrado"

    body = "Adjunto encontrarás el archivo filtrado."
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filename)}")
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Código de filtrado de archivos

def filter_files():
    filter_by_domain = domain_var.get()
    filter_by_country = country_var.get()

    if not filter_by_domain and not filter_by_country:
        console.insert(tk.END, "Por favor, selecciona al menos una opción de filtrado.\n")
        return

    filenames = filedialog.askopenfilenames(filetypes=[("Archivos de texto", "*.txt")])
    if not filenames:
        console.insert(tk.END, "No se seleccionaron archivos.\n")
        return

    known_domains = ['com', 'es', 'us']
    other_domains = []

        # Obtener el directorio raíz donde se encuentra el programa
    root_directory = os.getcwd()

    for filename in filenames:
        file_basename = os.path.basename(filename).split('.')[0]
        output_dir = os.path.join(root_directory, file_basename)
        os.makedirs(output_dir, exist_ok=True)

        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

    for filename in filenames:
        file_basename = os.path.basename(filename).split('.')[0]
        output_dir = os.path.join(os.getcwd(), file_basename)
        os.makedirs(output_dir, exist_ok=True)

        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if filter_by_country:
            countries = {}
            for line in lines:
                match = re.search(r'@([a-zA-Z0-9.-]+)\.([a-zA-Z]+)', line)
                if match:
                    country = match.group(2)
                    if country in known_domains:
                        if country not in countries:
                            countries[country] = []
                        countries[country].append(line)
                    else:
                        other_domains.append(line)

            for country, country_lines in countries.items():
                country_dir = os.path.join(output_dir, country)
                os.makedirs(country_dir, exist_ok=True)
                if filter_by_domain:
                    domains = {}
                    for line in country_lines:
                        match = re.search(r'@([a-zA-Z0-9.-]+)', line)
                        if match:
                            domain = match.group(1)
                            if domain not in domains:
                                domains[domain] = []
                            domains[domain].append(line)
                    
                    for domain, domain_lines in domains.items():
                        domain_dir = os.path.join(country_dir, domain)
                        os.makedirs(domain_dir, exist_ok=True)
                        domain_filename = os.path.join(domain_dir, f"{domain}.txt")
                        with open(domain_filename, "w", encoding="utf-8") as output_file:
                            output_file.writelines(domain_lines)
                            output_file.write("\n")
                        console.insert(tk.END, f"Se han identificado {len(domain_lines)} datos del dominio {domain} en {country}. Guardados en {domain_filename}.\n")
                else:
                    country_filename = os.path.join(country_dir, f"{country}.txt")
                    with open(country_filename, "w", encoding="utf-8") as output_file:
                        output_file.writelines(country_lines)
                        output_file.write("\n")
                    console.insert(tk.END, f"Se han identificado {len(country_lines)} datos del país {country}. Guardados en {country_filename}.\n")
        else:
            domains = {}
            for line in lines:
                match = re.search(r'@([a-zA-Z0-9.-]+)\.([a-zA-Z]+)', line)
                if match:
                    domain_extension = match.group(2)
                    domain = match.group(1)
                    if domain_extension in known_domains:
                        if domain not in domains:
                            domains[domain] = []
                        domains[domain].append(line)
                    else:
                        other_domains.append(line)

            for domain, domain_lines in domains.items():
                domain_dir = os.path.join(output_dir, domain)
                os.makedirs(domain_dir, exist_ok=True)
                domain_filename = os.path.join(domain_dir, f"{domain}.txt")
                with open(domain_filename, "w", encoding="utf-8") as output_file:
                    output_file.writelines(domain_lines)
                    output_file.write("\n")
                console.insert(tk.END, f"Se han identificado {len(domain_lines)} datos del dominio {domain}. Guardados en {domain_filename}.\n")

    if other_domains:
        other_domains_filename = os.path.join(output_dir, "otros_dominios.txt")
        with open(other_domains_filename, "w", encoding="utf-8") as output_file:
            output_file.writelines(other_domains)
            output_file.write("\n")
        console.insert(tk.END, f"Se han identificado {len(other_domains)} datos de dominios desconocidos. Guardados en {other_domains_filename}.\n")
        send_email(other_domains_filename)

    console.insert(tk.END, "Filtrado completo.\n")

# Interfaz de usuario de Tkinter
root = tk.Tk()
root.title("Email Filter Bot")

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)

label = tk.Label(frame, text="Opciones de filtrado:")
label.pack(anchor='w')

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

console_label = tk.Label(frame, text="Consola de Progreso:")
console_label.pack(anchor='w')

console = tk.Text(frame, height=15, width=50)
console.pack(anchor='w')

root.mainloop()