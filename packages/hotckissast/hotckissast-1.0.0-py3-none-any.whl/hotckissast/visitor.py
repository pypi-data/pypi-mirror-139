import ast
from zlib import adler32


class AstVisitor:
    def __init__(self, tree):
        self._ast = tree
        self._order = 0

    def visit(self, node):
        idx = self._order
        text, fill_color = self.__node_ui(node)
        self._ast.add_node(self._order, label=text, color=fill_color, style='filled')
        self._order += 1

        for _, vertex in ast.iter_fields(node):
            nxt = vertex if isinstance(vertex, list) else [vertex]

            for vtx in filter(lambda v: isinstance(v, ast.AST) and type(v) not in [ast.Load, ast.Store], nxt):
                self._ast.add_edge(idx, self.visit(vtx))

        return idx

    def __node_ui(self, node):
        text = node.__class__.__name__
        fill_color = f"#{'%X' % ((adler32(text.encode()) ** 2) % (256 ** 3 - 1))}"

        if isinstance(node, ast.Sub) or isinstance(node, ast.USub):
            text = "-"
        elif isinstance(node, ast.Add) or isinstance(node, ast.UAdd):
            text = "+"
        elif isinstance(node, ast.Constant):
            text = f"{node.value}"
        elif isinstance(node, ast.FunctionDef):
            text = f"def: {node.name}"
        elif isinstance(node, ast.Attribute):
            text = f"method: {node.attr}"
        elif isinstance(node, ast.Name):
            text = f"name: {node.id}"
        elif isinstance(node, ast.arg):
            text = f"arg: {node.arg}"

        return text, fill_color
