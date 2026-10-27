"""
Módulo de Ordem de Serviço (OS).
Gerencia as ordens de serviço abertas na oficina.
"""

from datetime import datetime


# ===== ESTRUTURA DE DADOS: LISTA ENCADEADA =====
class NoLista:
    """Nó da lista encadeada."""
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class Lista:
    """Lista encadeada genérica."""
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0

    def vazia(self):
        return self.cabeca is None

    def tamanho_lista(self):
        return self.tamanho

    def inserir_final(self, dado):
        novo_no = NoLista(dado)
        if self.vazia():
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no
        self.tamanho += 1

    def buscar(self, chave, funcao_chave):
        atual = self.cabeca
        while atual is not None:
            if funcao_chave(atual.dado) == chave:
                return atual.dado
            atual = atual.proximo
        return None

    def remover_por_chave(self, chave, funcao_chave):
        if self.vazia():
            return False
        if funcao_chave(self.cabeca.dado) == chave:
            self.cabeca = self.cabeca.proximo
            self.tamanho -= 1
            return True
        atual = self.cabeca
        while atual.proximo is not None:
            if funcao_chave(atual.proximo.dado) == chave:
                atual.proximo = atual.proximo.proximo
                self.tamanho -= 1
                return True
            atual = atual.proximo
        return False

    def listar_todos(self):
        elementos = []
        atual = self.cabeca
        while atual is not None:
            elementos.append(atual.dado)
            atual = atual.proximo
        return elementos


# ===== CLASSES DO DOMÍNIO =====
class ItemOS:
    """Representa um item da OS (peça ou serviço)."""
    def __init__(self, codigo, descricao, valor, tipo):
        self.codigo = codigo  # Código da peça ou identificador do serviço
        self.descricao = descricao
        self.valor = valor
        self.tipo = tipo  # "peca" ou "servico"

    def __str__(self):
        return f"{self.tipo.upper()}: {self.descricao} ({self.codigo}) - R$ {self.valor:.2f}"

    def __repr__(self):
        return self.__str__()


class OS:
    """Representa uma Ordem de Serviço."""
    def __init__(self, numero_os, placa, nome_cliente, mecanico):
        self.numero_os = numero_os
        self.placa = placa
        self.nome_cliente = nome_cliente
        self.mecanico = mecanico
        self.data_hora_abertura = datetime.now()
        self.data_hora_fechamento = None
        self.itens = Lista()  # Lista de peças e serviços
        self.remontagem_concluida = False
        self.fechada = False

    def adicionar_item(self, codigo, descricao, valor, tipo):
        """Adiciona um item (peça ou serviço) à OS."""
        if self.fechada:
            return False, "OS já fechada, não é possível adicionar itens"
        item = ItemOS(codigo, descricao, valor, tipo)
        self.itens.inserir_final(item)
        return True, f"{tipo} adicionado à OS"

    def remover_item(self, codigo):
        """Remove um item da OS pelo código."""
        if self.fechada:
            return False, "OS já fechada, não é possível remover itens"
        if self.itens.remover_por_chave(codigo, lambda i: i.codigo):
            return True, "Item removido da OS"
        return False, "Item não encontrado na OS"

    def concluir_remontagem(self):
        """Marca a remontagem como concluída."""
        self.remontagem_concluida = True
        return True, "Remontagem concluída"

    def pode_fechar(self):
        """Verifica se a OS pode ser fechada."""
        return self.remontagem_concluida and not self.fechada

    def fechar(self):
        """Fecha a OS."""
        if not self.pode_fechar():
            return False, "Não é possível fechar a OS (remontagem não concluída ou já fechada)"
        self.data_hora_fechamento = datetime.now()
        self.fechada = True
        return True, "OS fechada com sucesso"

    def calcular_total_pecas(self):
        """Calcula o total de peças."""
        total = 0
        for item in self.itens.listar_todos():
            if item.tipo == "peca":
                total += item.valor
        return total

    def calcular_total_servicos(self):
        """Calcula o total de serviços."""
        total = 0
        for item in self.itens.listar_todos():
            if item.tipo == "servico":
                total += item.valor
        return total

    def calcular_total(self):
        """Calcula o total da OS."""
        return self.calcular_total_pecas() + self.calcular_total_servicos()

    def listar_itens(self):
        """Lista todos os itens da OS."""
        return self.itens.listar_todos()

    def __str__(self):
        fechamento_str = f"Fechada em: {self.data_hora_fechamento.strftime('%d/%m/%Y %H:%M')}" if self.fechada else "Aberta"
        return f"OS #{self.numero_os} | {self.placa} | {self.nome_cliente} | Mecânico: {self.mecanico} | {fechamento_str}"

    def __repr__(self):
        return self.__str__()


class GerenciadorOS:
    """Gerenciador de Ordens de Serviço."""
    def __init__(self):
        self.oss = Lista()
        self.proximo_numero = 1

    def abrir_os(self, placa, nome_cliente, mecanico):
        """Abre uma nova OS."""
        os = OS(self.proximo_numero, placa, nome_cliente, mecanico)
        self.oss.inserir_final(os)
        self.proximo_numero += 1
        return True, os

    def buscar_os(self, numero_os):
        """Busca uma OS pelo número."""
        return self.oss.buscar(numero_os, lambda o: o.numero_os)

    def adicionar_item_os(self, numero_os, codigo, descricao, valor, tipo):
        """Adiciona um item a uma OS."""
        os = self.buscar_os(numero_os)
        if os is None:
            return False, "OS não encontrada"
        return os.adicionar_item(codigo, descricao, valor, tipo)

    def remover_item_os(self, numero_os, codigo):
        """Remove um item de uma OS."""
        os = self.buscar_os(numero_os)
        if os is None:
            return False, "OS não encontrada"
        return os.remover_item(codigo)

    def concluir_remontagem_os(self, numero_os):
        """Conclui a remontagem de uma OS."""
        os = self.buscar_os(numero_os)
        if os is None:
            return False, "OS não encontrada"
        return os.concluir_remontagem()

    def fechar_os(self, numero_os):
        """Fecha uma OS."""
        os = self.buscar_os(numero_os)
        if os is None:
            return False, "OS não encontrada"
        return os.fechar()

    def listar_todas_os(self):
        """Lista todas as OS."""
        return self.oss.listar_todos()

    def listar_os_abertas(self):
        """Lista todas as OS abertas."""
        return [os for os in self.listar_todas_os() if not os.fechada]

    def listar_os_fechadas(self):
        """Lista todas as OS fechadas."""
        return [os for os in self.listar_todas_os() if os.fechada]

    def relatorio_os(self, numero_os):
        """Gera relatório detalhado de uma OS."""
        os = self.buscar_os(numero_os)
        if os is None:
            return "OS não encontrada"

        relatorio = []
        relatorio.append(f"=== ORDEM DE SERVIÇO #{os.numero_os} ===")
        relatorio.append(f"Placa: {os.placa}")
        relatorio.append(f"Cliente: {os.nome_cliente}")
        relatorio.append(f"Mecânico: {os.mecanico}")
        relatorio.append(f"Abertura: {os.data_hora_abertura.strftime('%d/%m/%Y %H:%M')}")
        if os.data_hora_fechamento:
            relatorio.append(f"Fechamento: {os.data_hora_fechamento.strftime('%d/%m/%Y %H:%M')}")
        relatorio.append(f"Remontagem concluída: {'Sim' if os.remontagem_concluida else 'Não'}")
        relatorio.append(f"Status: {'FECHADA' if os.fechada else 'ABERTA'}")
        relatorio.append("")
        relatorio.append("--- ITENS ---")
        itens = os.listar_itens()
        if itens:
            for item in itens:
                relatorio.append(f"  {item}")
        else:
            relatorio.append("  (Nenhum item)")
        relatorio.append("")
        relatorio.append("--- VALORES ---")
        relatorio.append(f"Total peças: R$ {os.calcular_total_pecas():.2f}")
        relatorio.append(f"Total serviços: R$ {os.calcular_total_servicos():.2f}")
        relatorio.append(f"TOTAL: R$ {os.calcular_total():.2f}")

        return "\n".join(relatorio)

    def relatorio_geral(self):
        """Gera relatório geral de todas as OS."""
        oss = self.listar_todas_os()
        if not oss:
            return "Nenhuma OS cadastrada."

        relatorio = ["=== RELATÓRIO GERAL DE OS ==="]
        relatorio.append(f"Total de OS: {len(oss)}")
        relatorio.append(f"OS abertas: {len(self.listar_os_abertas())}")
        relatorio.append(f"OS fechadas: {len(self.listar_os_fechadas())}")
        relatorio.append("")

        for os in oss:
            relatorio.append(f"{os}")
            relatorio.append(f"  Itens: {len(os.listar_itens())}")
            relatorio.append(f"  Total: R$ {os.calcular_total():.2f}")
            relatorio.append("")

        return "\n".join(relatorio)
