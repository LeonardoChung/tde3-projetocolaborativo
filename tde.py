import os
import re
from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.order = 0
        self.size = 0

    def __str__(self):
        return self.print_adj_list()

    def save_adj_list(self, txt):

        with open(txt, "w") as f:

            for v in self.graph:
                linha = f"{v}: "
                for edge in self.graph[v]:
                    linha += f"('{edge[0]}', {edge[1]}) -> "
                linha = linha.rstrip(" -> ")
                f.write(linha + "\n")

    def node_exists(self, v):
        if v in self.graph:
            return v in self.graph
        else:
            return False

    def edge_exists(self, u, v):
        for edge in self.graph[u]:
            if edge[0] == v:
                return True
        return False

    def enter_degree(self, u):
        if self.node_exists(u):
          count = 0
          for v in self.graph:
              for edge in self.graph[v]:
                  if edge[0] == u:
                      count += 1
          return count
        else:
            return None

    def out_degree(self, u):
        if self.node_exists(u):
            return len(self.graph[u])
        else:
            return None

    def degree(self, u):
        if self.node_exists(u):
            return self.enter_degree(u) + self.out_degree(u)
        else:
            return None

    def get_weight(self, u, v):
        for edge in self.graph[u]:
            if edge[0] == v:
                return edge[1]
        return None

    def valid_weight(self, w):
        if w > 0:
            return True
        else:
            print("The weight cannot be negative!")
            return False

    def add_node(self, v):
        if self.node_exists(v):
            print("This node already exists in the graph!")
        else:
            self.graph[v] = []
            self.order += 1

    def add_edge(self, u, v, w):
        if self.valid_weight(w):
            if not self.node_exists(u):
                self.add_node(u)
            if not self.node_exists(v):
                self.add_node(v)

            if self.edge_exists(u, v):
                for i in range(len(self.graph[u])):
                    if self.graph[u][i][0] == v:
                        self.graph[u][i] = (v, w)
            else:
                self.graph[u].append((v, w))
                self.size += 1
            return True
        else:
            return False

    def remove_edge(self, u, v):
        if (self.node_exists(u) and self.node_exists(v)) and (self.edge_exists(u, v)):
            temp_size = len(self.graph[u])
            self.graph[u] = [edge for edge in self.graph[u] if edge[0] != v]
            remove_size = temp_size - len(self.graph[u])
            self.size -= remove_size
        else:
            print(f"Edge ({u, v}) cannot be removed!")

    def remove_node(self, v):
        if self.node_exists(v):
            self.size -= len(self.graph[v])
            self.graph.pop(v)
            self.order -= 1

            for u in self.graph:
                temp_size = len(self.graph[u])
                self.graph[u] = [edge for edge in self.graph[u] if edge[0] != v]
                remove_size = temp_size - len(self.graph[u])
                self.size -= remove_size
        else:
            print(f"Node {v} cannot be removed")

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

            if not os.path.isfile(caminho_arquivo):
                continue

            with open(caminho_arquivo, "r") as a:
                conteudo = a.read()

            f = r'(?:From:)\s*([\w\.-]+@[\w\.-]+)'
            to = r'(?:To:)\s*([\w\.-]+@[\w\.-]+)'

            emails_from = re.findall(f, conteudo)
            emails_to = re.findall(to, conteudo)

            if emails_from and emails_to:
                    remetente = emails_from[0].lower()
                    # caso tenha vários emails de destinatarios separados por vírgula
                    destinatarios = re.split(r'[,\s]+', emails_to[0])
                    destinatarios_filtrados = []

                    # filtrar somente emails validos
                    for d in destinatarios:
                        # se tiver um @ do email
                        if "@" in d:
                            # strip retira espaços extras
                            d = d.strip().lower()
                            destinatarios_filtrados.append(d)

                    destinatarios = destinatarios_filtrados

                    # caso não tenha nenhum destinatário ignora o vértice
                    if not destinatarios:
                        continue

                    # para cada um dos destinatários
                    for destinatario in destinatarios:

                        # Se já existir a aresta, incrementa o peso + 1
                        if grafo.edge_exists(remetente, destinatario):
                            peso_atual = grafo.get_weight(remetente, destinatario)
                            grafo.add_edge(remetente, destinatario, peso_atual + 1)
                        else:
                            grafo.add_edge(remetente, destinatario, 1)

grafo.save_adj_list("lista_de_adjacencias.txt")

# PART 2

def getOrder(graph):
    return graph.order

print(f"Graph order: {getOrder(grafo)}")

def getSize(graph):
    return graph.size

print(f"Graph size: {getSize(grafo)}")

def getIsolatedVertices(graph):
    count = 0
    for key in graph.graph:
        if graph.graph[key] == []:
            count +=1

    return count

print(f"Graph isolated vertices: {getIsolatedVertices(grafo)}\n")

def getMaximumOutDegrees(graph):
    vertices = []

    for key in graph.graph:
        outDegree = graph.out_degree(key)
        vertices.append((key, outDegree))

    sortedVertices = sorted(vertices, key=lambda x: x[1], reverse=True)

    return sortedVertices[:20]


print(f"Graph top 20 vertices with highest out-degree of the graph: \n")

for i in range(0, len(getMaximumOutDegrees(grafo))):
    print(f"{i + 1}: Email: {getMaximumOutDegrees(grafo)[i][0]} | Out Degree: {getMaximumOutDegrees(grafo)[i][1]}")

def getMaximumEnterDegrees(graph):
    vertices = []

    for key in graph.graph:
        enterDegree = graph.enter_degree(key)
        vertices.append((key, enterDegree))

    sortedVertices = sorted(vertices, key=lambda x: x[1], reverse=True)

    return sortedVertices[:20]

print(f"\nGraph top 20 vertices with highest in-degree of the graph: \n")

for i in range(0, len(getMaximumEnterDegrees(grafo))):
    print(f"{i + 1}: Email: {getMaximumEnterDegrees(grafo)[i][0]} | Enter Degree: {getMaximumEnterDegrees(grafo)[i][1]}")


# PART 3
def conexo(graph):
    def dfs(v, visited, g):
        visited.add(v)
        for neighbor in g.graph[v]:
            if neighbor[0] not in visited:
                dfs(neighbor[0], visited, g)

    if not graph.graph:
        return True  # grafo vazio é considerado fortemente conexo

    start_node = next(iter(graph.graph))
    visited = set()
    dfs(start_node, visited, graph)
    if len(visited) != len(graph.graph):
        return False

    # cria o grafo transposto
    transposto = Graph()
    for u in graph.graph:
        for v, w in graph.graph[u]:
            transposto.add_edge(v, u, w) # aresta invertida

    visited = set()
    dfs(start_node, visited, transposto)
    if len(visited) != len(transposto.graph):
        return False

    return True


def eureliano(graph, nome_arquivo_saida):
    eureliano = True
    motivos = []
    balanceados = []

    if not conexo(graph):
        eureliano = False
        motivos.append("O grafo não é fortemente conexo.")

    for node in graph.graph:
        in_degree = graph.enter_degree(node)
        out_degree = graph.out_degree(node)
        if in_degree != out_degree:
            eureliano = False
            motivos.append(f"O vértice '{node}' tem grau de entrada {in_degree} e grau de saída {out_degree}.")
        else: 
            balanceados.append(f"O vértice '{node}' tem grau de entrada e saída iguais: {in_degree}.")
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("🔎 Verificação de Eulerianidade do grafo:\n")
        if eureliano:
            f.write("O grafo é Eureliiano.\n")
        else:
            f.write("O grafo NÃO é Eureliano. Motivos:\n")
            for motivo in motivos:
                f.write(f" - {motivo}\n")
        f.write(" Vértices com grau de entrada igual ao grau de saída:\n")
        for linha in balanceados:
            f.write(f" - {linha}\n")

    return eureliano


eureliano(grafo, "verificacao_eureliano.txt")

def conexo(graph):
    def dfs(v, visited, g):
        visited.add(v)
        for neighbor in g.graph[v]:
            if neighbor[0] not in visited:
                dfs(neighbor[0], visited, g)

    if not graph.graph:
        return True  # grafo vazio é considerado fortemente conexo

    start_node = next(iter(graph.graph))
    visited = set()
    dfs(start_node, visited, graph)
    if len(visited) != len(graph.graph):
        return False

    # cria o grafo transposto
    transposto = Graph()
    for u in graph.graph:
        for v, w in graph.graph[u]:
            transposto.add_edge(v, u, w) # aresta invertida

    visited = set()
    dfs(start_node, visited, transposto)
    if len(visited) != len(transposto.graph):
        return False

    return True


def eureliano(graph, nome_arquivo_saida):
    eureliano = True
    motivos = []
    balanceados = []

    if not conexo(graph):
        eureliano = False
        motivos.append("O grafo não é fortemente conexo.")

    for node in graph.graph:
        in_degree = graph.enter_degree(node)
        out_degree = graph.out_degree(node)
        if in_degree != out_degree:
            eureliano = False
            motivos.append(f"O vértice '{node}' tem grau de entrada {in_degree} e grau de saída {out_degree}.")
        else: 
            balanceados.append(f"O vértice '{node}' tem grau de entrada e saída iguais: {in_degree}.")
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("🔎 Verificação de Eulerianidade do grafo:\n")
        if eureliano:
            f.write("O grafo é Eureliiano.\n")
        else:
            f.write("O grafo NÃO é Eureliano. Motivos:\n")
            for motivo in motivos:
                f.write(f" - {motivo}\n")
        f.write(" Vértices com grau de entrada igual ao grau de saída:\n")
        for linha in balanceados:
            f.write(f" - {linha}\n")

    return eureliano


eureliano(grafo, "verificacao_eureliano.txt")


def conexo(graph):
    def dfs(v, visited, g):
        visited.add(v)
        for neighbor in g.graph[v]:
            if neighbor[0] not in visited:
                dfs(neighbor[0], visited, g)

    if not graph.graph:
        return True  # grafo vazio é considerado fortemente conexo

    start_node = next(iter(graph.graph))
    visited = set()
    dfs(start_node, visited, graph)
    if len(visited) != len(graph.graph):
        return False

    # cria o grafo transposto
    transposto = Graph()
    for u in graph.graph:
        for v, w in graph.graph[u]:
            transposto.add_edge(v, u, w) # aresta invertida

    visited = set()
    dfs(start_node, visited, transposto)
    if len(visited) != len(transposto.graph):
        return False

    return True


def eureliano(graph, nome_arquivo_saida):
    eureliano = True
    motivos = []
    balanceados = []

    if not conexo(graph):
        eureliano = False
        motivos.append("O grafo não é fortemente conexo.")

    for node in graph.graph:
        in_degree = graph.enter_degree(node)
        out_degree = graph.out_degree(node)
        if in_degree != out_degree:
            eureliano = False
            motivos.append(f"O vértice '{node}' tem grau de entrada {in_degree} e grau de saída {out_degree}.")
        else: 
            balanceados.append(f"O vértice '{node}' tem grau de entrada e saída iguais: {in_degree}.")
    with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        f.write("🔎 Verificação de Eulerianidade do grafo:\n")
        if eureliano:
            f.write("O grafo é Eureliiano.\n")
        else:
            f.write("O grafo NÃO é Eureliano. Motivos:\n")
            for motivo in motivos:
                f.write(f" - {motivo}\n")
        f.write(" Vértices com grau de entrada igual ao grau de saída:\n")
        for linha in balanceados:
            f.write(f" - {linha}\n")

    return eureliano


eureliano(grafo, "verificacao_eureliano.txt")

resultado = eureliano(grafo, "verificacao_eureliano.txt")
print("É eureliano?" , resultado)
