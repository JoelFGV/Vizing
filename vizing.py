class Vizing:
    def colorir_grafo(self, grafo):
        """Aplica o algoritmo de Vizing para colorir as arestas do grafo dado."""
        vertices = {i for i in range(len(grafo))}
        arestas = self.matriz_adj_para_arestas(grafo)
        
        # Inicializa o estado da coloração
        self.arestas_cor = {aresta: None for aresta in arestas}
        self.vertices_cores_livres = self.obter_vertices_cores_livres(grafo)
        self.vertices_vizinhos = self.obter_vertices_vizinhos(vertices, arestas)

        # Processa cada aresta seguindo os casos do algoritmo
        for aresta_atual in arestas:
            vertice_u = aresta_atual[0]
            
            # Tenta colorir diretamente
            if self.colorir_diretamente(aresta_atual):
                continue
            
            # Cria fan e trata situação conforme tipo
            fan, caso = self.criar_fan(aresta_atual)
            if caso == 1:  # Último vértice do fan tem cor livre comum com u
                self.trocar_cores_fan(vertice_u, fan)
            elif caso == 2:  # Nenhum vértice do fan tem cor livre comum com u
                fan_modificado = self.alternar_cores(vertice_u, fan)
                self.trocar_cores_fan(vertice_u, fan_modificado)
                
        return self.arestas_cor

    def colorir_diretamente(self, aresta):
        """Tenta colorir a aresta diretamente com uma cor livre comum entre os vértices."""
        vertice_u, vertice_v = aresta
        cor_selecionada = self.obter_cor_livre_comum(vertice_u, vertice_v)
        if cor_selecionada is None:
            return False
        
        self.colorir_aresta(aresta, cor_selecionada)
        return True
        
    def criar_fan(self, aresta):
        """Constrói o fan com base em uma aresta e retorna o tipo de situação encontrada."""
        vertice_u, vertice_v = aresta
        vizinhos_candidatos = self.vertices_vizinhos[vertice_u].copy()
        
        fan = [vertice_v]
        fan_cores_arestas = set()
        
        # Expande o fan conforme a definição do algoritmo
        while True:
            for vizinho_w in vizinhos_candidatos:
                aresta_uw = self.obter_aresta_valida(vertice_u, vizinho_w)
                cor_uw = self.arestas_cor[aresta_uw]
                
                if cor_uw in self.vertices_cores_livres[fan[-1]]:
                    fan.append(vizinho_w)
                    fan_cores_arestas.add(cor_uw)
                    vizinhos_candidatos.discard(vizinho_w)
                    break
            else:
                return (fan, 2)  # Não foi possível expandir mais
            
            if self.obter_cor_livre_comum(vertice_u, fan[-1]) is not None:
                return (fan, 1)  # Achou cor livre comum
            if self.vertices_cores_livres[fan[-1]].intersection(fan_cores_arestas):
                return (fan, 2)  # Colisão de cores entre arestas do fan
            
    def trocar_cores_fan(self, vertice_u, fan):
        """Recolore as arestas do fan, iniciando pela última posição até a primeira."""
        cor_liberada = self.obter_cor_livre_comum(vertice_u, fan[-1])
        for vertice_w in fan[::-1]:
            aresta_uw = self.obter_aresta_valida(vertice_u, vertice_w)
            cor_liberada = self.colorir_aresta(aresta_uw, cor_liberada)

    def alternar_cores(self, vertice_u, fan):
        """
        Alterna cores ao longo de um caminho colorido seguindo o algoritmo de Vizing.
        Retorna uma versão possivelmente reduzida do fan.
        """
        ultimo_vertice_fan = fan[-1]
        ultimo_vertice_fan_cores_livres = self.vertices_cores_livres[ultimo_vertice_fan]
        
        # Parte 1: encontra aresta (u, w) para alternância
        for vertice_w_indice, vertice_w in enumerate(fan[1:], start=1):
            aresta_uw = self.obter_aresta_valida(vertice_u, vertice_w)
            cor_uw = self.arestas_cor[aresta_uw]
            if cor_uw in ultimo_vertice_fan_cores_livres:
                break
        
        aresta_selecionada = self.obter_aresta_valida(vertice_u, vertice_w)
        
        # Parte 2: escolhe cores a alternar ao longo do caminho
        cor_livre_u = next(iter(self.vertices_cores_livres[vertice_u]))
        cor_aresta_selecionada = self.arestas_cor[aresta_selecionada]
        cores_selecionadas = (cor_livre_u, cor_aresta_selecionada)
        
        # Parte 3: forma caminho alternante e remove coloração temporariamente
        caminho = [aresta_selecionada]
        self.colorir_aresta(aresta_selecionada, None)
        cor_atual_i = 0
        vertice_atual = vertice_w
        
        while True:
            cor_procurada = cores_selecionadas[cor_atual_i]
            cor_atual_i = 1 - cor_atual_i
            for vizinho_x in self.vertices_vizinhos[vertice_atual]:
                aresta_ax = self.obter_aresta_valida(vertice_atual, vizinho_x)
                if self.arestas_cor[aresta_ax] == cor_procurada:
                    caminho.append(aresta_ax)
                    self.colorir_aresta(aresta_ax, None)
                    vertice_atual = vizinho_x
                    break
            else:
                break

        # Parte 4: recolore o caminho com as cores trocadas
        for i, aresta_caminho in enumerate(caminho):
            cor_nova = cores_selecionadas[i % 2]
            self.colorir_aresta(aresta_caminho, cor_nova)
        
        # Retorna o fan modificado
        if vertice_atual != fan[vertice_w_indice - 1]:
            return fan[:vertice_w_indice]
        return fan

    # Auxiliares internos ------------------------------------------------------
    def obter_cor_livre_comum(self, vertice_u, vertice_v):
        """Retorna a menor cor livre comum entre os vértices u e v, se existir."""
        cores_u = self.vertices_cores_livres[vertice_u]
        cores_v = self.vertices_cores_livres[vertice_v]
        if cores_u < cores_v:
            cores_u, cores_v = cores_u, cores_v
        
        for cor in cores_u:
            if cor in cores_v:
                return cor
        return None
    
    def colorir_aresta(self, aresta, nova_cor):
        """Atualiza a cor de uma aresta e ajusta os conjuntos de cores livres."""
        vertice_u, vertice_v = aresta
        cores_livres_u = self.vertices_cores_livres[vertice_u]
        cores_livres_v = self.vertices_cores_livres[vertice_v]
        
        cor_atual = self.arestas_cor[aresta]
        if cor_atual is not None:
            cores_livres_u.add(cor_atual)
            cores_livres_v.add(cor_atual)
        
        if nova_cor is not None:
            cores_livres_u.discard(nova_cor)
            cores_livres_v.discard(nova_cor)

        self.arestas_cor[aresta] = nova_cor
        return cor_atual

    # Auxiliares externos ------------------------------------------------------
    @staticmethod
    def obter_aresta_valida(u, v):
        """Retorna uma tupla ordenada representando a aresta (u, v)."""
        return (u, v) if u < v else (v, u)

    @staticmethod
    def matriz_adj_para_arestas(matriz_adj):
        """Converte matriz de adjacência em lista de arestas."""
        arestas = []
        for u in range(len(matriz_adj)):
            for v in range(u + 1, len(matriz_adj)):
                if matriz_adj[u][v]:
                    arestas.append((u, v))
        return arestas

    @staticmethod
    def obter_vertices_cores_livres(grafo):
        """Inicializa as cores livres para cada vértice com base no grau máximo."""
        maior_grau = max(sum(linha) for linha in grafo)
        cores = list(range(maior_grau + 1))
        return {vertice: set(cores) for vertice in range(len(grafo))}

    @staticmethod
    def obter_vertices_vizinhos(vertices, arestas):
        """Constrói dicionário: vértice → conjunto de vizinhos."""
        vizinhos = {v: set() for v in vertices}
        for u, v in arestas:
            vizinhos[u].add(v)
            vizinhos[v].add(u)
        return vizinhos
