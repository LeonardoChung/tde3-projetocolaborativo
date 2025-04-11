import os
from Functions.Graph import Graph # Classe Grafo
from Functions.ProcessFile import processar_arquivo # Função da PART 1
from Functions.ExtractGraph import getOrder, getSize, getIsolatedVertices, getMaximumOutDegrees, getMaximumEnterDegrees # Funções da PART 2
from Functions.Eulerian import euleriano # Funções da PART 3
from Functions.Dijkstra import dijkstra_diametro, dijkstra_distancia # Funções PART 4 e 5

# PART 1
path = "Amostra Enron - 2016/"
caminhos = os.listdir(path) 

grafo = Graph()

for caminho in caminhos:
    c = path + caminho + "/"
    caminhos2 = os.listdir(c)

    for caminho2 in caminhos2:
        caminho3 = c + caminho2 + "/"
        arquivos = os.listdir(caminho3)

        for arquivo in arquivos:
            caminho_arquivo = caminho3 + arquivo

            # Verifica se é realmente um arquivo (ignora diretórios)
            if os.path.isfile(caminho_arquivo):
                processar_arquivo(caminho_arquivo, grafo)
            else:
                # Se for pasta, processa os arquivos dentro dela também
                subarquivos = os.listdir(caminho_arquivo)
                for arquivo_dentro in subarquivos:
                    caminho_final = caminho_arquivo + "/" + arquivo_dentro
                    if os.path.isfile(caminho_final):
                        processar_arquivo(caminho_final, grafo)


grafo.save_adj_list("lista_de_adjacencias.txt")

# PART 2

print("Informações sobre o grafo: \n")

print(f"Graph order: {getOrder(grafo)}")
print(f"Graph size: {getSize(grafo)}")
print(f"Graph isolated vertices: {getIsolatedVertices(grafo)}\n")

print(f"Graph top 20 vertices with highest out-degree of the graph: \n")

for i in range(0, len(getMaximumOutDegrees(grafo))):
    print(f"{i + 1}: Email: {getMaximumOutDegrees(grafo)[i][0]} | Out Degree: {getMaximumOutDegrees(grafo)[i][1]}")

print(f"\nGraph top 20 vertices with highest enter-degree of the graph: \n")

for i in range(0, len(getMaximumEnterDegrees(grafo))):
    print(f"{i + 1}: Email: {getMaximumEnterDegrees(grafo)[i][0]} | Enter Degree: {getMaximumEnterDegrees(grafo)[i][1]}")


# PART 3

resultado = euleriano(grafo)
print(f"\nÉ eurealiano? {resultado}\n")

# PART 4

node = 'jons@amerexenergy.com'
distance = 1
print(f"\nLista de vértices que estão localizados até uma distância {distance} do vértice {node}: \n{dijkstra_distancia(grafo, node, distance)}\n")

# PART 5

diametro, caminho = dijkstra_diametro(grafo)
print(f"\nDiâmetro do grafo: {diametro}\n")
print("Caminho mais longo (menor caminho mais longo):")
for v in caminho:
    print("->", v)

