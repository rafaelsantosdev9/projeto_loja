import json

def formata_preco(valor):
    return f'R$ {valor:.2f}'.replace('.',',')

def cart_total_qtd(carrinho):
    if isinstance(carrinho, str):
        try:
            carrinho = json.loads(carrinho)
        except json.JSONDecodeError:
            carrinho = {}
    
    return sum([item.get('quantidade', 0) for item in carrinho.values()])

def cart_totals(carrinho):
    return sum(
    [ item.get('preco_quantitativo_promocional')
      if item.get('preco_quantitativo_promocional')
      else item.get('preco_quantitativo')
      for item in carrinho.values()

    ]
    )