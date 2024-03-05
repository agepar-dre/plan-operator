import os
import shutil
import csv
import tkinter as tk
from tkinter import filedialog

def process_csv():
    file_path = file_path_entry.get()
    if not file_path:
        status_label.config(text="Por favor, selecione um arquivo.")
        return

    output_directory = output_directory_entry.get()
    if not output_directory:
        status_label.config(text="Por favor, selecione o diretório de saída.")
        return

    input_folder = os.path.join(output_directory, '1-INPUT')
    output_folder = os.path.join(output_directory, '2-OUTPUT')

    for folder in [input_folder, output_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    try:
        shutil.copy(file_path, input_folder)
    except shutil.Error as e:
        print(e)

    try:
        with open(os.path.join(input_folder, os.path.basename(file_path)), 'r') as file_in:
            csv_reader = csv.reader(file_in, delimiter=';')
            rows = list(csv_reader)

        target_column = 'SOMA'
        target_index = rows[0].index(target_column)  # indice da coluna a partir de 0

        for row in rows:
            try:
                value = int(row[target_index])
                row[target_index] = str(value + 10)
            except ValueError:
                pass  # Ignorar se não for possível converter para inteiro

        with open(os.path.join(output_folder, 'output_' + os.path.basename(file_path)), 'w', newline='') as file_out:
            csv_writer = csv.writer(file_out, delimiter=';')
            csv_writer.writerows(rows)

        status_label.config(text="Processo concluído com sucesso!")

        if open_output_directory.get():
            os.startfile(output_directory)  # Abre o diretório de saída se a checkbox estiver marcada

    except Exception as e:
        status_label.config(text=f"Erro: {str(e)}")

def choose_output_directory():
    output_directory = filedialog.askdirectory()
    if output_directory:
        output_directory_entry.delete(0, tk.END)
        output_directory_entry.insert(tk.END, output_directory)

# Criar a janela principal
root = tk.Tk()
root.title("Processamento de Arquivo CSV")

# Variável para rastrear o estado da checkbox
open_output_directory = tk.BooleanVar()
open_output_directory.set(False)

# Criar e posicionar os elementos da interface
file_path_label = tk.Label(root, text="Selecione o arquivo CSV:")
file_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

file_path_entry = tk.Entry(root, width=40)
file_path_entry.grid(row=0, column=1, padx=10, pady=5)

browse_button = tk.Button(root, text="Procurar", command=lambda: file_path_entry.insert(tk.END, filedialog.askopenfilename()))
browse_button.grid(row=0, column=2, padx=10, pady=5)

output_directory_label = tk.Label(root, text="Selecione o diretório de saída:")
output_directory_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

output_directory_entry = tk.Entry(root, width=40)
output_directory_entry.grid(row=1, column=1, padx=10, pady=5)

choose_directory_button = tk.Button(root, text="Escolher", command=choose_output_directory)
choose_directory_button.grid(row=1, column=2, padx=10, pady=5)

open_output_checkbox = tk.Checkbutton(root, text="Abrir diretório de saída após o processamento", variable=open_output_directory)
open_output_checkbox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

process_button = tk.Button(root, text="Processar", command=process_csv)
process_button.grid(row=3, column=1, padx=10, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

root.mainloop()
