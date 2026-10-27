# Oficina Mecânica - Sistema de Gestão

Sistema de gestão para oficina mecânica desenvolvido para a disciplina de Estrutura de Dados da Fatec Rio Claro.

## Estrutura do Projeto

```
oficina/
├── clientes.py          # Controle de clientes e veículos
├── estoque.py           # Controle de estoque de peças
├── atendimento.py      # Controle de fila de espera
├── componentes.py      # Árvore de componentes para diagnóstico
├── ordem_servico.py     # Gestão de ordens de serviço
├── pagamento.py         # Controle de pagamentos
└── sistema.py           # Integração de todos os módulos
```

## Combinações de Estruturas de Dados

### 1. Clientes e Veículos

**Estruturas envolvidas:**
- `Lista` (encadeada) de clientes
- Cada `Cliente` contém uma `Lista` (encadeada) de veículos

**Classes e métodos:**
- `GerenciadorClientes.clientes` - Lista de clientes
- `Cliente.veiculos` - Lista de veículos do cliente
- `GerenciadorClientes.buscar_veiculo_por_placa(placa)` - Percorre as duas listas

**Justificativa:**
Esta combinação é adequada porque permite que um cliente tenha múltiplos veículos sem limite pré-definido, mantendo a organização e permitindo busca eficiente por CPF (cliente) ou placa (veículo).

**Desvantagem de usar uma única estrutura:**
Se usássemos apenas uma lista de veículos, perderíamos a relação direta cliente-veículo, tornando difícil gerenciar veículos do mesmo cliente ou listar todos os veículos de um cliente específico.

---

### 2. Estoque com Múltiplos Lotes

**Estruturas envolvidas:**
- `Lista` (encadeada) de produtos
- Cada `Produto` contém uma `Fila` (FIFO) de lotes

**Classes e métodos:**
- `GerenciadorEstoque.produtos` - Lista de produtos
- `Produto.lotes` - Fila de lotes do produto
- `Produto.baixar_estoque(quantidade)` - Consome do lote mais antigo (FIFO)

**Justificativa:**
Esta combinação é ideal para implementar a regra FIFO (First In, First Out), onde a saída deve sempre consumir o lote mais antigo. A fila garante que os lotes sejam consumidos na ordem de chegada.

**Desvantagem de usar uma única estrutura:**
Se usássemos apenas uma lista de lotes (sem separação por produto), teríamos que filtrar lotes por produto toda vez que precisássemos baixar estoque, o que seria menos eficiente e mais complexo.

---

### 3. Atendimento com Prioridade para Guincho

**Estruturas envolvidas:**
- `Fila` (FIFO) de veículos normais
- `Fila` (FIFO) de veículos de guincho (prioridade)

**Classes e métodos:**
- `GerenciadorFila.fila_normal` - Fila de veículos normais
- `GerenciadorFila.fila_guincho` - Fila de veículos de guincho
- `GerenciadorFila.proximo_veiculo()` - Verifica fila de guincho primeiro, depois normal

**Justificativa:**
Esta combinação permite implementar prioridade de forma clara: veículos de guincho são atendidos antes, mas respeitando a ordem de chegada entre si. Duas filas separadas tornam a lógica simples e eficiente.

**Desvantagem de usar uma única estrutura:**
Se usássemos apenas uma fila com um campo de prioridade, teríamos que implementar uma lógica complexa de reordenamento ou uma fila de prioridade (heap), o que seria desnecessário para este caso simples de apenas dois níveis de prioridade.

---

## Estruturas de Dados Implementadas

### Lista Encadeada
- Implementação genérica com nós encadeados
- Operações: inserir, remover, buscar por chave
- Usada em: clientes, produtos, OS, pagamentos

### Fila (FIFO)
- Implementação genérica First In, First Out
- Operações: enfileirar, desenfileirar, ver frente
- Usada em: estoque (lotes), atendimento (filas normal e guincho)

### Árvore Genérica (não binária)
- Implementação onde cada nó pode ter 0 a N filhos
- Percurso em profundidade (pré-ordem)
- Usada em: árvore de componentes do veículo

## Funcionalidades do Sistema

1. **Controle de Clientes e Veículos**
   - Cadastrar/remover clientes e veículos
   - Buscar por CPF ou placa

2. **Controle de Estoque**
   - Cadastrar produtos e lotes
   - Baixa de estoque (FIFO)
   - Controle de validade e perdas
   - Alertas de estoque baixo

3. **Controle de Atendimento**
   - Fila de espera com prioridade para guincho
   - Gestão de boxes de serviço

4. **Diagnóstico**
   - Árvore hierárquica de componentes
   - Marcar peças com defeito
   - Relatório de diagnóstico

5. **Ordem de Serviço**
   - Abrir/fechar OS
   - Adicionar/remover peças e serviços
   - Controle de remontagem

6. **Pagamento**
   - PIX, cartão (à vista/parcelado), dinheiro
   - Registro de pagamentos por OS

7. **Sistema Integrado**
   - Fluxo completo de atendimento
   - Relatórios gerais

## Como Usar

```python
from oficina import SistemaOficina

# Criar sistema
sistema = SistemaOficina()

# Cadastrar cliente
sistema.cadastrar_cliente("João Silva", "123.456.789-00", "11-99999-9999")

# Cadastrar veículo
sistema.cadastrar_veiculo("123.456.789-00", "ABC-1234", "Uno", "Fiat", 2020)

# Simular atendimento completo
sistema.atendimento_completo(
    placa="ABC-1234",
    nome_cliente="João Silva",
    queixa="Barulho no freio",
    mecanico="Mecânico Carlos",
    forma_pagamento="cartao",
    nome_pagador="João Silva",
    num_parcelas=3
)
```

## Requisitos

- Python 3.x
- Nenhuma dependência externa (apenas biblioteca padrão)
