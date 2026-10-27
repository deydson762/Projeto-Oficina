"""
Teste do módulo de ordem de serviço.
"""

from oficina.ordem_servico import GerenciadorOS


def testar_os():
    print("=== TESTE ORDEM DE SERVIÇO ===\n")

    gerenciador = GerenciadorOS()

    # Abrir OS
    print("1. Abrir ordens de serviço:")
    resultado, os1 = gerenciador.abrir_os("ABC-1234", "João Silva", "Mecânico Carlos")
    print(f"   {os1}")
    resultado, os2 = gerenciador.abrir_os("XYZ-5678", "Maria Santos", "Mecânico Ana")
    print(f"   {os2}")
    print()

    # Adicionar itens
    print("2. Adicionar itens às OS:")
    resultado, msg = gerenciador.adicionar_item_os(1, "PEC-PAS", "Pastilha de Freio", 150.00, "peca")
    print(f"   OS #1: {msg}")
    resultado, msg = gerenciador.adicionar_item_os(1, "SER-TRO", "Troca de Pastilhas", 200.00, "servico")
    print(f"   OS #1: {msg}")
    resultado, msg = gerenciador.adicionar_item_os(2, "PEC-VELA", "Vela de Ignição", 80.00, "peca")
    print(f"   OS #2: {msg}")
    resultado, msg = gerenciador.adicionar_item_os(2, "SER-ALI", "Alinhamento", 150.00, "servico")
    print(f"   OS #2: {msg}")
    print()

    # Relatório OS
    print("3. Relatório da OS #1:")
    print(gerenciador.relatorio_os(1))
    print()

    # Remover item
    print("4. Remover item da OS #1:")
    resultado, msg = gerenciador.remover_item_os(1, "SER-TRO")
    print(f"   {msg}")
    print(gerenciador.relatorio_os(1))
    print()

    # Tentar fechar sem concluir remontagem
    print("5. Tentar fechar OS sem concluir remontagem:")
    resultado, msg = gerenciador.fechar_os(1)
    print(f"   {msg}")
    print()

    # Concluir remontagem
    print("6. Concluir remontagem da OS #1:")
    resultado, msg = gerenciador.concluir_remontagem_os(1)
    print(f"   {msg}")
    print()

    # Fechar OS
    print("7. Fechar OS #1:")
    resultado, msg = gerenciador.fechar_os(1)
    print(f"   {msg}")
    print(gerenciador.relatorio_os(1))
    print()

    # Tentar adicionar item em OS fechada
    print("8. Tentar adicionar item em OS fechada:")
    resultado, msg = gerenciador.adicionar_item_os(1, "PEC-OLEO", "Óleo", 50.00, "peca")
    print(f"   {msg}")
    print()

    # Relatório geral
    print("9. Relatório geral:")
    print(gerenciador.relatorio_geral())


if __name__ == "__main__":
    testar_os()
    print("\n[OK] Teste concluído!")
