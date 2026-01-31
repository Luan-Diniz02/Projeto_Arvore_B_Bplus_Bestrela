# Project Documentation

## Badges
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![CI](https://img.shields.io/badge/ci-passing-brightgreen)

## Introduction
This project implements B and B+ trees, which are specialized data structures commonly used in databases and file systems.

## B and B+ Trees
### B Tree
A B Tree is a balanced tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time.

### B+ Tree
A B+ Tree is an extension of a B Tree, in which all values are found in the leaf nodes. It is optimized for systems that read and write large blocks of data.

## Applications in Databases
- **MySQL**: Uses B+ Trees for indexing data.
- **PostgreSQL**: Utilizes B Trees and B+ Trees for various indexing strategies.

## Complexity Analysis
Both B and B+ trees have a logarithmic time complexity for search operations, which is ideal for large datasets.

## How to Execute Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Luan-Diniz02/Projeto_Arvore_B_Bplus_Bestrela.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Projeto_Arvore_B_Bplus_Bestrela
   ```
3. Compile and run the project according to the instructions in the **docs** folder.

## Project Structure
- **src/**: Contains the source code.
- **docs/**: Contains documentation and instructions.
- **tests/**: Contains test cases for various functionalities.

## Comparison between B and B+ Trees
| Feature             | B Tree      | B+ Tree      |
|---------------------|-------------|--------------|
| Leaf Nodes          | Data & Pointers | Only Pointers to Data  |
| Search Complexity    | O(log n)    | O(log n)      |
| Space Utilization    | Less efficient | More efficient |
| Range Queries        | Possible     | More efficient in range queries |

## Conclusion
This project provides a solid understanding of B and B+ trees and their applications, offering insights into their implementation and advantages in database systems.