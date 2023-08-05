import ast
import networkx
from .visitor import AstVisitor


def build_ast(source_file_path, image_path):
    with open(source_file_path) as f:
        tree = networkx.DiGraph()
        AstVisitor(tree).visit(ast.parse(f.read()))
        networkx.drawing.nx_pydot.to_pydot(tree).write_png(image_path)


if __name__ == "__main__":
    build_ast('fibonacci.py', 'artifacts/ast.png')
