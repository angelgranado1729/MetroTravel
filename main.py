from Data.Data import Data
from EDD.Graph import Graph
from GUI.App import App


def main():
    data = Data()
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
