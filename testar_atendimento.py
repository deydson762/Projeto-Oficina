"""
Teste do módulo de controle de atendimento.
"""

from oficina.atendimento import GerenciadorFila
import time


def testar_atendimento():
    print("=== TESTE CONTROLE DE ATENDIMENTO ===\n")

    gerenciador = GerenciadorFila(num_boxes=3)

    # Adicionar veículos à fila normal
    print("1. Adicionar veículos à fila normal:")
    gerenciador.adicionar_veiculo("ABC-1234", "João Silva", "Barulho no freio")
    print("   Veículo ABC-1234 adicionado")
    gerenciador.adicionar_veiculo("XYZ-5678", "Maria Santos", "Motor falhando")
    print("   Veículo XYZ-5678 adicionado")
    gerenciador.adicionar_veiculo("DEF-4321", "Pedro Costa", "Troca de óleo")
    print("   Veículo DEF-4321 adicionado\n")

    # Adicionar veículos de guincho (prioridade)
    print("2. Adicionar veículos de guincho (prioridade):")
    gerenciador.adicionar_veiculo("GUN-9999", "Carlos Lima", "Acidente grave", eh_guincho=True)
    print("   Veículo GUN-9999 adicionado (guincho)")
    gerenciador.adicionar_veiculo("GUN-8888", "Ana Pereira", "Motor queimado", eh_guincho=True)
    print("   Veículo GUN-8888 adicionado (guincho)\n")

    # Relatório da fila
    print("3. Relatório da fila:")
    print(gerenciador.relatorio_fila())

    # Simular liberação de boxes
    print("4. Simular atendimento (liberar boxes):")
    for i in range(5):
        print(f"\n   Box liberado {i+1}:")
        tem_proximo, proximo = gerenciador.box_liberado()
        if tem_proximo:
            print(f"   Próximo veículo: {proximo}")
        else:
            print("   Nenhum veículo aguardando")

    print("\n5. Relatório após atendimentos:")
    print(gerenciador.relatorio_fila())

    # Buscar veículo
    print("6. Buscar veículo por placa:")
    veiculo = gerenciador.buscar_por_placa("XYZ-5678")
    if veiculo:
        print(f"   Encontrado: {veiculo}")
    else:
        print("   Veículo não encontrado")

    # Remover veículo
    print("\n7. Remover veículo da fila:")
    resultado, msg = gerenciador.remover_por_placa("XYZ-5678")
    print(f"   {msg}")
    print(gerenciador.relatorio_fila())


if __name__ == "__main__":
    testar_atendimento()
    print("\n[OK] Teste concluído!")
