#!/usr/bin/env python3
"""
Script to add `else: pass` to every try-except block that lacks an else clause
in all Python files in the current directory (recursively).

Usage:
    python add_else_pass.py

Backups of modified files will be created with the `.bak` extension.
"""
import ast
import astor
import os
import shutil

class TryElseTransformer(ast.NodeTransformer):
    def visit_Try(self, node: ast.Try) -> ast.Try:
        # Only add else if there are except handlers and no existing else
        if node.handlers and not node.orelse:
            # Create a Pass statement
            pass_node = ast.Pass()
            # Add pass under else
            node.orelse = [pass_node]
        # Continue transforming nested nodes
        self.generic_visit(node)
        return node


def process_file(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as e:
        print(f"Skipping {path}: SyntaxError - {e}")
        return

    transformer = TryElseTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    new_source = astor.to_source(new_tree)

    if new_source != source:
        # Backup original
        bak_path = path + '.bak'
        shutil.copy2(path, bak_path)
        # Write modified
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_source)
        print(f"Updated {path}, backup at {bak_path}")


def main():
    # Walk current directory
    for root, dirs, files in os.walk('./core/src/toga'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                process_file(full_path)

if __name__ == '__main__':
    main()

