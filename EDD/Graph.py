import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from EDD.Queue import Queue


class Graph:
    def __init__(self, V, visas, codes):
        self.V = V
        self.adj = [[float("inf") for _ in range(V)] for _ in range(V)]
        self.visas = visas
        self.codes = codes

    def add_edge(self, source, dest, cost):
        self.adj[source][dest] = cost
        self.adj[dest][source] = cost

    def vertex_min_cost(self, distances, visited):
        min_cost = float("inf")
        min_vertex = -1

        for vertex in range(self.V):
            if not visited[vertex] and distances[vertex] < min_cost:
                min_cost = distances[vertex]
                min_vertex = vertex

        return min_vertex

    def get_path(self, previous_Airports, source, dest):
        path = []

        while dest != source:
            path.append(self.codes[dest])
            dest = previous_Airports[dest]

        path.append(self.codes[source])
        path = path[::-1]
        return path

    def dijkstra(self, source, end_v, has_visa):
        previous_Airports = [-1] * self.V
        visited = [False] * self.V
        costs = [float("inf")] * self.V
        costs[source] = 0

        if self.visas[self.codes[source]] == True and not has_visa:
            return None, float("inf")

        for _ in range(self.V):
            vertex = self.vertex_min_cost(costs, visited)
            if vertex == -1:
                break

            visited[vertex] = True

            for neighbor in range(self.V):
                if self.adj[vertex][neighbor] != float("inf") and not visited[neighbor]:

                    if self.visas[self.codes[neighbor]] == True and not has_visa:
                        continue

                    new_cost = costs[vertex] + self.adj[vertex][neighbor]

                    if new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        previous_Airports[neighbor] = vertex

        final_path = self.get_path(previous_Airports, source, end_v)
        final_cost = costs[end_v]

        return final_path, final_cost

    def bfs_shortest_path(self, source, dest, has_visa):
        queue = Queue()
        queue.enqueue((source, [source], 0))
        visited = [False] * self.V

        if self.visas[self.codes[source]] == True and not has_visa:
            return None, 0, float("inf")

        while not queue.is_empty():
            current, path, total_cost = queue.dequeue()
            visited[current] = True

            for neighbor in range(self.V):
                if self.adj[current][neighbor] != float("inf") and not visited[neighbor]:

                    if self.visas[self.codes[neighbor]] == True and not has_visa:
                        continue

                    if neighbor == dest:
                        final_path = path + [neighbor]
                        final_path_codes = [self.codes[node]
                                            for node in final_path]
                        return final_path_codes, len(final_path) - 2, total_cost + self.adj[current][neighbor]

                    queue.enqueue(
                        (neighbor, path + [neighbor], total_cost + self.adj[current][neighbor]))

                    visited[neighbor] = True

        return None, 0, float("inf")

    def plot_graph(self):
        G = nx.Graph()
        for i in range(self.V):
            for j in range(self.V):
                if self.adj[i][j] != float("inf"):
                    G.add_edge(self.codes[i], self.codes[j],
                               weight=self.adj[i][j])

        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        node_colors = ['#ff9999' if self.visas[self.codes[i]]
                       == True else 'lightblue' for i in range(self.V)]

        nx.draw(G, pos, with_labels=True, labels={node: node for node in G.nodes()}, node_color=node_colors,
                node_size=500, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.2,
                                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7), verticalalignment='center')

        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Requiere Visa',
                                  markerfacecolor='#ff9999', markersize=10),
                           Line2D([0], [0], marker='o', color='w', label='No Requiere Visa',
                                  markerfacecolor='lightblue', markersize=10)]
        plt.legend(handles=legend_elements, loc='best')

        plt.show()


# //FIXME - Arreglar bug de plot. Cuando se selecciona CCS y SBH, el nodo destino no se pinta de naranja

    def plot_selected_path(self, path):
        G = nx.Graph()
        for i in range(self.V):
            for j in range(self.V):
                if self.adj[i][j] != float("inf"):
                    G.add_edge(self.codes[i], self.codes[j],
                               weight=self.adj[i][j])

        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        node_colors = ['#ff9999' if self.visas[self.codes[i]]
                       else 'lightblue' for i in range(self.V)]

        origin_node = self.codes.index(path[0])
        destination_node = self.codes.index(path[-1])
        node_colors[origin_node] = 'yellow'  # Nodo de origen
        node_colors[destination_node] = 'orange'  # Nodo de destino

        nx.draw(G, pos, with_labels=True, labels={node: node for node in G.nodes()},
                node_color=node_colors, edge_color='lightgrey', node_size=500,
                font_size=10, font_weight='bold')

        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               edge_color='lightgreen', width=2)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.2,
                                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7), verticalalignment='center')

        source_label = "Origen (Requiere Visa)" if self.visas[self.codes[origin_node]
                                                              ] else "Origen"
        dest_label = "Destino (Requiere Visa)" if self.visas[
            self.codes[destination_node]] else "Destino"

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Requiere Visa',
                   markerfacecolor='#ff9999', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='No Requiere Visa',
                   markerfacecolor='lightblue', markersize=10),
            Line2D([0], [0], marker='o', color='w', label=source_label,
                   markerfacecolor='yellow', markersize=10),
            Line2D([0], [0], marker='o', color='w', label=dest_label,
                   markerfacecolor='orange', markersize=10),
            Line2D([0], [0], color='lightgreen',
                   lw=2, label='Ruta Seleccionada')
        ]

        plt.legend(handles=legend_elements, loc='best')

        plt.show()

    def get_airports(self):
        return self.airports

    def get_visas(self):
        return self.visas

    def __str__(self):
        return f"""
        Number of Vertices: {self.V}
        Visas: {self.visas}
        Adjacency Matrix: {self.adj}
        """
