# Algoritmo de Vizing

Este projeto implementa o **Algoritmo de Vizing**, que garante que qualquer grafo simples pode ter suas arestas coloridas usando no máximo **Δ + 1 cores**, onde Δ é o grau máximo do grafo.  
A classe `Vizing` recebe uma matriz de adjacência e retorna a coloração das arestas.

## Exemplo de uso

```python
from vizing import Vizing

# Grafo representado como matriz de adjacência
grafo = [
    [0, 1, 1, 0],
    [1, 0, 1, 0],
    [1, 1, 0, 1],
    [0, 0, 1, 0]
]

v = Vizing()
coloracao = v.colorir_grafo(grafo)

print(coloracao)

# Saída esperada:
# {
#     (0, 1): 0,
#     (0, 2): 1,
#     (1, 2): 2,
#     (2, 3): 0
# }
