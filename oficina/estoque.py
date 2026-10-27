"""
Módulo de Controle de Estoque de Peças.
Combinação de estruturas: Lista de produtos, cada um contendo uma Fila de lotes.
"""

from datetime import datetime, date


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
class Lote:
    """Representa um lote de produto comprado."""
    def __init__(self, codigo_lote, data_compra, data_validade, quantidade, preco_compra):
        self.codigo_lote = codigo_lote
        self.data_compra = data_compra  # datetime
        self.data_validade = data_validade  # datetime ou None (sem validade)
        self.quantidade = quantidade
        self.preco_compra = preco_compra

    def esta_vencido(self):
        """Verifica se o lote está vencido."""
        if self.data_validade is None:
            return False
        return datetime.now() > self.data_validade

    def __str__(self):
        validade_str = self.data_validade.strftime("%d/%m/%Y") if self.data_validade else "Sem validade"
        return f"Lote {self.codigo_lote} | Qtd: {self.quantidade} | Compra: {self.data_compra.strftime('%d/%m/%Y')} | Validade: {validade_str} | R$ {self.preco_compra:.2f}"

    def __repr__(self):
        return self.__str__()


class Produto:
    """Representa um produto do estoque."""
    def __init__(self, codigo, nome, fornecedor, preco_venda, estoque_minimo=10):
        self.codigo = codigo
        self.nome = nome
        self.fornecedor = fornecedor
        self.preco_venda = preco_venda
        self.estoque_minimo = estoque_minimo
        self.lotes = Fila()  # Fila de lotes (FIFO)

    def adicionar_lote(self, lote):
        """Adiciona um lote ao produto."""
        self.lotes.enfileirar(lote)

    def quantidade_total(self):
        """Calcula a quantidade total em estoque (soma de todos os lotes)."""
        total = 0
        for lote in self.lotes.listar_todos():
            total += lote.quantidade
        return total

    def abaixo_minimo(self):
        """Verifica se o estoque está abaixo do mínimo."""
        return self.quantidade_total() < self.estoque_minimo

    def remover_lotes_vencidos(self):
        """Remove e retorna lotes vencidos (perda)."""
        lotes_vencidos = []
        while not self.lotes.vazia():
            lote = self.lotes.frente_fila()
            if lote.esta_vencido():
                lotes_vencidos.append(self.lotes.desenfileirar())
            else:
                break
        return lotes_vencidos

    def baixar_estoque(self, quantidade):
        """
        Baixa quantidade do estoque, consumindo do lote mais antigo (FIFO).
        Retorna (True, mensagem) ou (False, mensagem).
        """
        if self.quantidade_total() < quantidade:
            return False, f"Estoque insuficiente. Disponível: {self.quantidade_total()}, Solicitado: {quantidade}"

        # Primeiro remove lotes vencidos
        self.remover_lotes_vencidos()

        # Consome do lote mais antigo
        restante = quantidade
        while restante > 0 and not self.lotes.vazia():
            lote = self.lotes.frente_fila()
            if lote.quantidade >= restante:
                lote.quantidade -= restante
                restante = 0
                if lote.quantidade == 0:
                    self.lotes.desenfileirar()
            else:
                restante -= lote.quantidade
                self.lotes.desenfileirar()

        return True, f"Baixa de {quantidade} unidades realizada com sucesso"

    def ajustar_inventario(self, nova_quantidade):
        """Ajusta a quantidade em estoque para um valor específico."""
        # Remove todos os lotes
        while not self.lotes.vazia():
            self.lotes.desenfileirar()

        # Cria um lote único com a nova quantidade
        lote = Lote(
            codigo_lote=f"AJUSTE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            data_compra=datetime.now(),
            data_validade=None,
            quantidade=nova_quantidade,
            preco_compra=0.0
        )
        self.adicionar_lote(lote)
        return True, "Inventário ajustado com sucesso"

    def __str__(self):
        return f"{self.nome} ({self.codigo}) | Fornecedor: {self.fornecedor} | Venda: R$ {self.preco_venda:.2f} | Estoque: {self.quantidade_total()}"

    def __repr__(self):
        return self.__str__()


class GerenciadorEstoque:
    """
    Gerenciador de estoque.
    Combinação: Lista de produtos, cada um contendo uma Fila de lotes.
    """
    def __init__(self):
        self.produtos = Lista()
        self.perdas = []  # Registro de perdas (lotes vencidos)

    def cadastrar_produto(self, codigo, nome, fornecedor, preco_venda, estoque_minimo=10):
        """Cadastra um novo produto."""
        if self.buscar_produto(codigo) is not None:
            return False, "Produto já cadastrado com este código"
        produto = Produto(codigo, nome, fornecedor, preco_venda, estoque_minimo)
        self.produtos.inserir_final(produto)
        return True, "Produto cadastrado com sucesso"

    def adicionar_lote(self, codigo_produto, codigo_lote, data_compra, data_validade, quantidade, preco_compra):
        """Adiciona um lote a um produto existente."""
        produto = self.buscar_produto(codigo_produto)
        if produto is None:
            return False, "Produto não encontrado"
        lote = Lote(codigo_lote, data_compra, data_validade, quantidade, preco_compra)
        produto.adicionar_lote(lote)
        return True, "Lote adicionado com sucesso"

    def buscar_produto(self, codigo):
        """Busca um produto pelo código."""
        return self.produtos.buscar(codigo, lambda p: p.codigo)

    def baixar_estoque(self, codigo_produto, quantidade):
        """Baixa quantidade do estoque de um produto."""
        produto = self.buscar_produto(codigo_produto)
        if produto is None:
            return False, "Produto não encontrado"
        return produto.baixar_estoque(quantidade)

    def ajustar_inventario(self, codigo_produto, nova_quantidade):
        """Ajusta o inventário de um produto."""
        produto = self.buscar_produto(codigo_produto)
        if produto is None:
            return False, "Produto não encontrado"
        return produto.ajustar_inventario(nova_quantidade)

    def verificar_alertas(self):
        """Retorna lista de produtos com estoque abaixo do mínimo."""
        alertas = []
        for produto in self.produtos.listar_todos():
            if produto.abaixo_minimo():
                alertas.append(produto)
        return alertas

    def limpar_lotes_vencidos(self):
        """Remove lotes vencidos de todos os produtos e registra perdas."""
        perdas_totais = []
        for produto in self.produtos.listar_todos():
            lotes_vencidos = produto.remover_lotes_vencidos()
            for lote in lotes_vencidos:
                perdas_totais.append({
                    'produto': produto.nome,
                    'lote': lote.codigo_lote,
                    'quantidade': lote.quantidade,
                    'valor': lote.quantidade * lote.preco_compra
                })
        self.perdas.extend(perdas_totais)
        return perdas_totais

    def relatorio_estoque(self):
        """Gera relatório completo do estoque."""
        produtos = self.produtos.listar_todos()
        if not produtos:
            return "Nenhum produto cadastrado."

        relatorio = []
        for produto in produtos:
            relatorio.append(f"Produto: {produto}")
            lotes = produto.lotes.listar_todos()
            if lotes:
                for lote in lotes:
                    relatorio.append(f"  - {lote}")
            else:
                relatorio.append("  (Nenhum lote)")
            if produto.abaixo_minimo():
                relatorio.append("  [ALERTA: Estoque abaixo do mínimo!]")
            relatorio.append("")
        return "\n".join(relatorio)

    def relatorio_perdas(self):
        """Gera relatório de perdas (lotes vencidos)."""
        if not self.perdas:
            return "Nenhuma perda registrada."

        relatorio = ["=== RELATÓRIO DE PERDAS ==="]
        for perda in self.perdas:
            relatorio.append(f"Produto: {perda['produto']}")
            relatorio.append(f"  Lote: {perda['lote']}")
            relatorio.append(f"  Quantidade: {perda['quantidade']}")
            relatorio.append(f"  Valor perdido: R$ {perda['valor']:.2f}")
            relatorio.append("")
        return "\n".join(relatorio)
