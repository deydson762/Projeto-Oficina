"""
Sistema de Oficina - Integração de todos os módulos.
Coordena o fluxo completo de atendimento.
"""

from .clientes import GerenciadorClientes
from .estoque import GerenciadorEstoque
from .atendimento import GerenciadorFila
from .componentes import ArvoreComponentes
from .ordem_servico import GerenciadorOS
from .pagamento import GerenciadorPagamento


class SistemaOficina:
    """
    Sistema integrado de oficina mecânica.
    Combina todos os gerenciadores em um único sistema.
    """
    def __init__(self):
        self.gerenciador_clientes = GerenciadorClientes()
        self.gerenciador_estoque = GerenciadorEstoque()
        self.gerenciador_fila = GerenciadorFila(num_boxes=3)
        self.arvore_componentes = ArvoreComponentes()
        self.gerenciador_os = GerenciadorOS()
        self.gerenciador_pagamento = GerenciadorPagamento()

    # ===== CLIENTES E VEÍCULOS =====
    def cadastrar_cliente(self, nome, cpf, telefone):
        return self.gerenciador_clientes.cadastrar_cliente(nome, cpf, telefone)

    def cadastrar_veiculo(self, cpf_cliente, placa, modelo, marca, ano):
        return self.gerenciador_clientes.cadastrar_veiculo(cpf_cliente, placa, modelo, marca, ano)

    def buscar_cliente(self, cpf):
        return self.gerenciador_clientes.buscar_cliente(cpf)

    def buscar_veiculo_por_placa(self, placa):
        return self.gerenciador_clientes.buscar_veiculo_por_placa(placa)

    # ===== ESTOQUE =====
    def cadastrar_produto(self, codigo, nome, fornecedor, preco_venda, estoque_minimo=10):
        return self.gerenciador_estoque.cadastrar_produto(codigo, nome, fornecedor, preco_venda, estoque_minimo)

    def adicionar_lote(self, codigo_produto, codigo_lote, data_compra, data_validade, quantidade, preco_compra):
        return self.gerenciador_estoque.adicionar_lote(codigo_produto, codigo_lote, data_compra, data_validade, quantidade, preco_compra)

    def baixar_estoque(self, codigo_produto, quantidade):
        return self.gerenciador_estoque.baixar_estoque(codigo_produto, quantidade)

    # ===== ATENDIMENTO =====
    def adicionar_veiculo_fila(self, placa, nome_cliente, queixa, eh_guincho=False):
        return self.gerenciador_fila.adicionar_veiculo(placa, nome_cliente, queixa, eh_guincho)

    def proximo_veiculo(self):
        return self.gerenciador_fila.proximo_veiculo()

    def box_liberado(self):
        return self.gerenciador_fila.box_liberado()

    # ===== COMPONENTES =====
    def exibir_arvore_componentes(self):
        return self.arvore_componentes.exibir_arvore()

    def marcar_defeito(self, nome_componente):
        return self.arvore_componentes.marcar_defeito(nome_componente)

    def listar_pecas_com_defeito(self):
        return self.arvore_componentes.listar_pecas_com_defeito()

    # ===== ORDEM DE SERVIÇO =====
    def abrir_os(self, placa, nome_cliente, mecanico):
        return self.gerenciador_os.abrir_os(placa, nome_cliente, mecanico)

    def adicionar_peca_os(self, numero_os, codigo, descricao, valor):
        return self.gerenciador_os.adicionar_item_os(numero_os, codigo, descricao, valor, "peca")

    def adicionar_servico_os(self, numero_os, codigo, descricao, valor):
        return self.gerenciador_os.adicionar_item_os(numero_os, codigo, descricao, valor, "servico")

    def concluir_remontagem_os(self, numero_os):
        return self.gerenciador_os.concluir_remontagem_os(numero_os)

    def fechar_os(self, numero_os):
        return self.gerenciador_os.fechar_os(numero_os)

    def buscar_os(self, numero_os):
        return self.gerenciador_os.buscar_os(numero_os)

    # ===== PAGAMENTO =====
    def registrar_pagamento(self, numero_os, nome_pagador, forma_pagamento, valor_pecas, valor_mao_obra, num_parcelas=1):
        return self.gerenciador_pagamento.registrar_pagamento(numero_os, nome_pagador, forma_pagamento, valor_pecas, valor_mao_obra, num_parcelas)

    # ===== FLUXO COMPLETO DE ATENDIMENTO =====
    def atendimento_completo(self, placa, nome_cliente, queixa, mecanico, forma_pagamento, nome_pagador, num_parcelas=1, eh_guincho=False):
        """
        Simula um atendimento completo do início ao fim.
        Retorna (sucesso, mensagem) com detalhes do processo.
        """
        log = []

        # 1. Adicionar veículo à fila
        log.append("=== INÍCIO DO ATENDIMENTO ===")
        sucesso, msg = self.adicionar_veiculo_fila(placa, nome_cliente, queixa, eh_guincho)
        log.append(f"1. Veículo na fila: {msg}")

        # 2. Chamar próximo veículo (simular box livre)
        sucesso, proximo = self.box_liberado()
        if proximo:
            log.append(f"2. Veículo chamado para atendimento: {proximo.placa}")
        else:
            log.append("2. Nenhum veículo disponível")
            return False, "\n".join(log)

        # 3. Abrir OS
        sucesso, os = self.abrir_os(placa, nome_cliente, mecanico)
        log.append(f"3. OS aberta: #{os.numero_os}")

        # 4. Diagnóstico (simular: marca 2 peças com defeito)
        log.append("4. Diagnóstico realizado:")
        pecas_defeito = ["Vela", "Pastilha dianteira"]
        for peca in pecas_defeito:
            sucesso, msg = self.marcar_defeito(peca)
            log.append(f"   - {msg}")

        # 5. Adicionar peças e serviços à OS (simular)
        log.append("5. Itens adicionados à OS:")
        # Supondo que as peças estão no estoque
        self.adicionar_peca_os(os.numero_os, "PEC-VELA", "Vela de Ignição", 80.00)
        log.append("   - Peça: Vela de Ignição (R$ 80.00)")
        self.adicionar_servico_os(os.numero_os, "SER-TRO", "Troca de Vela", 150.00)
        log.append("   - Serviço: Troca de Vela (R$ 150.00)")

        self.adicionar_peca_os(os.numero_os, "PEC-PAS", "Pastilha de Freio", 150.00)
        log.append("   - Peça: Pastilha de Freio (R$ 150.00)")
        self.adicionar_servico_os(os.numero_os, "SER-FRE", "Troca de Pastilhas", 200.00)
        log.append("   - Serviço: Troca de Pastilhas (R$ 200.00)")

        # 6. Baixar estoque (simular)
        log.append("6. Baixa de estoque:")
        # Supondo que os produtos existem no estoque
        sucesso, msg = self.baixar_estoque("PEC-VELA", 1)
        log.append(f"   - Vela: {msg}")
        sucesso, msg = self.baixar_estoque("PEC-PAS", 1)
        log.append(f"   - Pastilha: {msg}")

        # 7. Concluir remontagem
        sucesso, msg = self.concluir_remontagem_os(os.numero_os)
        log.append(f"7. {msg}")

        # 8. Fechar OS
        sucesso, msg = self.fechar_os(os.numero_os)
        log.append(f"8. {msg}")

        # 9. Calcular totais
        valor_pecas = os.calcular_total_pecas()
        valor_mao_obra = os.calcular_total_servicos()
        log.append(f"9. Totais: Peças R$ {valor_pecas:.2f} | Mão de obra R$ {valor_mao_obra:.2f} | Total R$ {os.calcular_total():.2f}")

        # 10. Processar pagamento
        sucesso, msg = self.registrar_pagamento(os.numero_os, nome_pagador, forma_pagamento, valor_pecas, valor_mao_obra, num_parcelas)
        log.append(f"10. Pagamento: {msg}")

        log.append("=== ATENDIMENTO CONCLUÍDO ===")

        return True, "\n".join(log)

    # ===== RELATÓRIOS =====
    def relatorio_geral(self):
        """Gera relatório geral do sistema."""
        relatorio = []
        relatorio.append("=== RELATÓRIO GERAL DO SISTEMA ===")
        relatorio.append("")

        # Clientes
        relatorio.append("--- CLIENTES ---")
        clientes = self.gerenciador_clientes.listar_todos_clientes()
        relatorio.append(f"Total de clientes: {len(clientes)}")
        relatorio.append("")

        # Estoque
        relatorio.append("--- ESTOQUE ---")
        alertas = self.gerenciador_estoque.verificar_alertas()
        relatorio.append(f"Produtos com estoque baixo: {len(alertas)}")
        relatorio.append("")

        # Fila
        relatorio.append("--- FILA DE ESPERA ---")
        relatorio.append(f"Veículos aguardando: {self.gerenciador_fila.tamanho_total()}")
        relatorio.append("")

        # OS
        relatorio.append("--- ORDENS DE SERVIÇO ---")
        os_abertas = self.gerenciador_os.listar_os_abertas()
        os_fechadas = self.gerenciador_os.listar_os_fechadas()
        relatorio.append(f"OS abertas: {len(os_abertas)}")
        relatorio.append(f"OS fechadas: {len(os_fechadas)}")
        relatorio.append("")

        # Pagamentos
        relatorio.append("--- PAGAMENTOS ---")
        pagamentos = self.gerenciador_pagamento.listar_todos_pagamentos()
        relatorio.append(f"Total de pagamentos: {len(pagamentos)}")
        relatorio.append(f"Total recebido: R$ {self.gerenciador_pagamento.calcular_total_recebido():.2f}")
        relatorio.append("")

        return "\n".join(relatorio)
