"""
Módulo de Controle de Pagamento.
Gerencia os pagamentos realizados no fechamento das OS.
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

    def listar_todos(self):
        elementos = []
        atual = self.cabeca
        while atual is not None:
            elementos.append(atual.dado)
            atual = atual.proximo
        return elementos


# ===== CLASSES DO DOMÍNIO =====
class Pagamento:
    """Representa um pagamento realizado."""
    def __init__(self, numero_os, nome_pagador, forma_pagamento, valor_pecas, valor_mao_obra, num_parcelas=1):
        self.numero_os = numero_os
        self.nome_pagador = nome_pagador
        self.forma_pagamento = forma_pagamento  # "PIX", "cartao", "dinheiro"
        self.valor_pecas = valor_pecas
        self.valor_mao_obra = valor_mao_obra
        self.valor_total = valor_pecas + valor_mao_obra
        self.num_parcelas = num_parcelas  # 1 para à vista, >1 para parcelado
        self.data_hora = datetime.now()

    def valor_parcela(self):
        """Calcula o valor de cada parcela (para cartão parcelado)."""
        if self.forma_pagamento == "cartao" and self.num_parcelas > 1:
            return self.valor_total / self.num_parcelas
        return self.valor_total

    def __str__(self):
        if self.forma_pagamento == "cartao" and self.num_parcelas > 1:
            forma_str = f"Cartão ({self.num_parcelas}x de R$ {self.valor_parcela():.2f})"
        elif self.forma_pagamento == "cartao":
            forma_str = "Cartão (à vista)"
        else:
            forma_str = self.forma_pagamento.upper()

        return f"OS #{self.numero_os} | {self.nome_pagador} | {forma_str} | Total: R$ {self.valor_total:.2f} | {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def __repr__(self):
        return self.__str__()


class GerenciadorPagamento:
    """Gerenciador de pagamentos."""
    def __init__(self):
        self.pagamentos = Lista()

    def registrar_pagamento(self, numero_os, nome_pagador, forma_pagamento, valor_pecas, valor_mao_obra, num_parcelas=1):
        """Registra um novo pagamento."""
        # Validações
        if forma_pagamento not in ["PIX", "cartao", "dinheiro"]:
            return False, "Forma de pagamento inválida"

        if forma_pagamento == "PIX" or forma_pagamento == "dinheiro":
            num_parcelas = 1  # Força à vista
        elif forma_pagamento == "cartao" and num_parcelas < 1:
            num_parcelas = 1

        pagamento = Pagamento(numero_os, nome_pagador, forma_pagamento, valor_pecas, valor_mao_obra, num_parcelas)
        self.pagamentos.inserir_final(pagamento)
        return True, "Pagamento registrado com sucesso"

    def buscar_pagamentos_por_os(self, numero_os):
        """Busca todos os pagamentos de uma OS."""
        pagamentos_encontrados = []
        for pagamento in self.pagamentos.listar_todos():
            if pagamento.numero_os == numero_os:
                pagamentos_encontrados.append(pagamento)
        return pagamentos_encontrados

    def listar_todos_pagamentos(self):
        """Lista todos os pagamentos."""
        return self.pagamentos.listar_todos()

    def calcular_total_recebido(self):
        """Calcula o total recebido em todos os pagamentos."""
        total = 0
        for pagamento in self.pagamentos.listar_todos():
            total += pagamento.valor_total
        return total

    def calcular_total_por_forma(self, forma):
        """Calcula o total recebido por forma de pagamento."""
        total = 0
        for pagamento in self.pagamentos.listar_todos():
            if pagamento.forma_pagamento == forma:
                total += pagamento.valor_total
        return total

    def relatorio_pagamento(self, numero_os):
        """Gera relatório de pagamentos de uma OS."""
        pagamentos = self.buscar_pagamentos_por_os(numero_os)
        if not pagamentos:
            return f"Nenhum pagamento encontrado para OS #{numero_os}"

        relatorio = [f"=== PAGAMENTOS DA OS #{numero_os} ==="]
        for pagamento in pagamentos:
            relatorio.append(f"  {pagamento}")
            relatorio.append(f"    Peças: R$ {pagamento.valor_pecas:.2f}")
            relatorio.append(f"    Mão de obra: R$ {pagamento.valor_mao_obra:.2f}")
            relatorio.append("")

        return "\n".join(relatorio)

    def relatorio_geral(self):
        """Gera relatório geral de pagamentos."""
        pagamentos = self.pagamentos.listar_todos()
        if not pagamentos:
            return "Nenhum pagamento registrado."

        relatorio = ["=== RELATÓRIO GERAL DE PAGAMENTOS ==="]
        relatorio.append(f"Total de pagamentos: {len(pagamentos)}")
        relatorio.append(f"Total recebido: R$ {self.calcular_total_recebido():.2f}")
        relatorio.append("")
        relatorio.append("--- POR FORMA DE PAGAMENTO ---")
        relatorio.append(f"PIX: R$ {self.calcular_total_por_forma('PIX'):.2f}")
        relatorio.append(f"Cartão: R$ {self.calcular_total_por_forma('cartao'):.2f}")
        relatorio.append(f"Dinheiro: R$ {self.calcular_total_por_forma('dinheiro'):.2f}")
        relatorio.append("")
        relatorio.append("--- TODOS OS PAGAMENTOS ---")

        for pagamento in pagamentos:
            relatorio.append(f"  {pagamento}")

        return "\n".join(relatorio)
