"""
Módulo de Controle de Clientes e Veículos.
Combinação de estruturas: Lista de clientes, cada um contendo uma Lista de veículos.
"""


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
class Veiculo:
    """Representa um veículo de um cliente."""
    def __init__(self, placa, modelo, marca, ano):
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.ano = ano

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - Placa: {self.placa}"

    def __repr__(self):
        return self.__str__()


class Cliente:
    """Representa um cliente da oficina."""
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.veiculos = Lista()  # Lista de veículos do cliente

    def adicionar_veiculo(self, veiculo):
        """Adiciona um veículo ao cliente."""
        self.veiculos.inserir_final(veiculo)

    def remover_veiculo(self, placa):
        """Remove um veículo pela placa."""
        return self.veiculos.remover_por_chave(placa, lambda v: v.placa)

    def buscar_veiculo(self, placa):
        """Busca um veículo pela placa."""
        return self.veiculos.buscar(placa, lambda v: v.placa)

    def listar_veiculos(self):
        """Retorna lista de todos os veículos do cliente."""
        return self.veiculos.listar_todos()

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf}, Tel: {self.telefone})"

    def __repr__(self):
        return self.__str__()


class GerenciadorClientes:
    """
    Gerenciador de clientes e veículos.
    Combinação: Lista de clientes, cada um contendo uma Lista de veículos.
    """
    def __init__(self):
        self.clientes = Lista()

    def cadastrar_cliente(self, nome, cpf, telefone):
        """Cadastra um novo cliente."""
        if self.buscar_cliente(cpf) is not None:
            return False, "Cliente já cadastrado com este CPF"
        cliente = Cliente(nome, cpf, telefone)
        self.clientes.inserir_final(cliente)
        return True, "Cliente cadastrado com sucesso"

    def cadastrar_veiculo(self, cpf_cliente, placa, modelo, marca, ano):
        """Cadastra um veículo para um cliente existente."""
        cliente = self.buscar_cliente(cpf_cliente)
        if cliente is None:
            return False, "Cliente não encontrado"
        if cliente.buscar_veiculo(placa) is not None:
            return False, "Veículo já cadastrado com esta placa"
        veiculo = Veiculo(placa, modelo, marca, ano)
        cliente.adicionar_veiculo(veiculo)
        return True, "Veículo cadastrado com sucesso"

    def buscar_cliente(self, cpf):
        """Busca um cliente pelo CPF."""
        return self.clientes.buscar(cpf, lambda c: c.cpf)

    def buscar_veiculo_por_placa(self, placa):
        """
        Busca um veículo pela placa.
        Percorre a lista de clientes e, para cada cliente, percorre sua lista de veículos.
        """
        clientes = self.clientes.listar_todos()
        for cliente in clientes:
            veiculo = cliente.buscar_veiculo(placa)
            if veiculo is not None:
                return veiculo, cliente
        return None, None

    def remover_cliente(self, cpf):
        """Remove um cliente pelo CPF."""
        if self.clientes.remover_por_chave(cpf, lambda c: c.cpf):
            return True, "Cliente removido com sucesso"
        return False, "Cliente não encontrado"

    def remover_veiculo(self, placa):
        """Remove um veículo pela placa."""
        clientes = self.clientes.listar_todos()
        for cliente in clientes:
            if cliente.remover_veiculo(placa):
                return True, "Veículo removido com sucesso"
        return False, "Veículo não encontrado"

    def listar_todos_clientes(self):
        """Retorna todos os clientes."""
        return self.clientes.listar_todos()

    def relatorio_completo(self):
        """Gera relatório completo de clientes e veículos."""
        clientes = self.listar_todos_clientes()
        if not clientes:
            return "Nenhum cliente cadastrado."

        relatorio = []
        for cliente in clientes:
            relatorio.append(f"Cliente: {cliente}")
            veiculos = cliente.listar_veiculos()
            if veiculos:
                for veiculo in veiculos:
                    relatorio.append(f"  - {veiculo}")
            else:
                relatorio.append("  (Nenhum veículo cadastrado)")
            relatorio.append("")
        return "\n".join(relatorio)
