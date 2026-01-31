# 🌳 Árvore B e B+ - Estruturas de Dados para Bancos de Dados

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Database](https://img.shields.io/badge/Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

**Implementações Completas de Árvore B e B+ com Interface Web**

[Sobre](#-sobre) • [Por que B+ Trees?](#-por-que-b-trees) • [Como Executar](#-como-executar) • [Aplicações](#-aplicações-reais)

</div>

---

## 📖 Sobre

Este projeto implementa as estruturas de dados **Árvore B** e **Árvore B+**, fundamentais para sistemas de gerenciamento de bancos de dados (SGBD) como **MySQL**, **PostgreSQL**, **MongoDB** e **SQLite**.

### 🎯 Objetivo

Demonstrar como estruturas de dados avançadas são aplicadas em sistemas reais, especialmente:
- **Indexação de bancos de dados**
- **Sistemas de arquivos** (NTFS, ext4, Btrfs)
- **Otimização de buscas** em grandes volumes de dados

---

## 🌟 Por que B+ Trees?

### 🗄️ **Base dos Bancos de Dados Modernos**

| SGBD | Uso de B+ Tree |
|------|----------------|
| **MySQL/InnoDB** | Índices primários e secundários |
| **PostgreSQL** | Índices B-tree (padrão) |
| **MongoDB** | Índices WiredTiger |
| **SQLite** | Índices e tabelas |
| **Oracle** | B-tree indexes |

### 💪 **Vantagens das B+ Trees**

✅ **Otimizada para Disco** - Reduz operações de I/O  
✅ **Buscas Eficientes** - O(log n) garantido  
✅ **Range Queries** - Varredura sequencial nas folhas  
✅ **Balanceamento Automático** - Mantém altura equilibrada  
✅ **Cache-Friendly** - Nós maiores aproveitam cache do SO  

---

## ✨ Funcionalidades

### 🌲 **Árvore B**
- ✅ Inserção com split automático
- ✅ Busca eficiente
- ✅ Remoção com merge e redistribuição
- ✅ Todas as chaves acessíveis em qualquer nó
- ✅ Balanceamento automático

### 🌲➕ **Árvore B+**
- ✅ Todas as chaves nas folhas
- ✅ Nós internos como roteadores
- ✅ Folhas encadeadas (linked list)
- ✅ Range queries eficientes
- ✅ Varredura sequencial otimizada

### 🎨 **Interfaces**

#### 🖥️ CLI (Command Line Interface)
- Menu interativo completo
- Inserção, busca e remoção
- Visualização da estrutura
- Testes automatizados

#### 🌐 Web (Flask Application)
- Dashboard responsivo
- Visualização gráfica da árvore
- APIs REST
- Interface intuitiva

---

## 🛠 Tecnologias

- **Python 3.10+** (desenvolvido com Python 3.12)
- **Flask** - Framework web
- **unittest** - Testes automatizados
- **HTML/CSS/JS** - Frontend

---

## 🚀 Como Executar

### Instalação

```bash
# Clonar repositório
git clone https://github.com/Luan-Diniz02/Projeto_Arvore_B_Bplus_Bestrela.git
cd Projeto_Arvore_B_Bplus_Bestrela

# Instalar dependências
pip install flask
```

> **Nota:** O projeto ajusta o `sys.path` automaticamente, não sendo necessário instalá-lo como módulo.

---

### 1️⃣ **Interface CLI**

```bash
python cli/main.py
```

**Menu interativo:**
```
========================================
    Árvore B e B+ - Menu Principal
========================================
1. Inserir chave
2. Buscar chave
3. Remover chave
4. Exibir árvore
5. Executar testes
6. Sair
========================================
```

---

### 2️⃣ **Interface Web**

```bash
python frontend/web_app/arvore_web.py
```

Acesse no navegador:
```
http://127.0.0.1:5000/
```

**Recursos:**
- Escolha entre Árvore B ou B+
- Inserção, busca e remoção visual
- Visualização da estrutura da árvore
- Testes interativos

---

### 3️⃣ **Testes Automatizados**

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📂 Estrutura do Projeto

```
Projeto_Arvore_B_Bplus_Bestrela/
├── backend/
│   ├── btree.py               # Implementação Árvore B
│   └── bplustree.py          # Implementação Árvore B+
├── cli/
│   └── main.py               # Interface CLI
├── frontend/
│   └── web_app/
│       ├── arvore_web.py     # Backend Flask
│       └── templates/        # HTML templates
├── tests/
│   ├── test_btree.py         # Testes Árvore B
│   └── test_bplustree.py     # Testes Árvore B+
└── README.md
```

---

## 🔍 Comparação: Árvore B vs B+

| Característica | Árvore B | Árvore B+ |
|---------------|----------|-----------|
| **Chaves nos nós internos** | ✅ Sim, com dados | ✅ Sim, apenas roteamento |
| **Chaves nas folhas** | ❌ Parcial | ✅ Todas as chaves |
| **Folhas encadeadas** | ❌ Não | ✅ Sim (linked list) |
| **Range queries** | 🟡 Razoável | ✅ Excelente |
| **Uso de espaço** | 🟡 Moderado | ✅ Melhor |
| **Busca individual** | ✅ Rápida | ✅ Rápida |
| **Melhor para** | Acesso aleatório | Bancos de dados |

---

## 📊 Complexidade Computacional

| Operação | Árvore B | Árvore B+ |
|----------|---------|-----------|
| **Busca** | O(log n) | O(log n) |
| **Inserção** | O(log n) | O(log n) |
| **Remoção** | O(log n) | O(log n) |
| **Range Query** | O(log n + k) | **O(log n + k)** ⚡ |
| **Espaço** | O(n) | O(n) |

*k = número de elementos no intervalo*

### Conceitos Rápidos

#### Árvore B
- Árvore de busca balanceada com múltiplas chaves por nó
- Todos os nós folha no mesmo nível
- Altura mantida pequena por divisões (split) e combinações (merge)

#### Árvore B+
- Variação onde todas as chaves residem nas folhas
- Nós internos possuem apenas chaves de roteamento
- Folhas encadeadas facilitam percursos sequenciais

---

## 💡 Aplicações Reais

### 🗄️ **Bancos de Dados**

#### MySQL (InnoDB)
```sql
-- Índice usando B+ Tree
CREATE INDEX idx_usuario_nome ON usuarios(nome);

-- Range query otimizada
SELECT * FROM usuarios WHERE nome BETWEEN 'A' AND 'C';
-- Usa B+ Tree para busca eficiente!
```

#### PostgreSQL
```sql
-- Padrão é B-tree
CREATE INDEX idx_pedidos_data ON pedidos(data_pedido);
```

### 📁 **Sistemas de Arquivos**
- **NTFS** (Windows) - Usa B+ trees para diretórios
- **ext4** (Linux) - HTree (variação de B-tree)
- **Btrfs** - B-trees para metadados

### 🚀 **Outras Aplicações**
- **Elasticsearch** - Índices Lucene
- **Redis** - Sorted sets
- **DynamoDB** - Índices secundários

---

## 🎓 Conceitos Demonstrados

### Algoritmos
- ✅ **Balanceamento de árvores**
- ✅ **Split e merge de nós**
- ✅ **Redistribuição de chaves**
- ✅ **Busca binária em nós**

### Estruturas de Dados
- ✅ **Árvores auto-balanceadas**
- ✅ **Linked lists** (folhas da B+)
- ✅ **Arrays ordenados** (chaves nos nós)

### Otimização
- ✅ **Minimização de I/O**
- ✅ **Cache-friendly design**
- ✅ **Complexidade logarítmica**

---

## 🔄 Roadmap

- [ ] Implementar persistência em disco
- [ ] Adicionar visualização gráfica da árvore
- [ ] Implementar B* tree
- [ ] Criar benchmark comparativo
- [ ] Adicionar suporte a chaves duplicadas
- [ ] Implementar concurrent access (locks)
- [ ] Adicionar métricas de performance

---

## 📚 Referências

- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/9780262046305/)
- [MySQL InnoDB B+ Tree](https://dev.mysql.com/doc/refman/8.0/en/innodb-physical-structure.html)
- [PostgreSQL B-tree Implementation](https://www.postgresql.org/docs/current/btree-implementation.html)
- [Database Internals Book](https://www.databass.dev/)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga o processo padrão:
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 👨‍💻 Autor

**Luan Diniz**

- GitHub: [@Luan-Diniz02](https://github.com/Luan-Diniz02)
- Projeto desenvolvido para **Estrutura de Dados II**

---

## 📄 Licença

Projeto de código aberto para fins educacionais.

---

<div align="center">

**🌳 A base dos bancos de dados modernos!**

*Desenvolvido com foco em estruturas de dados aplicadas a sistemas reais*

</div>