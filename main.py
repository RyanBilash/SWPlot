import csv

import matplotlib
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

DEFAULT_COLOR = "#4682B4"

COLOR_KEY = "p"

POSITION_SCALE = 1
RADIUS = 0.25
LABEL_OFFSET = -0.6

UNIQUE_MAP = None

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
    global UNIQUE_MAP
    if UNIQUE_MAP is None:
        UNIQUE_MAP = get_general_map(filename)

    return color_map_to_list(UNIQUE_MAP, graph)


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


def color_by_control(graph, filename):
    # TODO
    return None


def planet_pos(filename):
    file = open(filename)
    reader = csv.reader(file)
    mapping = {}
    for row in reader:
        mapping[row[0]] = [POSITION_SCALE * float(row[1]), POSITION_SCALE * float(row[2])]

    return mapping


def onclick(event):
    x, y = event.xdata, event.ydata

    # Radius is 0.25
    clicked = None
    smallest_distance = 999

    for key in pos:
        if key not in G.nodes():
            continue
        distance = ((x - pos[key][0]) ** 2) + ((y - pos[key][1]) ** 2)
        if distance < RADIUS and key is None:
            clicked = key
            smallest_distance = distance
        elif distance < RADIUS and key is not None:
            if distance < smallest_distance:
                clicked = key
                smallest_distance = distance

    print(clicked)

    # Add planets and do stuff
    add_hyperlanes(G, "data/hyperlanes/deep-core.csv")
    nx.set_node_attributes(G, planet_points, name="points")

    draw_graph(True, True)


def onkey(event):
    print(event.key)
    if event.key in ['p', 'u', 'c']:
        global COLOR_KEY
        COLOR_KEY = event.key

        draw_graph(True, True)


def draw_graph(change_colors=False, change_edges=False):
    global fig, colors
    fig.clf()
    plt.clf()

    # nodes
    if change_colors:
        global colors1, colors2
        colors1 = color_by_points(G, full_colors)
        # colors2 = color_map_to_list(full_colors, G)
        colors2 = define_colors(G, "data/colors-u.csv")
        match COLOR_KEY:
            case 'p':
                colors = colors1
            case 'u':
                colors = colors2
            case 'c':
                # colors = colors3
                colors = colors1

    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=colors)

    # edges
    if change_edges:
        global edges
        edges = [(u, v) for (u, v, d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, alpha=0.3)

    # node labels
    nx.draw_networkx_labels(G, label_pos, font_size=8, font_family="sans-serif")

    ax = plt.gca()
    # widgets.CheckButtons(ax,["Core","Rim","Unknown"])
    ax.margins(0.1)
    plt.axis("off")
    plt.tight_layout()
    #click_reg = fig.canvas.mpl_connect('button_press_event', onclick)
    #key_reg = fig.canvas.mpl_connect('key_press_event', onkey)

    fig.canvas.draw()


if __name__ == '__main__':
    G = nx.Graph()
    fig = plt.figure("Map", figsize=(10, 10))

    add_hyperlanes(G, "data/hyperlanes/limited.csv")
    add_hyperlanes(G, "data/hyperlanes/merc.csv")
    #add_hyperlanes(G, "data/hyperlanes/deep-core.csv")
    #add_hyperlanes(G, "data/hyperlanes/core-inner.csv")
    #add_hyperlanes(G, "data/hyperlanes/inner-rim.csv")
    #add_hyperlanes(G, "data/hyperlanes/hapan-space.csv")
    add_hyperlanes(G, "data/hyperlanes/northern.csv")
    #add_hyperlanes(G, "data/hyperlanes/slice.csv")
    #add_hyperlanes(G, "data/hyperlanes/western-reaches.csv")
    #add_hyperlanes(G, "data/hyperlanes/unknown.csv")

    pos = planet_pos("data/planet-loc.csv")
    label_pos = {}
    for key in pos.keys():
        label_pos[key] = (pos[key][0], pos[key][1] + LABEL_OFFSET)

    edges = [(u, v) for (u, v, d) in G.edges(data=True)]

    # Get point values, then put them to the colors or something
    planet_points = get_point_values(G, "data/planet-points.csv")
    full_colors = get_general_map("data/color-data.csv")

    colors1 = color_by_points(G, full_colors)
    colors2 = define_colors(G, "data/colors-u.csv")
    colors3 = color_by_control(G, "data/player-control.csv")
    colors = colors1

    draw_graph()
    plt.show()
