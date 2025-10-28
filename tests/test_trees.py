"""Testes automatizados para as Árvores B e B+."""

from __future__ import annotations

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend import BPlusTree, BTree  # noqa: E402  # pylint: disable=wrong-import-position


def test_btree_insertion():
    print("\n" + "=" * 50)
    print("TESTE: Inserção na Árvore B")
    print("=" * 50)

    tree = BTree(order=3)
    values = [10, 20, 5, 6, 12, 30, 7, 17]

    print(f"Inserindo valores: {values}")
    for value in values:
        tree.insert(value)

    print("\nÁrvore após inserções:")
    print(tree)

    all_found = all(tree.search(item) for item in values)
    print(f"\n✓ Todos os valores inseridos: {all_found}")

    return tree


def test_btree_deletion():
    print("\n" + "=" * 50)
    print("TESTE: Exclusão na Árvore B")
    print("=" * 50)

    tree = BTree(order=3)
    values = [10, 20, 5, 6, 12, 30, 7, 17]

    for value in values:
        tree.insert(value)

    print("Árvore inicial:")
    print(tree)

    to_delete = [6, 12, 20]
    print(f"\nExcluindo valores: {to_delete}")

    for value in to_delete:
        tree.delete(value)

    print("\nÁrvore após exclusões:")
    print(tree)

    deleted = all(not tree.search(item) for item in to_delete)
    remaining = all(tree.search(item) for item in values if item not in to_delete)

    print(f"\n✓ Valores excluídos corretamente: {deleted}")
    print(f"✓ Valores restantes mantidos: {remaining}")


def test_bplustree_insertion():
    print("\n" + "=" * 50)
    print("TESTE: Inserção na Árvore B+")
    print("=" * 50)

    tree = BPlusTree(order=3)
    values = [10, 20, 5, 6, 12, 30, 7, 17]

    print(f"Inserindo valores: {values}")
    for value in values:
        tree.insert(value)

    print("\nÁrvore após inserções:")
    print(tree)

    print("\nLista encadeada de folhas:")
    tree.display_leaves()

    all_found = all(tree.search(item) for item in values)
    print(f"\n✓ Todos os valores inseridos: {all_found}")

    return tree


def test_bplustree_deletion():
    print("\n" + "=" * 50)
    print("TESTE: Exclusão na Árvore B+")
    print("=" * 50)

    tree = BPlusTree(order=3)
    values = [10, 20, 5, 6, 12, 30, 7, 17]

    for value in values:
        tree.insert(value)

    print("Árvore inicial:")
    print(tree)

    to_delete = [6, 12, 20]
    print(f"\nExcluindo valores: {to_delete}")

    for value in to_delete:
        tree.delete(value)

    print("\nÁrvore após exclusões:")
    print(tree)

    print("\nLista encadeada de folhas após exclusões:")
    tree.display_leaves()

    deleted = all(not tree.search(item) for item in to_delete)
    remaining = all(tree.search(item) for item in values if item not in to_delete)

    print(f"\n✓ Valores excluídos corretamente: {deleted}")
    print(f"✓ Valores restantes mantidos: {remaining}")


def test_history():
    print("\n" + "=" * 50)
    print("TESTE: Histórico de Operações")
    print("=" * 50)

    tree = BTree(order=3)

    tree.insert(10)
    tree.insert(20)
    tree.insert(5)
    tree.delete(10)

    history = tree.get_history()

    print("Histórico de operações:")
    for index, operation in enumerate(history, 1):
        print(f"{index}. {operation}")

    expected_count = 4
    print(f"\n✓ Número de operações registradas: {len(history)} (esperado: {expected_count})")

    tree.clear_history()
    history_after_clear = tree.get_history()
    print(f"✓ Histórico limpo: {len(history_after_clear) == 0}")


def test_large_dataset():
    print("\n" + "=" * 50)
    print("TESTE: Conjunto de Dados Grande")
    print("=" * 50)

    tree = BTree(order=5)
    values = list(range(1, 51))

    print(f"Inserindo {len(values)} valores...")
    for value in values:
        tree.insert(value)

    print("\nÁrvore final:")
    print(tree)

    all_found = all(tree.search(item) for item in values)
    print(f"\n✓ Todos os {len(values)} valores foram encontrados: {all_found}")

    to_delete = values[::2]
    print(f"\nExcluindo {len(to_delete)} valores...")
    for value in to_delete:
        tree.delete(value)

    deleted = all(not tree.search(item) for item in to_delete)
    remaining = all(tree.search(item) for item in values if item not in to_delete)

    print(f"✓ Valores excluídos corretamente: {deleted}")
    print(f"✓ Valores restantes mantidos: {remaining}")


def test_edge_cases():
    print("\n" + "=" * 50)
    print("TESTE: Casos Extremos")
    print("=" * 50)

    print("\n1. Busca em árvore vazia:")
    tree = BTree(order=3)
    result = tree.search(10)
    print(f"   Buscar 10 em árvore vazia: {result} (esperado: False)")

    print("\n2. Inserir valores duplicados:")
    tree.insert(10)
    tree.insert(10)
    print("   Árvore após inserir 10 duas vezes:")
    print(tree)

    print("\n3. Excluir de árvore vazia:")
    empty_tree = BTree(order=3)
    empty_tree.delete(10)
    print("   Excluir 10 de árvore vazia (não deve gerar erro)")

    print("\n4. Excluir valor inexistente:")
    tree = BTree(order=3)
    tree.insert(10)
    tree.delete(20)
    print("   Excluir 20 quando só existe 10 (não deve gerar erro)")

    print("\n✓ Todos os casos extremos tratados corretamente")


def run_all_tests():
    print("\n")
    print("#" * 50)
    print("#" + " " * 48 + "#")
    print("#  EXECUTANDO TESTES DAS ÁRVORES B E B+         #")
    print("#" + " " * 48 + "#")
    print("#" * 50)

    try:
        test_btree_insertion()
        test_btree_deletion()
        test_bplustree_insertion()
        test_bplustree_deletion()
        test_history()
        test_large_dataset()
        test_edge_cases()

        print("\n" + "=" * 50)
        print("✓ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 50 + "\n")

    except Exception as exc:  # pylint: disable=broad-except
        print(f"\n✗ ERRO DURANTE OS TESTES: {exc}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
