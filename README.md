# Dimensionamento Geométrico Fotovoltaico ☀️

Este projeto consiste em uma ferramenta em Python desenvolvida para automação do estudo preliminar e arranjo geométrico bidimensional (*Grid-Based Packing*) de painéis fotovoltaicos sobre superfícies retangulares (telhados). 

O algoritmo calcula a quantidade máxima de módulos que podem ser alocados em duas orientações distintas (Retrato e Paisagem), respeitando restrições físicas de segurança e gerando uma estrutura de dados robusta para futuras integrações visuais.

## 🚀 Funcionalidades

* **Abordagem Heurística (*Greedy Grid*):** Varredura analítica que preenche a área útil otimizando o espaçamento entre módulos.
* **Zonas de Exclusão Avançadas:** Implementação de recuo perimetral mínimo nas bordas (0,5 m) e restrição por distância Euclidiana nas quinas do telhado (1,0 m).
* **Estrutura com Pandas:** Exportação dos dados gerados para um `DataFrame` contendo as coordenadas `(X, Y)` exatas dos quatro vértices de cada painel.

