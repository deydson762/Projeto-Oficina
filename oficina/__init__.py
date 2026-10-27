"""
Pacote do sistema de oficina mecânica.
"""

from .clientes import Cliente, Veiculo, GerenciadorClientes
from .estoque import Produto, Lote, GerenciadorEstoque
from .atendimento import VeiculoEspera, GerenciadorFila
from .componentes import Componente, ArvoreComponentes
from .ordem_servico import OS, GerenciadorOS
from .pagamento import Pagamento, GerenciadorPagamento

__all__ = ['Cliente', 'Veiculo', 'GerenciadorClientes', 'Produto', 'Lote', 'GerenciadorEstoque', 'VeiculoEspera', 'GerenciadorFila', 'Componente', 'ArvoreComponentes', 'OS', 'GerenciadorOS', 'Pagamento', 'GerenciadorPagamento']
