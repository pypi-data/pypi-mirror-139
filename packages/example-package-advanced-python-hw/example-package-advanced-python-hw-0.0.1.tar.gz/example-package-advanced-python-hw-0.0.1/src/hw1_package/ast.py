import ast
import networkx as nx
import inspect

# from hw1.src.hw1_package import HW_1_ROOT_PATH
# from hw1.src.hw1_package.fibonacci import get_n_fibonacci_number


def get_n_fibonacci_number(n: int):
    """
    Simple version of fibonacci number calculations, with cashing.
    :param n: int number of fibonacci sequences to return.
    :return: int n'th fibonacci number.
    """
    first_fibonacci_number = 0
    second_fibonacci_number = 1

    if n == 1:
        return first_fibonacci_number

    elif n == 2:
        return second_fibonacci_number

    elif n < 1:
        raise AssertionError("Function takes only positive integers.")

    else:
        for i in range(n - 2):
            to_become_first = second_fibonacci_number
            second_fibonacci_number = first_fibonacci_number + second_fibonacci_number
            first_fibonacci_number = to_become_first
        return second_fibonacci_number


class AssignmentVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()
        self.parent = None

    def _get_label(self, node):
        label = None
        try:
            label = str(node.op).split()[0][5:]
        except AttributeError:
            try:
                label = node.value
            except AttributeError:
                try:
                    label = node.id
                except AttributeError:
                    pass
        return label

    def generic_visit(self, node):
        label = self._get_label(node)

        if label:
            self.graph.add_node(str(node), label=label)
        else:
            self.graph.add_node(str(node))

        if self.parent:
            self.graph.add_edge(self.parent, str(node))
        self.parent = str(node)
        super().generic_visit(node)


def main(image_path: str = f"artifacts/ast.png"):
    tree = AssignmentVisitor()
    function_text = inspect.getsource(get_n_fibonacci_number)
    module = ast.parse(source=function_text)
    tree.visit(module)
    p = nx.drawing.nx_pydot.to_pydot(tree.graph)
    p.write_png(image_path)


if __name__ == "__main__":
    main()
