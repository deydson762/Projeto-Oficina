"""
Teste do módulo de controle de estoque.
"""

from datetime import datetime, timedelta
from oficina.estoque import GerenciadorEstoque


def testar_estoque():
    print("=== TESTE CONTROLE DE ESTOQUE ===\n")

    gerenciador = GerenciadorEstoque()

    # Cadastrar produtos
    print("1. Cadastrar produtos:")
    resultado, msg = gerenciador.cadastrar_produto("PEC001", "Pastilha de Freio", "Freios Ltda", 150.00, 20)
    print(f"   {msg}")
    resultado, msg = gerenciador.cadastrar_produto("PEC002", "Óleo de Motor 5W30", "Lubrificantes SA", 80.00, 15)
    print(f"   {msg}")
    resultado, msg = gerenciador.cadastrar_produto("PEC003", "Filtro de Óleo", "AutoPeças", 35.00, 10)
    print(f"   {msg}\n")

    # Adicionar lotes
    print("2. Adicionar lotes:")
    data_atual = datetime.now()
    data_vencida = data_atual - timedelta(days=10)  # 10 dias atrás (vencido)
    data_futura = data_atual + timedelta(days=365)  # 1 ano no futuro

    resultado, msg = gerenciador.adicionar_lote("PEC001", "LOT-001", data_atual, None, 50, 80.00)
    print(f"   {msg}")
    resultado, msg = gerenciador.adicionar_lote("PEC001", "LOT-002", data_atual, data_futura, 30, 85.00)
    print(f"   {msg}")
    resultado, msg = gerenciador.adicionar_lote("PEC002", "LOT-003", data_atual, data_futura, 100, 45.00)
    print(f"   {msg}")
    resultado, msg = gerenciador.adicionar_lote("PEC002", "LOT-004", data_atual, data_vencida, 20, 40.00)  # Vencido
    print(f"   {msg} (lote vencido)\n")

    # Relatório de estoque
    print("3. Relatório de estoque:")
    print(gerenciador.relatorio_estoque())

    # Limpar lotes vencidos
    print("4. Limpar lotes vencidos:")
    perdas = gerenciador.limpar_lotes_vencidos()
    print(f"   {len(perdas)} lote(s) vencido(s) removido(s)")
    for perda in perdas:
        print(f"   - {perda['produto']}: {perda['quantidade']} unidades (R$ {perda['valor']:.2f})")
    print()
    print(gerenciador.relatorio_estoque())

    # Baixar estoque (FIFO)
    print("5. Baixar estoque (consumo FIFO):")
    resultado, msg = gerenciador.baixar_estoque("PEC001", 25)
    print(f"   {msg}")
    resultado, msg = gerenciador.baixar_estoque("PEC001", 30)
    print(f"   {msg}")
    print(gerenciador.relatorio_estoque())

    # Verificar alertas
    print("6. Verificar alertas de estoque baixo:")
    alertas = gerenciador.verificar_alertas()
    if alertas:
        print(f"   {len(alertas)} produto(s) com estoque abaixo do mínimo:")
        for produto in alertas:
            print(f"   - {produto.nome}: {produto.quantidade_total()} unidades (mínimo: {produto.estoque_minimo})")
    else:
        print("   Nenhum produto com estoque baixo.\n")

    # Ajustar inventário
    print("7. Ajustar inventário:")
    resultado, msg = gerenciador.ajustar_inventario("PEC001", 100)
    print(f"   {msg}")
    print(gerenciador.relatorio_estoque())

    # Relatório de perdas
    print("8. Relatório de perdas:")
    print(gerenciador.relatorio_perdas())


if __name__ == "__main__":
    testar_estoque()
    print("\n[OK] Teste concluído!")
