"""
Teste do módulo de árvore de componentes.
"""

from oficina.componentes import ArvoreComponentes


def testar_componentes():
    print("=== TESTE ÁRVORE DE COMPONENTES ===\n")

    arvore = ArvoreComponentes()

    # Exibir árvore
    print("1. Árvore de componentes (exibição indentada):")
    print(arvore.exibir_arvore())
    print()

    # Buscar componente
    print("2. Buscar componentes:")
    componente = arvore.buscar_componente("Vela")
    print(f"   Vela: {componente}")
    componente = arvore.buscar_componente("Inexistente")
    print(f"   Inexistente: {componente}\n")

    # Marcar defeitos
    print("3. Marcar componentes com defeito:")
    resultado, msg = arvore.marcar_defeito("Vela")
    print(f"   {msg}")
    resultado, msg = arvore.marcar_defeito("Pastilha dianteira")
    print(f"   {msg}")
    resultado, msg = arvore.marcar_defeito("Amortecedor")
    print(f"   {msg}")
    resultado, msg = arvore.marcar_defeito("Inexistente")
    print(f"   {msg}\n")

    # Exibir árvore com defeitos
    print("4. Árvore com defeitos marcados:")
    print(arvore.exibir_arvore())
    print()

    # Relatório de diagnóstico
    print("5. Relatório de diagnóstico:")
    print(arvore.relatorio_diagnostico())
    print()

    # Listar peças com defeito
    print("6. Listar peças com defeito:")
    pecas = arvore.listar_pecas_com_defeito()
    for peca in pecas:
        print(f"   - {peca}")
    print()

    # Marcar como OK
    print("7. Marcar componente como OK:")
    resultado, msg = arvore.marcar_ok("Vela")
    print(f"   {msg}")
    print(arvore.exibir_arvore())
    print()

    # Relatório atualizado
    print("8. Relatório atualizado:")
    print(arvore.relatorio_diagnostico())


if __name__ == "__main__":
    testar_componentes()
    print("\n[OK] Teste concluído!")
