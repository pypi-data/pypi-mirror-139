import matplotlib.pyplot as plt
import networkx as nx
import ast


node_count = 0
labeldict = {}


def dfs(obj, parent, name):
    global node_count, labeldict
    if obj is None:
        return
    node_count += 1
    number = node_count
    G.add_node(number)
    labeldict[number] = type(obj).__name__
    if parent is not None:
        G.add_edge(parent, number, name=name, length=8)
    if isinstance(obj, list):
        for i in obj:
            dfs(i, number, "element")
        return
    if type(obj) == str:
        labeldict[number] += ": " + str(obj)
        return
    if type(obj) == int:
        labeldict[number] += ": " + str(obj)
        return
    attrs = obj.__dict__
    for key, val in attrs.items():
        arg = getattr(obj, key)
        if arg is None or arg == [] or arg == {}:
            continue
        dfs(arg, number, key)

G = nx.Graph()
def build_graph(filename):
    with open(filename, "r") as fin:
        func_ast = ast.parse(fin.read())
    dfs(func_ast, None, "root")

    pos = nx.spring_layout(G)
    edge_labels = {(u, v,): d['name'] for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, labels=labeldict, font_size=5)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5)
    fig = plt.gcf()
    fig.set_size_inches(25, 25)
    fig.savefig('artifacts/result.pdf')
