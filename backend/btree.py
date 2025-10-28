"""
Implementação de Árvore B.
"""


class BTreeNode:
    """Nó da Árvore B."""

    def __init__(self, leaf: bool = False):
        self.keys = []
        self.children = []
        self.leaf = leaf

    def split(self, parent: "BTreeNode", payload):
        """Divide o nó quando está cheio."""
        new_node = BTreeNode(leaf=self.leaf)
        mid_point = len(self.keys) // 2
        new_node.keys = self.keys[mid_point + 1:]
        self.keys = self.keys[:mid_point]

        if not self.leaf:
            new_node.children = self.children[mid_point + 1:]
            self.children = self.children[:mid_point + 1]

        parent.add_key(payload, [self, new_node])
        return parent

    def add_key(self, value, children=None):
        """Adiciona uma chave ao nó."""
        if not self.keys:
            self.keys.append(value)
            if children:
                self.children = children
            return

        for index, key in enumerate(self.keys):
            if value < key:
                self.keys.insert(index, value)
                if children:
                    self.children = (
                        self.children[: index + 1] + children + self.children[index + 1 :]
                    )
                return

        self.keys.append(value)
        if children:
            self.children.extend(children)

    def is_full(self, order: int) -> bool:
        """Verifica se o nó está cheio."""
        return len(self.keys) >= order


class BTree:
    """Implementação de Árvore B."""

    def __init__(self, order: int = 3):
        self.root = BTreeNode(leaf=True)
        self.order = order
        self.history = []

    def insert(self, value):
        """Insere um valor na árvore."""
        self.history.append(f"Inserir: {value}")

        if self.root.is_full(2 * self.order - 1):
            new_root = BTreeNode()
            new_root.children.append(self.root)
            new_root.leaf = False
            self.root = self.root.split(new_root, self.root.keys[len(self.root.keys) // 2])

        self._insert_non_full(self.root, value)

    def _insert_non_full(self, node: BTreeNode, value):
        """Insere em um nó que não está cheio."""
        if node.leaf:
            node.add_key(value)
        else:
            child_index = 0
            for index, key in enumerate(node.keys):
                if value < key:
                    child_index = index
                    break
            else:
                child_index = len(node.keys)

            child = node.children[child_index]

            if child.is_full(2 * self.order - 1):
                mid_key = child.keys[len(child.keys) // 2]
                node = child.split(node, mid_key)

                if value > node.keys[child_index]:
                    child_index += 1
                child = node.children[child_index]

            self._insert_non_full(child, value)

    def search(self, value, node: BTreeNode | None = None) -> bool:
        """Busca um valor na árvore."""
        if node is None:
            node = self.root

        for index, key in enumerate(node.keys):
            if value == key:
                return True
            if value < key:
                if node.leaf:
                    return False
                return self.search(value, node.children[index])

        if node.leaf:
            return False
        return self.search(value, node.children[len(node.keys)])

    def delete(self, value):
        """Remove um valor da árvore."""
        self.history.append(f"Excluir: {value}")
        self._delete(self.root, value)

        if len(self.root.keys) == 0:
            if not self.root.leaf and len(self.root.children) > 0:
                self.root = self.root.children[0]

    def _delete(self, node: BTreeNode, value):
        """Remove um valor do nó informado."""
        try:
            index = node.keys.index(value)
        except ValueError:
            index = None

        if index is not None:
            if node.leaf:
                node.keys.pop(index)
            else:
                self._delete_internal_node(node, index)
        elif not node.leaf:
            child_index = 0
            for idx, key in enumerate(node.keys):
                if value < key:
                    child_index = idx
                    break
            else:
                child_index = len(node.keys)

            if child_index < len(node.children):
                child = node.children[child_index]

                if len(child.keys) < self.order:
                    self._fill(node, child_index)

                if child_index > len(node.children) - 1:
                    child_index -= 1

                if child_index < len(node.children):
                    self._delete(node.children[child_index], value)

    def _delete_internal_node(self, node: BTreeNode, index: int):
        key = node.keys[index]

        if len(node.children[index].keys) >= self.order:
            predecessor = self._get_predecessor(node, index)
            node.keys[index] = predecessor
            self._delete(node.children[index], predecessor)
        elif len(node.children[index + 1].keys) >= self.order:
            successor = self._get_successor(node, index)
            node.keys[index] = successor
            self._delete(node.children[index + 1], successor)
        else:
            self._merge(node, index)
            self._delete(node.children[index], key)

    def _get_predecessor(self, node: BTreeNode, index: int):
        current = node.children[index]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node: BTreeNode, index: int):
        current = node.children[index + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _fill(self, node: BTreeNode, index: int):
        if index > 0 and len(node.children[index - 1].keys) >= self.order:
            self._borrow_from_prev(node, index)
        elif index < len(node.children) - 1 and len(node.children[index + 1].keys) >= self.order:
            self._borrow_from_next(node, index)
        else:
            if index < len(node.children) - 1:
                self._merge(node, index)
            else:
                self._merge(node, index - 1)

    def _borrow_from_prev(self, node: BTreeNode, child_index: int):
        child = node.children[child_index]
        sibling = node.children[child_index - 1]

        child.keys.insert(0, node.keys[child_index - 1])
        node.keys[child_index - 1] = sibling.keys.pop()

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, node: BTreeNode, child_index: int):
        child = node.children[child_index]
        sibling = node.children[child_index + 1]

        child.keys.append(node.keys[child_index])
        node.keys[child_index] = sibling.keys.pop(0)

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, node: BTreeNode, index: int):
        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys[index])
        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        node.keys.pop(index)
        node.children.pop(index + 1)

    def get_history(self):
        """Retorna o histórico de operações."""
        return self.history.copy()

    def clear_history(self):
        """Limpa o histórico de operações."""
        self.history.clear()

    def display(self, node: BTreeNode | None = None, level: int = 0):
        """Exibe a árvore no console."""
        if node is None:
            node = self.root

        print(f"Nível {level}: {node.keys}")

        if not node.leaf:
            for child in node.children:
                self.display(child, level + 1)

    def __str__(self) -> str:
        return self._str_helper(self.root, 0)

    def _str_helper(self, node: BTreeNode, level: int) -> str:
        result = "  " * level + f"Nível {level}: {node.keys}\n"
        if not node.leaf:
            for child in node.children:
                result += self._str_helper(child, level + 1)
        return result
