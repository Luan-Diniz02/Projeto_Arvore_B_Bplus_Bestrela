# Projeto de Árvores B e B+

Este repositório reúne implementações das estruturas **Árvore B** e **Árvore B+** acompanhadas de uma interface de linha de comando, uma aplicação web em Flask e uma suíte de testes automatizados.

## Estrutura do repositório

- `backend/` – Implementações das árvores (`btree.py`, `bplustree.py`).
- `cli/` – Interface de linha de comando (`main.py`).
- `frontend/web_app/` – Aplicação Flask com templates HTML.
- `tests/` – Testes automatizados para validar o comportamento das árvores.
- `README.md` – Visão geral e instruções de uso.

> Observação: Os pacotes ajustam o `sys.path` automaticamente quando executados diretamente, portanto não é necessário instalar o projeto como módulo.

## Dependências

- Python 3.10+ (desenvolvido com Python 3.12).
- Flask (somente para a aplicação web). Instalação sugerida:

```bash
pip install flask
```

## Como executar

### Linha de comando

```bash
python cli/main.py
```

### Aplicação web

```bash
python frontend/web_app/arvore_web.py
```

Depois de iniciar, acesse `http://127.0.0.1:5000/` no navegador.

### Testes automatizados

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Conceitos rápidos

### Árvore B
- Árvore de busca balanceada com múltiplas chaves por nó.
- Todos os nós folha ficam no mesmo nível.
- A altura é mantida pequena graças a divisões (split) e combinações (merge).

### Árvore B+
- Variação da Árvore B em que todas as chaves residem nas folhas.
- Nós internos possuem somente chaves de roteamento.
- Folhas encadeadas facilitam percursos sequenciais.

## Complexidade

| Operação | Complexidade |
|----------|-------------|
| Busca    | O(log n)    |
| Inserção | O(log n)    |
| Exclusão | O(log n)    |
| Espaço   | O(n)        |

## Referências

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. *Introduction to Algorithms* (3ª edição).
- Knuth, D. E. *The Art of Computer Programming, Volume 3: Sorting and Searching*.
