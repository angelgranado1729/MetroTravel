from Data.Data import Data
from EDD.Graph import Graph
from GUI.App import App
from Data.FileSelector import start_file_selector

def main():
    flights_file, visas_file, airports_file = start_file_selector()
    
    if not (flights_file and visas_file and airports_file):
        print("No se seleccionaron archivos. Saliendo del programa.")
        return

    data = Data(flights_file, visas_file, airports_file)
    graph = Graph(len(data.vertices), data.visas, data.codes)

    for flight in data.flights:
        source = data.vertices[flight[0]]
        dest = data.vertices[flight[1]]
        cost = flight[2]
        graph.add_edge(source, dest, cost)

    app = App(graph)
    app.run()

if __name__ == "__main__":
    main()