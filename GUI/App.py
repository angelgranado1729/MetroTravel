import tkinter as tk
from tkinter import ttk, messagebox

class App:
    def __init__(self, graph):
        self.root = tk.Tk()
        self.root.title("Metro Travel")
        self.graph = graph

        # Centrar la ventana principal
        self.center_window(self.root, 400, 200)

        self.origin_var = tk.StringVar()
        self.destination_var = tk.StringVar()
        self.visa_var = tk.BooleanVar()
        self.method_var = tk.StringVar(value="Menor Costo")

        # Frame for inputs
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(2, weight=1)

        ttk.Label(frame, text="Origen:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.origin_var).grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="Destino:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.destination_var).grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="Método:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        ttk.Radiobutton(frame, text="Menor Costo", variable=self.method_var, value="Menor Costo").grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(frame, text="Menor Escalas", variable=self.method_var, value="Menor Escalas").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)

        ttk.Checkbutton(frame, text="Tengo Visa", variable=self.visa_var).grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)

        ttk.Button(frame, text="Calcular Ruta", command=self.calculate_route).grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(frame, text="Ver Grafo", command=self.view_graph).grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)

    def center_window(self, window, width, height):
        # Obtén el tamaño de la pantalla
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calcula las coordenadas x e y para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Establece la geometría de la ventana
        window.geometry(f'{width}x{height}+{x}+{y}')

    def calculate_route(self):
        origin = self.origin_var.get().upper()
        destination = self.destination_var.get().upper()
        has_visa = self.visa_var.get()
        method = self.method_var.get()

        if origin not in self.graph.codes or destination not in self.graph.codes:
            messagebox.showerror("Error", "Origen o Destino no válidos.")
            return

        elif origin == destination:
            messagebox.showerror("Error", "Origen y Destino no pueden ser iguales.")
            return

        origin_index = self.graph.codes.index(origin)
        destination_index = self.graph.codes.index(destination)

        if method == "Menor Costo":
            path, total_cost = self.graph.dijkstra(origin_index, destination_index, has_visa)
            stops = -1
        else:
            path, stops, total_cost = self.graph.shortest_path(origin_index, destination_index, has_visa)

        if total_cost == float("inf"):
            messagebox.showerror("Error", "No se encontró una ruta.")
            return

        if method == "Menor Costo":
            message = f"La ruta más barata entre {origin} y {destination} es: {path}, con un costo de ${total_cost}"
        else:
            message = f"La ruta con menos escalas entre {origin} y {destination} es: {path}, con {stops - 1} escalas y un costo de ${total_cost}"

        print(message)
        messagebox.showinfo("Ruta Calculada", message)
        self.graph.plot_selected_path(path)

    def view_graph(self):
        self.graph.plot_graph()

    def run(self):
        self.root.mainloop()

