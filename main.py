"""
Menu Interativo do Sistema de Oficina Mecânica.
"""

from datetime import datetime
from oficina import SistemaOficina


def limpar_tela():
    """Limpa a tela (funciona em Windows e Linux/Mac)."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa para o usuário ver a mensagem."""
    input("\nPressione Enter para continuar...")


def menu_clientes(sistema):
    """Menu de clientes e veículos."""
    while True:
        limpar_tela()
        print("=" * 60)
        print("MENU DE CLIENTES E VEÍCULOS")
        print("=" * 60)
        print("1. Cadastrar cliente")
        print("2. Cadastrar veículo")
        print("3. Buscar cliente por CPF")
        print("4. Buscar veículo por placa")
        print("5. Relatório de clientes")
        print("0. Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            telefone = input("Telefone: ")
            sucesso, msg = sistema.cadastrar_cliente(nome, cpf, telefone)
            print(f"\n{msg}")
            pausar()

        elif opcao == "2":
            cpf = input("CPF do cliente: ")
            placa = input("Placa do veículo: ")
            modelo = input("Modelo: ")
            marca = input("Marca: ")
            ano = int(input("Ano: "))
            sucesso, msg = sistema.cadastrar_veiculo(cpf, placa, modelo, marca, ano)
            print(f"\n{msg}")
            pausar()

        elif opcao == "3":
            cpf = input("CPF: ")
            cliente = sistema.buscar_cliente(cpf)
            if cliente:
                print(f"\nCliente encontrado: {cliente}")
                print(f"Veículos: {len(cliente.listar_veiculos())}")
                for v in cliente.listar_veiculos():
                    print(f"  - {v}")
            else:
                print("\nCliente não encontrado")
            pausar()

        elif opcao == "4":
            placa = input("Placa: ")
            veiculo, cliente = sistema.buscar_veiculo_por_placa(placa)
            if veiculo:
                print(f"\nVeículo: {veiculo}")
                print(f"Cliente: {cliente}")
            else:
                print("\nVeículo não encontrado")
            pausar()

        elif opcao == "5":
            print("\n" + sistema.gerenciador_clientes.relatorio_completo())
            pausar()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida!")
            pausar()


def menu_estoque(sistema):
    """Menu de estoque."""
    while True:
        limpar_tela()
        print("=" * 60)
        print("MENU DE ESTOQUE")
        print("=" * 60)
        print("1. Cadastrar produto")
        print("2. Adicionar lote")
        print("3. Baixar estoque")
        print("4. Verificar alertas")
        print("5. Relatório de estoque")
        print("0. Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            codigo = input("Código: ")
            nome = input("Nome: ")
            fornecedor = input("Fornecedor: ")
            preco_venda = float(input("Preço de venda: "))
            estoque_minimo = int(input("Estoque mínimo: "))
            sucesso, msg = sistema.cadastrar_produto(codigo, nome, fornecedor, preco_venda, estoque_minimo)
            print(f"\n{msg}")
            pausar()

        elif opcao == "2":
            codigo = input("Código do produto: ")
            codigo_lote = input("Código do lote: ")
            quantidade = int(input("Quantidade: "))
            preco_compra = float(input("Preço de compra: "))
            print("Data de compra (deixe vazio para hoje):")
            data_compra_str = input("Data (DD/MM/AAAA): ")
            if data_compra_str:
                data_compra = datetime.strptime(data_compra_str, "%d/%m/%Y")
            else:
                data_compra = datetime.now()
            print("Data de validade (deixe vazio se não tiver):")
            data_validade_str = input("Data (DD/MM/AAAA): ")
            data_validade = datetime.strptime(data_validade_str, "%d/%m/%Y") if data_validade_str else None
            sucesso, msg = sistema.adicionar_lote(codigo, codigo_lote, data_compra, data_validade, quantidade, preco_compra)
            print(f"\n{msg}")
            pausar()

        elif opcao == "3":
            codigo = input("Código do produto: ")
            quantidade = int(input("Quantidade a baixar: "))
            sucesso, msg = sistema.baixar_estoque(codigo, quantidade)
            print(f"\n{msg}")
            pausar()

        elif opcao == "4":
            alertas = sistema.gerenciador_estoque.verificar_alertas()
            if alertas:
                print("\nProdutos com estoque baixo:")
                for produto in alertas:
                    print(f"  - {produto.nome}: {produto.quantidade_total()} (mínimo: {produto.estoque_minimo})")
            else:
                print("\nNenhum produto com estoque baixo")
            pausar()

        elif opcao == "5":
            print("\n" + sistema.gerenciador_estoque.relatorio_estoque())
            pausar()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida!")
            pausar()


def menu_atendimento(sistema):
    """Menu de atendimento."""
    while True:
        limpar_tela()
        print("=" * 60)
        print("MENU DE ATENDIMENTO")
        print("=" * 60)
        print("1. Adicionar veículo à fila")
        print("2. Chamar próximo veículo")
        print("3. Relatório da fila")
        print("0. Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            placa = input("Placa: ")
            nome_cliente = input("Nome do cliente: ")
            queixa = input("Queixa: ")
            eh_guincho = input("É guincho? (s/n): ").lower() == 's'
            sucesso, msg = sistema.adicionar_veiculo_fila(placa, nome_cliente, queixa, eh_guincho)
            print(f"\n{msg}")
            pausar()

        elif opcao == "2":
            sucesso, proximo = sistema.box_liberado()
            if proximo:
                print(f"\nPróximo veículo: {proximo.placa} - {proximo.nome_cliente}")
                print(f"Queixa: {proximo.queixa}")
            else:
                print("\nNenhum veículo aguardando")
            pausar()

        elif opcao == "3":
            print("\n" + sistema.gerenciador_fila.relatorio_fila())
            pausar()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida!")
            pausar()


def menu_componentes(sistema):
    """Menu de componentes."""
    while True:
        limpar_tela()
        print("=" * 60)
        print("MENU DE COMPONENTES")
        print("=" * 60)
        print("1. Exibir árvore de componentes")
        print("2. Marcar componente com defeito")
        print("3. Marcar componente como OK")
        print("4. Relatório de diagnóstico")
        print("0. Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n" + sistema.exibir_arvore_componentes())
            pausar()

        elif opcao == "2":
            nome = input("Nome do componente: ")
            sucesso, msg = sistema.marcar_defeito(nome)
            print(f"\n{msg}")
            pausar()

        elif opcao == "3":
            nome = input("Nome do componente: ")
            sucesso, msg = sistema.arvore_componentes.marcar_ok(nome)
            print(f"\n{msg}")
            pausar()

        elif opcao == "4":
            print("\n" + sistema.arvore_componentes.relatorio_diagnostico())
            pausar()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida!")
            pausar()


def menu_os(sistema):
    """Menu de ordem de serviço."""
    while True:
        limpar_tela()
        print("=" * 60)
        print("MENU DE ORDEM DE SERVIÇO")
        print("=" * 60)
        print("1. Abrir OS")
        print("2. Adicionar peça à OS")
        print("3. Adicionar serviço à OS")
        print("4. Concluir remontagem")
        print("5. Fechar OS")
        print("6. Relatório de OS")
        print("7. Relatório geral de OS")
        print("0. Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            placa = input("Placa: ")
            nome_cliente = input("Nome do cliente: ")
            mecanico = input("Mecânico: ")
            sucesso, os = sistema.abrir_os(placa, nome_cliente, mecanico)
            print(f"\nOS aberta: #{os.numero_os}")
            pausar()

        elif opcao == "2":
            numero_os = int(input("Número da OS: "))
            codigo = input("Código da peça: ")
            descricao = input("Descrição: ")
            valor = float(input("Valor: "))
            sucesso, msg = sistema.adicionar_peca_os(numero_os, codigo, descricao, valor)
            print(f"\n{msg}")
            pausar()

        elif opcao == "3":
            numero_os = int(input("Número da OS: "))
            codigo = input("Código do serviço: ")
            descricao = input("Descrição: ")
            valor = float(input("Valor: "))
            sucesso, msg = sistema.adicionar_servico_os(numero_os, codigo, descricao, valor)
            print(f"\n{msg}")
            pausar()

        elif opcao == "4":
            numero_os = int(input("Número da OS: "))
            sucesso, msg = sistema.concluir_remontagem_os(numero_os)
            print(f"\n{msg}")
            pausar()

        elif opcao == "5":
            numero_os = int(input("Número da OS: "))
            sucesso, msg = sistema.fechar_os(numero_os)
            print(f"\n{msg}")
            pausar()

        elif opcao == "6":
            numero_os = int(input("Número da OS: "))
            print("\n" + sistema.gerenciador_os.relatorio_os(numero_os))
            pausar()

        elif opcao == "7":
            print("\n" + sistema.gerenciador_os.relatorio_geral())
            pausar()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida!")
            pausar()


def menu_pagamento(sistema):
    """Menu de pagamento."""
    while True:
        limpar_tela()
        print("=" * 60)
        print("MENU DE PAGAMENTO")
        print("=" * 60)
        print("1. Registrar pagamento")
        print("2. Relatório de pagamento por OS")
        print("3. Relatório geral de pagamentos")
        print("0. Voltar")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            numero_os = int(input("Número da OS: "))
            nome_pagador = input("Nome de quem pagou: ")
            print("Formas: PIX, cartao, dinheiro")
            forma = input("Forma de pagamento: ")
            valor_pecas = float(input("Valor das peças: "))
            valor_mao_obra = float(input("Valor da mão de obra: "))
            if forma == "cartao":
                num_parcelas = int(input("Número de parcelas: "))
            else:
                num_parcelas = 1
            sucesso, msg = sistema.registrar_pagamento(numero_os, nome_pagador, forma, valor_pecas, valor_mao_obra, num_parcelas)
            print(f"\n{msg}")
            pausar()

        elif opcao == "2":
            numero_os = int(input("Número da OS: "))
            print("\n" + sistema.gerenciador_pagamento.relatorio_pagamento(numero_os))
            pausar()

        elif opcao == "3":
            print("\n" + sistema.gerenciador_pagamento.relatorio_geral())
            pausar()

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida!")
            pausar()


def menu_principal():
    """Menu principal do sistema."""
    sistema = SistemaOficina()

    while True:
        limpar_tela()
        print("=" * 60)
        print("SISTEMA DE OFICINA MECÂNICA")
        print("=" * 60)
        print("1. Clientes e Veículos")
        print("2. Estoque")
        print("3. Atendimento")
        print("4. Componentes (Diagnóstico)")
        print("5. Ordem de Serviço")
        print("6. Pagamento")
        print("7. Relatório Geral do Sistema")
        print("8. Simular Atendimento Completo")
        print("0. Sair")
        print()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_clientes(sistema)
        elif opcao == "2":
            menu_estoque(sistema)
        elif opcao == "3":
            menu_atendimento(sistema)
        elif opcao == "4":
            menu_componentes(sistema)
        elif opcao == "5":
            menu_os(sistema)
        elif opcao == "6":
            menu_pagamento(sistema)
        elif opcao == "7":
            print("\n" + sistema.relatorio_geral())
            pausar()
        elif opcao == "8":
            print("\n=== SIMULAÇÃO DE ATENDIMENTO COMPLETO ===")
            placa = input("Placa: ")
            nome_cliente = input("Nome do cliente: ")
            queixa = input("Queixa: ")
            mecanico = input("Mecânico: ")
            print("Formas: PIX, cartao, dinheiro")
            forma_pagamento = input("Forma de pagamento: ")
            nome_pagador = input("Nome de quem pagou: ")
            if forma_pagamento == "cartao":
                num_parcelas = int(input("Número de parcelas: "))
            else:
                num_parcelas = 1
            eh_guincho = input("É guincho? (s/n): ").lower() == 's'

            sucesso, log = sistema.atendimento_completo(
                placa, nome_cliente, queixa, mecanico,
                forma_pagamento, nome_pagador, num_parcelas, eh_guincho
            )
            print("\n" + log)
            pausar()
        elif opcao == "0":
            print("\nSaindo do sistema...")
            break
        else:
            print("\nOpção inválida!")
            pausar()


if __name__ == "__main__":
    menu_principal()
