import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class FileSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Seleccionar Archivos CSV")

        self.flights_file = None
        self.visas_file = None
        self.airports_file = None

        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Seleccionar archivos CSV:").grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Button(frame, text="Seleccionar Vuelos", command=self.select_flights_file).grid(row=1, column=0, pady=5)
        self.flights_label = ttk.Label(frame, text="No seleccionado")
        self.flights_label.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        ttk.Button(frame, text="Seleccionar Visas", command=self.select_visas_file).grid(row=2, column=0, pady=5)
        self.visas_label = ttk.Label(frame, text="No seleccionado")
        self.visas_label.grid(row=2, column=1, columnspan=2, sticky=tk.W)

        ttk.Button(frame, text="Seleccionar Aeropuertos", command=self.select_airports_file).grid(row=3, column=0, pady=5)
        self.airports_label = ttk.Label(frame, text="No seleccionado")
        self.airports_label.grid(row=3, column=1, columnspan=2, sticky=tk.W)

        ttk.Button(frame, text="Continuar", command=self.validate_files).grid(row=4, column=0, columnspan=3, pady=10)

    def select_flights_file(self):
        self.flights_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.flights_label.config(text=self.flights_file if self.flights_file else "No seleccionado")

    def select_visas_file(self):
        self.visas_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.visas_label.config(text=self.visas_file if self.visas_file else "No seleccionado")

    def select_airports_file(self):
        self.airports_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.airports_label.config(text=self.airports_file if self.airports_file else "No seleccionado")

    def validate_files(self):
        if not (self.flights_file and self.visas_file and self.airports_file):
            messagebox.showerror("Error", "Debe seleccionar los tres archivos CSV.")
            return

        if not (self.validate_csv(self.flights_file, ['origin', 'destination', 'cost']) and
                self.validate_csv(self.visas_file, ['airport', 'visa_required']) and
                self.validate_csv(self.airports_file, ['code', 'name'])):
            messagebox.showerror("Error", "Uno o más archivos no tienen el formato esperado.")
            return

        self.root.destroy()

    def validate_csv(self, file_path, expected_headers):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            return headers == expected_headers

def start_file_selector():
    root = tk.Tk()
    selector = FileSelector(root)
    root.mainloop()
    return selector.flights_file, selector.visas_file, selector.airports_file
