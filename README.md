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

### 💪 **Vantagens das B+ Trees**

✅ **Otimizada para Disco** - Reduz operações de I/O  
✅ **Buscas Eficientes** - O(log n) garantido  
✅ **Range Queries** - Varredura sequencial nas folhas  
✅ **Balanceamento Automático** - Mantém altura equilibrada  

---

## ✨ Funcionalidades

### 🌲 **Árvore B**
- ✅ Inserção com split automático
- ✅ Busca eficiente O(log n)
- ✅ Remoção com merge e redistribuição
- ✅ Balanceamento automático

### 🌲➕ **Árvore B+**
- ✅ Todas as chaves nas folhas
- ✅ Nós internos como roteadores
- ✅ Folhas encadeadas (linked list)
- ✅ Range queries otimizadas

---

## 🚀 Como Executar

### Instalação

```bash
# Clonar repositório
git clone https://github.com/Luan-Diniz02/Projeto_Arvore_B_Bplus_Bestrela.git
cd Projeto_Arvore_B_Bplus_Bestrela

# Instalar dependências
pip install flask
