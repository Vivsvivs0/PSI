from django.shortcuts import render, get_object_or_404, redirect
from loja.models import Produto, Carrinho, CarrinhoItem
from datetime import datetime

# Função para adicionar um item ao carrinho
def create_carrinhoitem_view(request, produto_id=None):
    print('create_carrinhoitem_view')

    # Obtém o produto ou retorna 404
    produto = get_object_or_404(Produto, pk=produto_id)
    if produto:
        print(f'Produto: {produto.id}')

    # Tenta pegar o carrinho da sessão ou cria um novo carrinho
    carrinho_id = request.session.get('carrinho_id')
    print(f'Carrinho ID na sessão: {carrinho_id}')
    carrinho = None

    if carrinho_id:
        # Tenta obter o carrinho da base de dados
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        print(f'Carrinho encontrado: {carrinho}')
        if carrinho:
            print(f'Carrinho ID: {carrinho.id}')
            hoje = datetime.today().date()

            # Verifica se o carrinho é do dia atual
            if carrinho.criado_em.date() != hoje:
                # Se não for, cria um novo carrinho
                carrinho = Carrinho.objects.create()
                request.session['carrinho_id'] = carrinho.id
                print(f'Novo carrinho criado: {carrinho.id}')
    else:
        # Se não houver carrinho na sessão, cria um novo
        carrinho = Carrinho.objects.create()
        request.session['carrinho_id'] = carrinho.id
        print(f'Carrinho criado: {carrinho.id}')

    # Verifica se o produto já existe no carrinho
    carrinho_item = CarrinhoItem.objects.filter(carrinho=carrinho, produto=produto).first()
    if carrinho_item:
        # Se já existir, incrementa a quantidade
        carrinho_item.quantidade += 1
        print(f'Quantidade aumentada para o item do produto {carrinho_item.id}')
    else:
        # Caso contrário, cria um novo item no carrinho
        carrinho_item = CarrinhoItem.objects.create(
            carrinho=carrinho,
            produto=produto,
            quantidade=1,
            preco=produto.preco
        )
        print(f'Novo item de carrinho criado: {carrinho_item.id}')

    # Salva o item no banco de dados
    carrinho_item.save()
    print(f'Item do carrinho salvo: {carrinho_item.id}')

    # Redireciona para a página do carrinho
    return redirect('/carrinho')
