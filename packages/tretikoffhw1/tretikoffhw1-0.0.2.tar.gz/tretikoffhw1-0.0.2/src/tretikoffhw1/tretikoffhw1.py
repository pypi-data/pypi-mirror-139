import ast
import inspect
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout


def fib0(x):
    if x == 0 or x == 1:
        return 1
    return fib0(x - 1) + fib0(x - 2)


tree = nx.DiGraph()
color_map = []
labels = {}


class NodeVisitor(object):
    def __init__(self):
        self.parents = []

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_Module(self, node):
        self.node(node, "Module:", "grey", edge=False)
        self.parents.append(node)
        self.visit_item(node.body)
        self.parents.pop()

    def visit_arguments(self, node):
        self.node(node, "arguments", "cyan")
        self.visit_children(node)

    def visit_arg(self, node):
        self.node(node, "arg " + node.arg, "green")

    def visit_FunctionDef(self, node):
        self.node(node, "fun " + node.name, "red")
        self.visit_children(node)

    def visit_children(self, node):
        tree.add_edge(self.parents[-1], node)
        self.parents.append(node)
        for field, value in ast.iter_fields(node):
            self.visit_item(value)
        self.parents.pop()

    def visit_item(self, value):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    self.visit(item)
        elif isinstance(value, ast.AST):
            self.visit(value)

    def generic_visit(self, node):
        self.node(node, node.__class__.__name__, "orange")
        self.visit_children(node)

    def visit_Call(self, node):
        self.node(node, "call " + ast.unparse(node.func), "green")
        self.parents.append(node)
        self.visit_item(node.args)
        self.parents.pop()

    def visit_If(self, node):
        self.node(node, "If", "grey")
        self.visit_children(node)

    def node(self, node, label, color="grey", edge=True):
        if node in tree:
            return
        tree.add_node(node)
        if edge:
            self.edge(node)
        labels[node] = label
        color_map.append(color)

    def edge(self, nod):
        tree.add_edge(self.parents[-1], nod)

    def visit_BinOp(self, node):
        self.node(node, "binop: " + node.op.__class__.__name__, "grey")
        self.parents.append(node)
        self.visit(node.left)
        self.visit(node.right)
        self.parents.pop()

    def visit_Compare(self, node):
        self.node(node, " ".join(map(lambda x: x.__class__.__name__, node.ops)), "olive")
        self.parents.append(node)
        self.visit_item(node.left)
        self.visit_item(node.comparators)
        self.parents.pop()

    def visit_Constant(self, node):
        self.node(node, "const " + str(node.value), "yellow")

    def visit_BoolOp(self, node):
        self.node(node, "binop: " + node.op.__class__.__name__, "grey")
        self.parents.append(node)
        self.visit_item(node.values)
        self.parents.pop()

    def visit_Name(self, node):
        self.node(node, "variable " + ast.unparse(node), "green")


def print_node(node):
    NodeVisitor().visit(node)


def set_picture(url):
    print_node(ast.parse(inspect.getsource(fib0)))
    write_dot(tree, '../../../test.dot')
    pos = graphviz_layout(tree, prog='dot')
    plt.figure(figsize=(9, 9))
    nx.draw(tree, pos, with_labels=True, labels=labels, node_color=color_map,
            node_size=[len(labels[v]) * 450 for v in tree.nodes()])
    plt.savefig(url)
    plt.show()


if __name__ == '__main__':
    set_picture('artifacts/tree.png')
