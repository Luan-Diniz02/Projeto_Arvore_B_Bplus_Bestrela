"""Aplicação web para gerenciamento das Árvores B e B+."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, render_template, request

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    # Ensure the backend package is importable when running this script directly.
    sys.path.append(str(PROJECT_ROOT))

from backend import (  # noqa: E402  # pylint: disable=wrong-import-position
    BPlusTree,
    BPlusTreeNode,
    BTree,
    BTreeNode,
)


def _serialize_btree_node(node: BTreeNode) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "keys": list(node.keys),
        "leaf": node.leaf,
    }

    if not node.leaf:
        data["children"] = [_serialize_btree_node(child) for child in node.children]

    return data


def _serialize_bplustree_node(node: BPlusTreeNode) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "keys": list(node.keys),
        "leaf": node.leaf,
    }

    if node.leaf and node.next:
        data["next_keys"] = list(node.next.keys)

    if not node.leaf:
        data["children"] = [_serialize_bplustree_node(child) for child in node.children]

    return data


def _collect_btree_leaves(node: BTreeNode) -> List[List[int]]:
    if node.leaf:
        return [list(node.keys)] if node.keys else []

    leaves: List[List[int]] = []
    for child in node.children:
        leaves.extend(_collect_btree_leaves(child))
    return leaves


def _collect_bplustree_leaves(tree: BPlusTree) -> List[List[int]]:
    leaves: List[List[int]] = []
    node = tree.root

    while node and not node.leaf:
        node = node.children[0]

    while node:
        leaves.append(list(node.keys))
        node = node.next

    return leaves


@dataclass
class ManagedTree:
    label: str
    type_key: str
    instance: Optional[Any] = None
    created: bool = False

    def reset(self, order: int) -> None:
        if self.type_key == "b":
            self.instance = BTree(order=order)
        else:
            self.instance = BPlusTree(order=order)

        self.created = True
        self.append_history(f"Criar árvore {self.label} (ordem {order})")

    @property
    def order(self) -> Optional[int]:
        if not self.instance:
            return None
        return getattr(self.instance, "order", None)

    @property
    def history(self) -> List[str]:
        if not self.instance:
            return []
        return list(self.instance.get_history())

    def append_history(self, message: str) -> None:
        if not self.instance:
            return
        self.instance.history.append(message)


app = Flask(__name__)

TREES: Dict[str, ManagedTree] = {
    "b": ManagedTree(label="Árvore B", type_key="b"),
    "bplus": ManagedTree(label="Árvore B+", type_key="bplus"),
}


def _get_tree(tree_type: str) -> ManagedTree:
    key = tree_type.lower()
    if key not in TREES:
        raise ValueError("Tipo de árvore inválido")
    return TREES[key]


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/api/tree/create", methods=["POST"])
def create_tree():
    payload = request.get_json(force=True)
    tree_type = payload.get("tree_type", "b").lower()
    order = payload.get("order", 3)

    if not isinstance(order, int) or order < 3:
        return jsonify({"error": "A ordem deve ser um inteiro maior ou igual a 3."}), 400

    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    tree.reset(order)

    return jsonify(
        {
            "success": True,
            "message": f"{tree.label} criada com sucesso (ordem {order}).",
            "tree_type": tree.type_key,
            "order": order,
        }
    )


@app.route("/api/tree/<tree_type>/insert", methods=["POST"])
def insert_value(tree_type: str):
    payload = request.get_json(force=True)
    value = payload.get("value")

    if value is None:
        return jsonify({"error": "Informe um valor inteiro para inserir."}), 400

    try:
        value = int(value)
    except (TypeError, ValueError):
        return jsonify({"error": "O valor deve ser um número inteiro."}), 400

    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not tree.instance:
        return jsonify({"error": "Crie a árvore antes de inserir valores."}), 400

    tree.instance.insert(value)

    return jsonify({"success": True, "message": f"Valor {value} inserido na {tree.label}."})


@app.route("/api/tree/<tree_type>/search/<int:value>")
def search_value(tree_type: str, value: int):
    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not tree.instance:
        return jsonify({"error": "Crie a árvore antes de realizar buscas."}), 400

    found = tree.instance.search(value)
    tree.append_history(f"Buscar: {value} -> {'Encontrado' if found else 'Não encontrado'}")

    return jsonify({"value": value, "found": found})


@app.route("/api/tree/<tree_type>/value/<int:value>", methods=["DELETE"])
def delete_value(tree_type: str, value: int):
    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not tree.instance:
        return jsonify({"error": "Crie a árvore antes de excluir valores."}), 400

    result = tree.instance.delete(value)
    if result is False:
        tree.append_history(f"Excluir: {value} -> Valor não encontrado")
        return jsonify({"error": f"Valor {value} não encontrado na {tree.label}."}), 404

    tree.append_history(f"Excluir: {value}")
    return jsonify({"success": True, "message": f"Valor {value} removido da {tree.label}."})


@app.route("/api/tree/<tree_type>")
def get_tree(tree_type: str):
    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not tree.instance:
        return jsonify({"error": "Crie a árvore antes de visualizar a estrutura."}), 400

    if tree.type_key == "b":
        serialized = _serialize_btree_node(tree.instance.root)
        leaves = _collect_btree_leaves(tree.instance.root)
    else:
        serialized = _serialize_bplustree_node(tree.instance.root)
        leaves = _collect_bplustree_leaves(tree.instance)

    return jsonify(
        {
            "label": tree.label,
            "order": tree.instance.order,
            "string_representation": str(tree.instance),
            "serialized": serialized,
            "leaves": leaves,
        }
    )


@app.route("/api/tree/<tree_type>/leaves")
def get_leaves(tree_type: str):
    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not tree.instance:
        return jsonify({"error": "Crie a árvore antes de visualizar as folhas."}), 400

    if tree.type_key == "b":
        leaves = _collect_btree_leaves(tree.instance.root)
    else:
        leaves = _collect_bplustree_leaves(tree.instance)

    return jsonify({"leaves": leaves})


@app.route("/api/tree/<tree_type>/history")
def get_history(tree_type: str):
    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not tree.instance:
        return jsonify({"error": "Crie a árvore antes de consultar o histórico."}), 400

    return jsonify({"history": tree.history})


@app.route("/api/tree/<tree_type>/history", methods=["DELETE"])
def clear_history(tree_type: str):
    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not tree.instance:
        return jsonify({"error": "Crie a árvore antes de limpar o histórico."}), 400

    tree.instance.clear_history()
    return jsonify({"success": True, "message": "Histórico limpo com sucesso."})


@app.route("/api/tree/<tree_type>/export")
def export_tree(tree_type: str):
    try:
        tree = _get_tree(tree_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not tree.instance:
        return jsonify({"error": "Crie a árvore antes de exportar a estrutura."}), 400

    if tree.type_key == "b":
        serialized = _serialize_btree_node(tree.instance.root)
    else:
        serialized = _serialize_bplustree_node(tree.instance.root)

    return jsonify(
        {
            "label": tree.label,
            "order": tree.instance.order,
            "serialized": serialized,
            "history": tree.history,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
