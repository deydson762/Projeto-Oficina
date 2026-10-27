"""
Módulo de Controle de Atendimento.
Combinação de estruturas: Fila normal + Fila de prioridade (guincho).
"""

from datetime import datetime


# ===== ESTRUTURA DE DADOS: FILA (FIFO) =====
class NoFila:
    """Nó da fila."""
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class Fila:
    """Fila genérica FIFO."""
    def __init__(self):
        self.frente = None
        self.tras = None
        self.tamanho = 0

    def vazia(self):
        return self.frente is None

    def tamanho_fila(self):
        return self.tamanho

    def enfileirar(self, dado):
        novo_no = NoFila(dado)
        if self.vazia():
            self.frente = novo_no
            self.tras = novo_no
        else:
            self.tras.proximo = novo_no
            self.tras = novo_no
        self.tamanho += 1

    def desenfileirar(self):
        if self.vazia():
            return None
        dado = self.frente.dado
        self.frente = self.frente.proximo
        if self.frente is None:
            self.tras = None
        self.tamanho -= 1
        return dado

    def frente_fila(self):
        if self.vazia():
            return None
        return self.frente.dado

    def listar_todos(self):
        elementos = []
        atual = self.frente
        while atual is not None:
            elementos.append(atual.dado)
            atual = atual.proximo
        return elementos


# ===== CLASSES DO DOMÍNIO =====
class VeiculoEspera:
    """Representa um veículo aguardando atendimento."""
    def __init__(self, placa, nome_cliente, queixa, eh_guincho=False):
        self.placa = placa
        self.nome_cliente = nome_cliente
        self.queixa = queixa
        self.eh_guincho = eh_guincho
        self.data_hora_chegada = datetime.now()

    def tempo_espera(self):
        """Retorna o tempo de espera em segundos."""
        return (datetime.now() - self.data_hora_chegada).total_seconds()

    def __str__(self):
        guincho_str = "[GUINCHO] " if self.eh_guincho else ""
        tempo = self.tempo_espera()
        return f"{guincho_str}{self.placa} | {self.nome_cliente} | {self.queixa} | Espera: {tempo:.0f}s"

    def __repr__(self):
        return self.__str__()


class GerenciadorFila:
    """
    Gerenciador de fila de atendimento.
    Combinação: Fila normal + Fila de prioridade (guincho).
    """
    def __init__(self, num_boxes=3):
        self.fila_normal = Fila()
        self.fila_guincho = Fila()
        self.num_boxes = num_boxes
        self.boxes_ocupados = 0

    def adicionar_veiculo(self, placa, nome_cliente, queixa, eh_guincho=False):
        """Adiciona um veículo à fila de espera."""
        veiculo = VeiculoEspera(placa, nome_cliente, queixa, eh_guincho)
        if eh_guincho:
            self.fila_guincho.enfileirar(veiculo)
            return True, f"Veículo {placa} adicionado à fila de guincho"
        else:
            self.fila_normal.enfileirar(veiculo)
            return True, f"Veículo {placa} adicionado à fila normal"

    def proximo_veiculo(self):
        """
        Retorna o próximo veículo a ser atendido.
        Prioridade: fila de guincho > fila normal.
        """
        # Primeiro verifica fila de guincho
        if not self.fila_guincho.vazia():
            return self.fila_guincho.desenfileirar()
        # Se não houver guincho, vai para fila normal
        if not self.fila_normal.vazia():
            return self.fila_normal.desenfileirar()
        return None

    def box_liberado(self):
        """
        Simula a liberação de um box e retorna o próximo veículo.
        """
        if self.boxes_ocupados > 0:
            self.boxes_ocupados -= 1

        proximo = self.proximo_veiculo()
        if proximo:
            self.boxes_ocupados += 1
            return True, proximo
        return False, None

    def tamanho_total(self):
        """Retorna o tamanho total da fila (normal + guincho)."""
        return self.fila_normal.tamanho_fila() + self.fila_guincho.tamanho_fila()

    def buscar_por_placa(self, placa):
        """Busca um veículo pela placa em ambas as filas."""
        # Busca na fila de guincho
        for veiculo in self.fila_guincho.listar_todos():
            if veiculo.placa == placa:
                return veiculo
        # Busca na fila normal
        for veiculo in self.fila_normal.listar_todos():
            if veiculo.placa == placa:
                return veiculo
        return None

    def remover_por_placa(self, placa):
        """Remove um veículo da fila pela placa."""
        # Cria novas filas sem o veículo a remover
        nova_fila_guincho = Fila()
        nova_fila_normal = Fila()
        removido = False

        # Processa fila de guincho
        while not self.fila_guincho.vazia():
            veiculo = self.fila_guincho.desenfileirar()
            if veiculo.placa == placa and not removido:
                removido = True
            else:
                nova_fila_guincho.enfileirar(veiculo)

        # Processa fila normal
        while not self.fila_normal.vazia():
            veiculo = self.fila_normal.desenfileirar()
            if veiculo.placa == placa and not removido:
                removido = True
            else:
                nova_fila_normal.enfileirar(veiculo)

        self.fila_guincho = nova_fila_guincho
        self.fila_normal = nova_fila_normal

        if removido:
            return True, "Veículo removido da fila"
        return False, "Veículo não encontrado na fila"

    def relatorio_fila(self):
        """Gera relatório da fila de espera."""
        relatorio = []
        relatorio.append(f"=== FILA DE ESPERA ===")
        relatorio.append(f"Boxes disponíveis: {self.num_boxes - self.boxes_ocupados}/{self.num_boxes}")
        relatorio.append(f"Total aguardando: {self.tamanho_total()}")
        relatorio.append("")

        # Fila de guincho (prioridade)
        guinchos = self.fila_guincho.listar_todos()
        if guinchos:
            relatorio.append("--- FILA DE GUINCHO (PRIORIDADE) ---")
            for i, veiculo in enumerate(guinchos, 1):
                relatorio.append(f"{i}. {veiculo}")
            relatorio.append("")
        else:
            relatorio.append("--- FILA DE GUINCHO (vazia) ---")
            relatorio.append("")

        # Fila normal
        normais = self.fila_normal.listar_todos()
        if normais:
            relatorio.append("--- FILA NORMAL ---")
            for i, veiculo in enumerate(normais, 1):
                relatorio.append(f"{i}. {veiculo}")
            relatorio.append("")
        else:
            relatorio.append("--- FILA NORMAL (vazia) ---")
            relatorio.append("")

        return "\n".join(relatorio)
