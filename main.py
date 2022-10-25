import csv

import networkx as nx
import matplotlib.pyplot as plt

DEFAULT_COLOR = "#4682B4"

COLOR_UNIQUE = True


def add_hyperlanes(graph, filename):
    file = open(filename)
    reader = csv.reader(file)

    for row in reader:
        for i in range(len(row) - 1):
            graph.add_edge(row[i], row[i + 1])


def get_point_values(graph, filename):
    planet_map = get_general_map(filename)

    nx.set_node_attributes(graph, planet_map, name="points")

    return planet_map


def define_colors(graph, filename):
    colors = get_general_map(filename)

    return color_map_to_list(colors, graph)


def color_map_to_list(colors, graph):
    list_colors = []

    for key in graph.nodes():
        if key in colors.keys():
            list_colors.append(colors[key])
        else:
            list_colors.append(DEFAULT_COLOR)

    return list_colors


def get_general_map(filename):
    file = open(filename)
    reader = csv.reader(file)
    mapping = {}

    for row in reader:
        mapping[row[0]] = row[1]

    return mapping


def color_by_points(graph, point_color):
    list_colors = []
    for key in graph.nodes():
        if graph.nodes[key]["points"] in point_color.keys():
            list_colors.append(point_color[graph.nodes[key]["points"]])
        else:
            list_colors.append(DEFAULT_COLOR)

    return list_colors


if __name__ == '__main__':
    G = nx.Graph()

    """
    G.add_edge("Coruscant", "Anaxes")
    G.add_edge("Coruscant", "Empress Teta")
    G.add_edge("Tython", "Empress Teta")
    G.add_edge("Byss", "Empress Teta")
    G.add_edge("Coruscant", "Borleias")
    G.add_edge("Anaxes", "Alderaan")
    G.add_edge("Anaxes", "Carida")
    G.add_edge("Anaxes", "Chandrila")
    G.add_edge("Ilum", "Metellos")
    G.add_edge("Metellos", "Coruscant")
    G.add_edge("Borleias", "Dorin")
    G.add_edge("Iridonia", "Dorin")
    G.add_edge("Glee Anselm", "Dorin")
    G.add_edge("Ord Mantell", "Dorin")
    G.add_edge("Ord Mantell", "Orinda")
    G.add_edge("Mygeeto", "Orinda")
    G.add_edge("Muunilist", "Orinda")
    G.add_edge("Muunilist", "Bastion")
    G.add_edge("Mygeeto", "Dantooine")
    G.add_edge("Mygeeto", "Agamar")
    G.add_edge("Ord Mantell", "Ithor")
    G.add_edge("Agamar", "Ithor")
    G.add_edge("Champala", "Anaxes")
    G.add_edge("Champala", "Corsin")
    G.add_edge("Corsin", "Taris")
    G.add_edge("Dathomir", "Taris")
    G.add_edge("Agamar", "Ord Cestus")
    G.add_edge("Tangrene", "Ord Cestus")
    G.add_edge("Tangrene", "Serenno")
    G.add_edge("Telos IV", "Serenno")
    G.add_edge("Taris", "Serenno")
    G.add_edge("Yavin IV", "Serenno")
    G.add_edge("Yavin IV", "Korriban")
    G.add_edge("Vjun", "Ord Cestus")
    G.add_edge("Rhen Var", "Vjun")
    G.add_edge("Rhen Var", "Felucia")
    G.add_edge("Florrum", "Felucia")
    G.add_edge("Ossus", "Felucia")
    G.add_edge("Roche", "Felucia")
    G.add_edge("Roche", "Contruum")
    G.add_edge("Obroa-skai", "Contruum")
    G.add_edge("Carida", "Contruum")
    G.add_edge("Obroa-skai", "Corsin")
    G.add_edge("Kuat", "Anaxes")
    G.add_edge("Rendili", "Coruscant")
    G.add_edge("Rendili", "Corellia")
    G.add_edge("Alderaan", "Commenor")
    G.add_edge("Duro", "Corellia")
    G.add_edge("Devaron", "Corellia")
    G.add_edge("Devaron", "Fondor")
    G.add_edge("Abregado-rae", "Fondor")
    G.add_edge("Thyferra", "Fondor")
    G.add_edge("Devaron", "Yag'Dhul")
    G.add_edge("Thyferra", "Yag'Dhul")
    G.add_edge("Qat Chrystac", "Yag'Dhul")
    G.add_edge("Qat Chrystac", "Eriadu")
    G.add_edge("Takodana", "Yag'Dhul")
    G.add_edge("Takodana", "Cerea")
    G.add_edge("Bespin", "Cerea")
    G.add_edge("Endor", "Cerea")
    G.add_edge("Endor", "Bakura")
    G.add_edge("Bespin", "Hoth")
    G.add_edge("Yag'Dhul", "Koori IV")
    G.add_edge("Yag'Dhul", "Hoth")
    G.add_edge("Yag'Dhul", "Malastare")
    G.add_edge("Sullust", "Malastare")
    G.add_edge("Hoth", "Koori IV")
    G.add_edge("Sullust", "Eriadu")
    G.add_edge("Mustafar", "Eriadu")
    G.add_edge("Mustafar", "Polis Massa")
    G.add_edge("Bith", "Eriadu")
    G.add_edge("Dagobah", "Eriadu")
    G.add_edge("Utapau", "Eriadu")
    G.add_edge("Naboo", "Malastare")
    """

    add_hyperlanes(G, "data/hyperlanes/limited.csv")
    add_hyperlanes(G, "data/hyperlanes/merc.csv")
    add_hyperlanes(G, "data/hyperlanes/unknown.csv")
    seed = 21
    # print(G.nodes)

    edges = [(u, v) for (u, v, d) in G.edges(data=True)]

    pos = nx.spring_layout(G, seed=seed)  # positions for all nodes - seed for reproducibility
    label_pos = {}
    for key in pos.keys():
        label_pos[key] = (pos[key][0], pos[key][1] - 0.1)

    # Get point values, then put them to the colors or something
    get_point_values(G, "data/planet-points.csv")

    colors1 = color_by_points(G, get_general_map("data/color-data.csv"))
    colors2 = define_colors(G, "data/colors-u.csv")

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color=colors1)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.3)

    # node labels
    nx.draw_networkx_labels(G, label_pos, font_size=5, font_family="sans-serif")

    ax = plt.gca()
    ax.margins(0.1)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
