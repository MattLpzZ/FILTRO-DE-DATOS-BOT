
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os
from datetime import datetime
#BOT 2
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
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        records = parse_data(file_path)
        output_path = save_to_excel(records, file_path)
        messagebox.showinfo("Success", f"Data successfully saved to {output_path}")

def main():
    root = tk.Tk()
    root.title("Text to Excel Converter")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Select a text file to convert to Excel:")
    label.pack(pady=10)

    button = tk.Button(frame, text="Select File", command=select_file)
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
