"""
Pacote do sistema de oficina mecânica.
"""

from .clientes import Cliente, Veiculo, GerenciadorClientes
from .estoque import Produto, Lote, GerenciadorEstoque
from .atendimento import VeiculoEspera, GerenciadorFila

__all__ = ['Cliente', 'Veiculo', 'GerenciadorClientes', 'Produto', 'Lote', 'GerenciadorEstoque', 'VeiculoEspera', 'GerenciadorFila']
