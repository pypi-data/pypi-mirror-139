import networkx as nx
import ast
import matplotlib.pyplot as plt
import re


def to_camelcase(string):
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()


def transform_ast(code_ast):
    if isinstance(code_ast, ast.AST):
        node = {to_camelcase(k): transform_ast(getattr(code_ast, k)) for k in code_ast._fields}
        node['node_type'] = to_camelcase(code_ast.__class__.__name__)
        return node
    elif isinstance(code_ast, list):
        return [transform_ast(el) for el in code_ast]
    else:
        return code_ast


cnt = 0


def dfs(v):
    global cnt
    prev_cnt = cnt - 1
    for key in v.keys():
        if key == 'node_type':
            return
        if isinstance(v[key], list):
            G.add_node(cnt, name="[list]")
            G.add_edge(prev_cnt, cnt, name=key)
            cnt += 1
            list_cnt = cnt - 1
            for i in range(len(v[key])):
                if isinstance(v[key][i], str):
                    G.add_node(cnt, name=v[key][i])
                    G.add_edge(list_cnt, cnt, name=i)
                    cnt += 1
                else:
                    G.add_node(cnt, name=v[key][i]['node_type'])
                    G.add_edge(list_cnt, cnt, name=i)
                    cnt += 1
                    dfs(v[key][i])
        elif isinstance(v[key], dict):
            G.add_node(cnt, name=v[key]['node_type'])
            G.add_edge(prev_cnt, cnt, name=key)
            cnt += 1
            dfs(v[key])
        else:
            G.add_node(cnt, name=v[key])
            G.add_edge(prev_cnt, cnt, name=key)
            cnt += 1


if __name__ == "__main__":
    with open("fib_func.py", "r") as source:
        tree = ast.parse(source.read())
    G = nx.Graph()
    G.add_node(0, name="module")
    cnt = 1
    graph_dict = transform_ast(tree)
    # print(ast.dump(tree))
    # print(graph_dict)
    dfs(graph_dict)
    node_labels = dict([(v, d['name'])
                        for v, d in G.nodes(data=True)])
    edge_labels = dict([((u, v,), d['name'])
                        for u, v, d in G.edges(data=True)])
    pos = nx.planar_layout(G)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5)
    nx.draw_networkx_labels(G, pos, node_labels, font_size=5)
    nx.draw(G, pos, node_size=5)
    # print(cnt)
    # print(nx.get_node_attributes(G, 'name'))
    plt.savefig("graph.png")
    plt.show()
