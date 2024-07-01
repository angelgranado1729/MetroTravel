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

        if self.visas[self.codes[source]] and not has_visa:
            return None, float("inf")

        for _ in range(self.V):
            vertex = self.vertex_min_cost(costs, visited)
            if vertex == -1:
                break

            visited[vertex] = True

            for neighbor in range(self.V):
                if self.adj[vertex][neighbor] != float("inf") and not visited[neighbor]:

                    if self.visas[self.codes[neighbor]] and not has_visa:
                        continue

                    new_cost = costs[vertex] + self.adj[vertex][neighbor]

                    if new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        previous_Airports[neighbor] = vertex

        final_path = self.get_path(previous_Airports, source, end_v)
        final_cost = costs[end_v]

        return final_path, final_cost

# // FIXME - USAR DIJSKTRA PARA MENOR CANTIDAD DE ESCALAS
    def shortest_path(self, source, end_v, has_visa):
        previous_Airports = [-1] * self.V
        visited = [False] * self.V
        # ruta, escalas, costo
        auxList = [([self.codes[source]], 1, 0)]

        if self.visas[self.codes[source]] and not has_visa:
            return None, 0, float("inf")

        while len(auxList) > 0:
            auxList.sort(key=lambda x: x[1])
            path, stops, cost = auxList.pop(0)
            current = self.codes.index(path[-1])

            if current == end_v:
                return path, stops, cost

            visited[current] = True

            for neighbor in range(self.V):
                if self.adj[current][neighbor] != float("inf") and not visited[neighbor]:
                    if has_visa or not self.visas[self.codes[neighbor]]:
                        auxList.append(
                            (path + [self.codes[neighbor]], stops + 1, cost + self.adj[current][neighbor]))

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

    def plot_selected_path(self, path):
        G = nx.Graph()
        for i in range(self.V):
            for j in range(self.V):
                if self.adj[i][j] != float("inf"):
                    G.add_edge(self.codes[i], self.codes[j],
                               weight=self.adj[i][j])

        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')

        nx.draw(G, pos, with_labels=True, labels={node: node for node in G.nodes()}, node_color='lightgray',
                node_size=500, font_size=10, font_weight='bold')

        nx.draw_networkx_edges(G, pos, edgelist=[(
            path[i], path[i + 1]) for i in range(len(path) - 1)], edge_color='lightgreen', width=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.2,
                                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7), verticalalignment='center')

        node_colors = []

        for node in G.nodes():
            if node in path:
                if self.visas[node] == True and node != path[0] and node != path[-1]:
                    node_colors.append('#ff9999')

                elif node == path[0]:
                    node_colors.append('yellow')

                elif node == path[-1]:
                    node_colors.append('orange')

                else:
                    node_colors.append('lightblue')

            else:
                node_colors.append('lightgray')

        nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(),
                               node_color=node_colors, node_size=500)

        scr_label = "Origen (Requiere Visa)" if self.visas[path[0]
                                                           ] == True else "Origen"
        dest_label = "Destino (Requiere Visa)" if self.visas[path[-1]
                                                             ] == True else "Destino"

        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Requiere Visa',
                                  markerfacecolor='#ff9999', markersize=10),
                           Line2D([0], [0], marker='o', color='w', label='No Requiere Visa',
                                  markerfacecolor='lightblue', markersize=10),
                           Line2D([0], [0], color='lightgreen',
                                  lw=2, label='Ruta Recomendada'),
                           Line2D([0], [0], marker='o', color='w', label=scr_label,
                                  markerfacecolor='yellow', markersize=10),
                           Line2D([0], [0], marker='o', color='w', label=dest_label,
                                  markerfacecolor='orange', markersize=10)]

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
