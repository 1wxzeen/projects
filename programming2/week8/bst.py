''' 
author: wazeen hoq 
kuid: 3137691 
date created: 4/21
lab: lab#1005C
last modified: 4/21
purpose: bst class
'''

class BinaryNode:
    def __init__(self, entry):
        self.entry = entry
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, entry):
        self.root = self._insert_recursive(self.root, entry)

    def _insert_recursive(self, node, entry):
        if node is None:
            return BinaryNode(entry)
        if entry == node.entry:
            raise RuntimeError("Duplicate entry not allowed.")
        elif entry < node.entry:
            node.left = self._insert_recursive(node.left, entry)
        else:
            node.right = self._insert_recursive(node.right, entry)
        return node

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None:
            raise RuntimeError("Pokemon not found.")
        if key == node.entry.get_key():
            return node.entry
        elif key < node.entry.get_key():
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def in_order(self, visit_func):
        self._in_order(self.root, visit_func)

    def _in_order(self, node, visit_func):
        if node:
            self._in_order(node.left, visit_func)
            visit_func(node.entry)
            self._in_order(node.right, visit_func)

    def pre_order(self, visit_func):
        self._pre_order(self.root, visit_func)

    def _pre_order(self, node, visit_func):
        if node:
            visit_func(node.entry)
            self._pre_order(node.left, visit_func)
            self._pre_order(node.right, visit_func)

    def post_order(self, visit_func):
        self._post_order(self.root, visit_func)

    def _post_order(self, node, visit_func):
        if node:
            self._post_order(node.left, visit_func)
            self._post_order(node.right, visit_func)
            visit_func(node.entry)

    def remove(self, key):
        self.root = self._remove_recursive(self.root, key)

    def _remove_recursive(self, node, key):
        if node is None:
            raise RuntimeError("Pokemon not found.")
        if key < node.entry.get_key():
            node.left = self._remove_recursive(node.left, key)
        elif key > node.entry.get_key():
            node.right = self._remove_recursive(node.right, key)
        else:  # Found node to remove
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                max_node = self._get_max(node.left)
                node.entry = max_node.entry
                node.left = self._remove_recursive(node.left, max_node.entry.get_key())
        return node

    def _get_max(self, node):
        while node.right:
            node = node.right
        return node