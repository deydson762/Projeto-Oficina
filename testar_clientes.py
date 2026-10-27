"""
Teste do módulo de clientes e veículos.
"""

from oficina.clientes import GerenciadorClientes


def testar_clientes():
    print("=== TESTE CLIENTES E VEÍCULOS ===\n")

    gerenciador = GerenciadorClientes()

    # Cadastrar clientes
    print("1. Cadastrar clientes:")
    resultado, msg = gerenciador.cadastrar_cliente("João Silva", "123.456.789-00", "11-99999-9999")
    print(f"   {msg}")
    resultado, msg = gerenciador.cadastrar_cliente("Maria Santos", "987.654.321-00", "11-88888-8888")
    print(f"   {msg}")
    resultado, msg = gerenciador.cadastrar_cliente("João Silva", "123.456.789-00", "11-77777-7777")
    print(f"   {msg} (tentativa duplicada)\n")

    # Cadastrar veículos
    print("2. Cadastrar veículos:")
    resultado, msg = gerenciador.cadastrar_veiculo("123.456.789-00", "ABC-1234", "Uno", "Fiat", 2020)
    print(f"   {msg}")
    resultado, msg = gerenciador.cadastrar_veiculo("123.456.789-00", "XYZ-5678", "Gol", "Volkswagen", 2018)
    print(f"   {msg}")
    resultado, msg = gerenciador.cadastrar_veiculo("987.654.321-00", "DEF-4321", "Corolla", "Toyota", 2022)
    print(f"   {msg}")
    resultado, msg = gerenciador.cadastrar_veiculo("123.456.789-00", "ABC-1234", "Civic", "Honda", 2021)
    print(f"   {msg} (tentativa duplicada)\n")

    # Relatório completo
    print("3. Relatório completo:")
    print(gerenciador.relatorio_completo())

    # Buscar cliente por CPF
    print("4. Buscar cliente por CPF:")
    cliente = gerenciador.buscar_cliente("123.456.789-00")
    print(f"   {cliente}")
    cliente = gerenciador.buscar_cliente("000.000.000-00")
    print(f"   Cliente inexistente: {cliente}\n")

    # Buscar veículo por placa
    print("5. Buscar veículo por placa:")
    veiculo, cliente = gerenciador.buscar_veiculo_por_placa("ABC-1234")
    print(f"   Veículo: {veiculo}")
    print(f"   Cliente: {cliente}")
    veiculo, cliente = gerenciador.buscar_veiculo_por_placa("ZZZ-9999")
    print(f"   Veículo inexistente: {veiculo}\n")

    # Remover veículo
    print("6. Remover veículo:")
    resultado, msg = gerenciador.remover_veiculo("XYZ-5678")
    print(f"   {msg}")
    print(gerenciador.relatorio_completo())

    # Remover cliente
    print("7. Remover cliente:")
    resultado, msg = gerenciador.remover_cliente("987.654.321-00")
    print(f"   {msg}")
    print(gerenciador.relatorio_completo())


if __name__ == "__main__":
    testar_clientes()
    print("\n[OK] Teste concluído!")
