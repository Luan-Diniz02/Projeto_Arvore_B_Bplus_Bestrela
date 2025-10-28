"""
Implementação de Árvore B+.
"""


class BPlusTreeNode:
    """Nó da Árvore B+."""

    def __init__(self, leaf: bool = False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.next = None
        self.parent = None

    def split(self, parent: "BPlusTreeNode | None"):
        """Divide o nó quando está cheio."""
        mid_point = len(self.keys) // 2
        new_node = BPlusTreeNode(leaf=self.leaf)
        new_node.parent = self.parent

        if self.leaf:
            new_node.keys = self.keys[mid_point:]
            new_node.next = self.next
            self.next = new_node
            self.keys = self.keys[:mid_point]
            split_key = new_node.keys[0]
        else:
            split_key = self.keys[mid_point]
            new_node.keys = self.keys[mid_point + 1 :]
            new_node.children = self.children[mid_point + 1 :]
            self.keys = self.keys[:mid_point]
            self.children = self.children[: mid_point + 1]

            for child in new_node.children:
                child.parent = new_node

        if parent is None:
            parent = BPlusTreeNode()
            parent.keys = [split_key]
            parent.children = [self, new_node]
            self.parent = parent
            new_node.parent = parent
            return parent

        parent.insert_key(split_key, [self, new_node])
        return None

    def insert_key(self, key, children=None):
        """Insere uma chave no nó."""
        if not self.keys:
            self.keys.append(key)
            if children:
                self.children = children
            return

        for index, current_key in enumerate(self.keys):
            if key < current_key:
                self.keys.insert(index, key)
                if children:
                    self.children = (
                        self.children[: index + 1]
                        + children
                        + self.children[index + 1 :]
                    )
                return

        self.keys.append(key)
        if children:
            self.children.extend(children)


class BPlusTree:
    """Implementação de Árvore B+."""

    def __init__(self, order: int = 3):
        self.root = BPlusTreeNode(leaf=True)
        self.order = order
        self.history = []

    def insert(self, value):
        """Insere um valor na árvore."""
        self.history.append(f"Inserir: {value}")

        leaf = self._find_leaf(self.root, value)
        leaf.insert_key(value)

        if len(leaf.keys) >= self.order:
            self._split_and_propagate(leaf)

    def _find_leaf(self, node: BPlusTreeNode, value) -> BPlusTreeNode:
        if node.leaf:
            return node

        for index, key in enumerate(node.keys):
            if value < key:
                return self._find_leaf(node.children[index], value)

        return self._find_leaf(node.children[-1], value)

    def _split_and_propagate(self, node: BPlusTreeNode):
        parent = node.parent
        new_root = node.split(parent)

        if new_root:
            self.root = new_root
            return

        if parent and len(parent.keys) >= self.order:
            self._split_and_propagate(parent)

    def search(self, value) -> bool:
        """Busca um valor na árvore."""
        leaf = self._find_leaf(self.root, value)
        return value in leaf.keys

    def delete(self, value):
        """Remove um valor da árvore."""
        self.history.append(f"Excluir: {value}")

        leaf = self._find_leaf(self.root, value)

        if value not in leaf.keys:
            return False

        leaf.keys.remove(value)

        min_keys = (self.order - 1) // 2
        if len(leaf.keys) < min_keys and leaf != self.root:
            self._rebalance(leaf)

        if len(self.root.keys) == 0 and not self.root.leaf:
            if self.root.children:
                self.root = self.root.children[0]
                self.root.parent = None

        return True

    def _rebalance(self, node: BPlusTreeNode):
        parent = node.parent
        if not parent:
            return

        node_index = parent.children.index(node)

        if node_index > 0:
            left_sibling = parent.children[node_index - 1]
            if len(left_sibling.keys) > (self.order - 1) // 2:
                self._borrow_from_left(node, left_sibling, parent, node_index)
                return

        if node_index < len(parent.children) - 1:
            right_sibling = parent.children[node_index + 1]
            if len(right_sibling.keys) > (self.order - 1) // 2:
                self._borrow_from_right(node, right_sibling, parent, node_index)
                return

        if node_index > 0:
            left_sibling = parent.children[node_index - 1]
            self._merge(left_sibling, node, parent, node_index - 1)
        elif node_index < len(parent.children) - 1:
            right_sibling = parent.children[node_index + 1]
            self._merge(node, right_sibling, parent, node_index)

    def _borrow_from_left(self, node, left_sibling, parent, node_index):
        if node.leaf:
            borrowed_key = left_sibling.keys.pop()
            node.keys.insert(0, borrowed_key)
            parent.keys[node_index - 1] = node.keys[0]
        else:
            borrowed_key = left_sibling.keys.pop()
            borrowed_child = left_sibling.children.pop()
            node.keys.insert(0, parent.keys[node_index - 1])
            parent.keys[node_index - 1] = borrowed_key
            node.children.insert(0, borrowed_child)
            borrowed_child.parent = node

    def _borrow_from_right(self, node, right_sibling, parent, node_index):
        if node.leaf:
            borrowed_key = right_sibling.keys.pop(0)
            node.keys.append(borrowed_key)
            parent.keys[node_index] = right_sibling.keys[0]
        else:
            borrowed_key = right_sibling.keys.pop(0)
            borrowed_child = right_sibling.children.pop(0)
            node.keys.append(parent.keys[node_index])
            parent.keys[node_index] = borrowed_key
            node.children.append(borrowed_child)
            borrowed_child.parent = node

    def _merge(self, left_node, right_node, parent, left_index):
        if left_node.leaf:
            left_node.keys.extend(right_node.keys)
            left_node.next = right_node.next
        else:
            left_node.keys.append(parent.keys[left_index])
            left_node.keys.extend(right_node.keys)
            left_node.children.extend(right_node.children)

            for child in right_node.children:
                child.parent = left_node

        parent.keys.pop(left_index)
        parent.children.pop(left_index + 1)

        min_keys = (self.order - 1) // 2
        if len(parent.keys) < min_keys and parent != self.root:
            self._rebalance(parent)

    def get_history(self):
        return self.history.copy()

    def clear_history(self):
        self.history.clear()

    def display(self, node: BPlusTreeNode | None = None, level: int = 0):
        if node is None:
            node = self.root

        print(f"Nível {level}: {node.keys} {'(Folha)' if node.leaf else ''}")

        if not node.leaf:
            for child in node.children:
                self.display(child, level + 1)

    def display_leaves(self):
        current = self.root
        while not current.leaf:
            current = current.children[0]

        print("Folhas: ", end="")
        while current:
            print(current.keys, end=" -> ")
            current = current.next
        print("None")

    def __str__(self) -> str:
        return self._str_helper(self.root, 0)

    def _str_helper(self, node: BPlusTreeNode, level: int) -> str:
        result = "  " * level + f"Nível {level}: {node.keys} {'(Folha)' if node.leaf else ''}\n"
        if not node.leaf:
            for child in node.children:
                result += self._str_helper(child, level + 1)
        return result
