class BinaryNode:
    def __init__(self, entry):
        self.entry = entry
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def add(self, entry):
        if self.root is None:
            self.root = BinaryNode(entry)
        else:
            self._add_recursive(self.root, entry)
            
    def _add_recursive(self, node, entry):
        if entry == node.entry:
            raise ValueError("Duplicate entry not allowed.")
        elif entry < node.entry:
            if node.left is None:
                node.left = BinaryNode(entry)
            else:
                self._add_recursive(node.left, entry)
        else:  # entry > node.entry
            if node.right is None:
                node.right = BinaryNode(entry)
            else:
                self._add_recursive(node.right, entry)

    def preorder(self, visit_func):
        self._preorder_recursive(self.root, visit_func)

    def _preorder_recursive(self, node, visit_func):
        if node:
            visit_func(node.entry)
            self._preorder_recursive(node.left, visit_func)
            self._preorder_recursive(node.right, visit_func)

    def inorder(self, visit_func):
        self._inorder_recursive(self.root, visit_func)

    def _inorder_recursive(self, node, visit_func):
        if node:
            self._inorder_recursive(node.left, visit_func)
            visit_func(node.entry)
            self._inorder_recursive(node.right, visit_func)

    def postorder(self, visit_func):
        self._postorder_recursive(self.root, visit_func)

    def _postorder_recursive(self, node, visit_func):
        if node:
            self._postorder_recursive(node.left, visit_func)
            self._postorder_recursive(node.right, visit_func)
            visit_func(node.entry)
