"""
Módulo de Árvore de Componentes para Diagnóstico.
Árvore genérica (não binária) para representar hierarquia de componentes do veículo.
"""


# ===== ESTRUTURA DE DADOS: ÁRVORE GENÉRICA =====
class NoArvore:
    """Nó da árvore genérica."""
    def __init__(self, dado):
        self.dado = dado
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def remover_filho(self, filho):
        if filho in self.filhos:
            self.filhos.remove(filho)

    def numero_filhos(self):
        return len(self.filhos)

    def __str__(self):
        return str(self.dado)


class Arvore:
    """Árvore genérica."""
    def __init__(self, raiz=None):
        self.raiz = raiz

    def vazia(self):
        return self.raiz is None

    def percurso_pre_ordem(self, no=None, resultado=None, nivel=0):
        """
        Percurso em profundidade (pré-ordem).
        Retorna lista de tuplas (dado, nivel) para exibição indentada.
        """
        if resultado is None:
            resultado = []
        if no is None:
            no = self.raiz

        if no is not None:
            resultado.append((no.dado, nivel))
            for filho in no.filhos:
                self.percurso_pre_ordem(filho, resultado, nivel + 1)

        return resultado

    def exibir_indentada(self):
        """Exibe a árvore de forma indentada."""
        if self.vazia():
            return "Árvore vazia"

        resultado = self.percurso_pre_ordem()
        linhas = []
        for dado, nivel in resultado:
            indent = "  " * nivel
            linhas.append(f"{indent}{dado}")
        return "\n".join(linhas)

    def buscar(self, chave, funcao_chave=None, no=None):
        """
        Busca um nó na árvore.
        chave: valor a buscar
        funcao_chave: função que extrai a chave do dado
        """
        if no is None:
            no = self.raiz

        if no is not None:
            if funcao_chave:
                if funcao_chave(no.dado) == chave:
                    return no
            else:
                if no.dado == chave:
                    return no

            for filho in no.filhos:
                resultado = self.buscar(chave, funcao_chave, filho)
                if resultado is not None:
                    return resultado

        return None

    def __str__(self):
        return self.exibir_indentada()


# ===== CLASSES DO DOMÍNIO =====
class Componente:
    """Representa um componente do veículo."""
    def __init__(self, nome, codigo_peca=None, estado="OK"):
        self.nome = nome
        self.codigo_peca = codigo_peca  # None se não for peça (sistema/subconjunto)
        self.estado = estado  # "OK" ou "Com defeito"

    def marcar_defeito(self):
        """Marca o componente como com defeito."""
        self.estado = "Com defeito"

    def marcar_ok(self):
        """Marca o componente como OK."""
        self.estado = "OK"

    def eh_peca(self):
        """Verifica se é uma peça (tem código)."""
        return self.codigo_peca is not None

    def __str__(self):
        estado_str = f"[{self.estado}]" if self.eh_peca() else ""
        codigo_str = f" ({self.codigo_peca})" if self.codigo_peca else ""
        return f"{self.nome}{codigo_str} {estado_str}".strip()

    def __repr__(self):
        return self.__str__()


class ArvoreComponentes:
    """
    Árvore de componentes pré-definida para diagnóstico.
    """
    def __init__(self):
        self.arvore = self._criar_arvore_pre_definida()

    def _criar_arvore_pre_definida(self):
        """Cria a árvore de componentes conforme o enunciado."""
        # Nós
        veiculo = NoArvore(Componente("Veículo"))

        motor = NoArvore(Componente("Motor"))
        ignicao = NoArvore(Componente("Sistema de ignição"))
        vela = NoArvore(Componente("Vela", "PEC-VELA"))
        bobina = NoArvore(Componente("Bobina", "PEC-BOB"))
        correia = NoArvore(Componente("Correia dentada", "PEC-COR"))

        freios = NoArvore(Componente("Freios"))
        pastilha = NoArvore(Componente("Pastilha dianteira", "PEC-PAS"))
        disco = NoArvore(Componente("Disco dianteiro", "PEC-DIS"))

        suspencao = NoArvore(Componente("Suspensão"))
        amortecedor = NoArvore(Componente("Amortecedor", "PEC-AMO"))
        bandeja = NoArvore(Componente("Bandeja", "PEC-BAN"))

        # Montar árvore
        veiculo.adicionar_filho(motor)
        veiculo.adicionar_filho(freios)
        veiculo.adicionar_filho(suspencao)

        motor.adicionar_filho(ignicao)
        motor.adicionar_filho(correia)

        ignicao.adicionar_filho(vela)
        ignicao.adicionar_filho(bobina)

        freios.adicionar_filho(pastilha)
        freios.adicionar_filho(disco)

        suspencao.adicionar_filho(amortecedor)
        suspencao.adicionar_filho(bandeja)

        return Arvore(veiculo)

    def exibir_arvore(self):
        """Exibe a árvore de componentes de forma indentada."""
        return self.arvore.exibir_indentada()

    def buscar_componente(self, nome):
        """Busca um componente pelo nome."""
        no = self.arvore.buscar(nome, lambda c: c.nome)
        return no.dado if no else None

    def marcar_defeito(self, nome_componente):
        """Marca um componente como com defeito."""
        componente = self.buscar_componente(nome_componente)
        if componente:
            componente.marcar_defeito()
            return True, f"Componente '{nome_componente}' marcado como com defeito"
        return False, f"Componente '{nome_componente}' não encontrado"

    def marcar_ok(self, nome_componente):
        """Marca um componente como OK."""
        componente = self.buscar_componente(nome_componente)
        if componente:
            componente.marcar_ok()
            return True, f"Componente '{nome_componente}' marcado como OK"
        return False, f"Componente '{nome_componente}' não encontrado"

    def listar_pecas_com_defeito(self):
        """Lista todas as peças marcadas com defeito."""
        pecas_defeito = []
        resultado = self.arvore.percurso_pre_ordem()
        for componente, nivel in resultado:
            if componente.eh_peca() and componente.estado == "Com defeito":
                pecas_defeito.append(componente)
        return pecas_defeito

    def relatorio_diagnostico(self):
        """Gera relatório de diagnóstico mostrando peças com defeito."""
        pecas_defeito = self.listar_pecas_com_defeito()
        if not pecas_defeito:
            return "Nenhuma peça com defeito identificada."

        relatorio = ["=== PEÇAS COM DEFEITO ==="]
        for peca in pecas_defeito:
            relatorio.append(f"- {peca.nome} ({peca.codigo_peca})")
        return "\n".join(relatorio)
