"""Interface de linha de comando para manipular Árvores B e B+."""

from __future__ import annotations

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend import BPlusTree, BTree  # noqa: E402  # pylint: disable=wrong-import-position


def print_menu():
    print("\n" + "=" * 50)
    print("SISTEMA DE ÁRVORES B E B+")
    print("=" * 50)
    print("1. Árvore B")
    print("2. Árvore B+")
    print("0. Sair")
    print("=" * 50)


def print_tree_menu(tree_type: str):
    print(f"\n{'=' * 50}")
    print(f"OPERAÇÕES DA ÁRVORE {tree_type}")
    print("=" * 50)
    print("1. Criar Árvore")
    print("2. Inserir Valor")
    print("3. Buscar Valor")
    print("4. Excluir Valor")
    print("5. Exibir Árvore")
    print("6. Histórico de Operações")
    print("7. Limpar Histórico")
    print("0. Voltar")
    print("=" * 50)


def criar_arvore_b():
    try:
        order = int(input("Digite a ordem da árvore (padrão 3): ") or "3")
        tree = BTree(order=order)
        print(f"✓ Árvore B criada com sucesso! (Ordem: {order})")
        return tree
    except ValueError:
        print("✗ Erro: valor inválido. Criando árvore com ordem padrão 3.")
        return BTree(order=3)


def criar_arvore_bplus():
    try:
        order = int(input("Digite a ordem da árvore (padrão 3): ") or "3")
        tree = BPlusTree(order=order)
        print(f"✓ Árvore B+ criada com sucesso! (Ordem: {order})")
        return tree
    except ValueError:
        print("✗ Erro: valor inválido. Criando árvore com ordem padrão 3.")
        return BPlusTree(order=3)


def inserir_valor(tree):
    try:
        value = int(input("Digite o valor a ser inserido: "))
        tree.insert(value)
        print(f"✓ Valor {value} inserido com sucesso!")
    except ValueError:
        print("✗ Erro: por favor, digite um número válido.")


def buscar_valor(tree):
    try:
        value = int(input("Digite o valor a ser buscado: "))
        if tree.search(value):
            print(f"✓ Valor {value} encontrado na árvore!")
        else:
            print(f"✗ Valor {value} não encontrado na árvore.")
    except ValueError:
        print("✗ Erro: por favor, digite um número válido.")


def excluir_valor(tree):
    try:
        value = int(input("Digite o valor a ser excluído: "))
        result = tree.delete(value)
        if result is False:
            print(f"✗ Valor {value} não encontrado na árvore.")
        else:
            print(f"✓ Valor {value} excluído com sucesso!")
    except ValueError:
        print("✗ Erro: por favor, digite um número válido.")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"✗ Erro ao excluir: {exc}")


def exibir_arvore(tree, tree_type: str):
    print(f"\n{'=' * 50}")
    print(f"ESTRUTURA DA ÁRVORE {tree_type}")
    print("=" * 50)
    print(tree)

    if isinstance(tree, BPlusTree):
        print("\nLista encadeada de folhas:")
        tree.display_leaves()


def exibir_historico(tree):
    history = tree.get_history()
    print(f"\n{'=' * 50}")
    print("HISTÓRICO DE OPERAÇÕES")
    print("=" * 50)
    if history:
        for index, operation in enumerate(history, 1):
            print(f"{index}. {operation}")
    else:
        print("Nenhuma operação registrada.")
    print("=" * 50)


def limpar_historico(tree):
    tree.clear_history()
    print("✓ Histórico limpo com sucesso!")


def menu_arvore(tree_type: str, create_func):
    tree = None

    while True:
        print_tree_menu(tree_type)

        try:
            choice = input("Escolha uma opção: ").strip()

            if choice == "0":
                break
            if choice == "1":
                tree = create_func()
            elif choice == "2":
                if tree is None:
                    print("✗ Erro: crie uma árvore primeiro (opção 1).")
                else:
                    inserir_valor(tree)
            elif choice == "3":
                if tree is None:
                    print("✗ Erro: crie uma árvore primeiro (opção 1).")
                else:
                    buscar_valor(tree)
            elif choice == "4":
                if tree is None:
                    print("✗ Erro: crie uma árvore primeiro (opção 1).")
                else:
                    excluir_valor(tree)
            elif choice == "5":
                if tree is None:
                    print("✗ Erro: crie uma árvore primeiro (opção 1).")
                else:
                    exibir_arvore(tree, tree_type)
            elif choice == "6":
                if tree is None:
                    print("✗ Erro: crie uma árvore primeiro (opção 1).")
                else:
                    exibir_historico(tree)
            elif choice == "7":
                if tree is None:
                    print("✗ Erro: crie uma árvore primeiro (opção 1).")
                else:
                    limpar_historico(tree)
            else:
                print("✗ Opção inválida. Tente novamente.")
        except KeyboardInterrupt:
            print("\n\nPrograma interrompido pelo usuário.")
            break
        except Exception as exc:  # pylint: disable=broad-except
            print(f"✗ Erro: {exc}")


def main():
    print("Bem-vindo ao Sistema de Árvores B e B+!")

    while True:
        print_menu()

        try:
            choice = input("Escolha uma opção: ").strip()

            if choice == "0":
                print("Encerrando o programa. Até logo!")
                break
            if choice == "1":
                menu_arvore("B", criar_arvore_b)
            elif choice == "2":
                menu_arvore("B+", criar_arvore_bplus)
            else:
                print("✗ Opção inválida. Tente novamente.")
        except KeyboardInterrupt:
            print("\n\nPrograma interrompido pelo usuário. Até logo!")
            break
        except Exception as exc:  # pylint: disable=broad-except
            print(f"✗ Erro: {exc}")


if __name__ == "__main__":
    main()
