"""
Teste do módulo de pagamento.
"""

from oficina.pagamento import GerenciadorPagamento


def testar_pagamento():
    print("=== TESTE CONTROLE DE PAGAMENTO ===\n")

    gerenciador = GerenciadorPagamento()

    # Registrar pagamentos
    print("1. Registrar pagamentos:")
    resultado, msg = gerenciador.registrar_pagamento(1, "João Silva", "PIX", 150.00, 200.00)
    print(f"   OS #1 - PIX: {msg}")
    resultado, msg = gerenciador.registrar_pagamento(2, "Maria Santos", "cartao", 80.00, 150.00, 3)
    print(f"   OS #2 - Cartão 3x: {msg}")
    resultado, msg = gerenciador.registrar_pagamento(3, "Pedro Costa", "dinheiro", 200.00, 100.00)
    print(f"   OS #3 - Dinheiro: {msg}")
    resultado, msg = gerenciador.registrar_pagamento(4, "Ana Lima", "cartao", 50.00, 100.00, 1)
    print(f"   OS #4 - Cartão à vista: {msg}")
    print()

    # Relatório por OS
    print("2. Relatório de pagamento da OS #2:")
    print(gerenciador.relatorio_pagamento(2))
    print()

    # Buscar pagamentos por OS
    print("3. Buscar pagamentos por OS:")
    pagamentos = gerenciador.buscar_pagamentos_por_os(1)
    print(f"   OS #1: {len(pagamentos)} pagamento(s)")
    pagamentos = gerenciador.buscar_pagamentos_por_os(99)
    print(f"   OS #99: {len(pagamentos)} pagamento(s)\n")

    # Calcular totais
    print("4. Calcular totais:")
    print(f"   Total recebido: R$ {gerenciador.calcular_total_recebido():.2f}")
    print(f"   Total PIX: R$ {gerenciador.calcular_total_por_forma('PIX'):.2f}")
    print(f"   Total Cartão: R$ {gerenciador.calcular_total_por_forma('cartao'):.2f}")
    print(f"   Total Dinheiro: R$ {gerenciador.calcular_total_por_forma('dinheiro'):.2f}")
    print()

    # Relatório geral
    print("5. Relatório geral:")
    print(gerenciador.relatorio_geral())

    # Testar forma inválida
    print("\n6. Testar forma de pagamento inválida:")
    resultado, msg = gerenciador.registrar_pagamento(5, "Teste", "bitcoin", 100.00, 50.00)
    print(f"   {msg}")


if __name__ == "__main__":
    testar_pagamento()
    print("\n[OK] Teste concluído!")
