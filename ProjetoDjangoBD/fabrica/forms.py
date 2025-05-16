from django import forms


class ClienteSearchForm(forms.Form):
    id_cliente = forms.IntegerField(
        required=False,
        label="ID Cliente",
        widget=forms.TextInput(
            attrs={"placeholder": "Digite o ID do cliente", "class": "form-control"}
        ),
    )
    nome = forms.CharField(
        required=False,
        label="Nome",
        widget=forms.TextInput(
            attrs={"placeholder": "Digite o nome do cliente", "class": "form-control"}
        ),
    )
    telefone = forms.CharField(
        required=False,
        label="Telefone",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Digite o telefone do cliente",
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={"placeholder": "Digite o email do cliente", "class": "form-control"}
        ),
    )
    numero = forms.IntegerField(
        required=False,
        label="Número",
        widget=forms.TextInput(
            attrs={"placeholder": "Digite o número do cliente", "class": "form-control"}
        ),
    )
    cep = forms.CharField(
        required=False,
        label="CEP",
        widget=forms.TextInput(
            attrs={"placeholder": "Digite o CEP do cliente", "class": "form-control"}
        ),
    )
    complemento = forms.CharField(
        required=False,
        label="Complemento",
        widget=forms.TextInput(
            attrs={"placeholder": "Digite o complemento", "class": "form-control"}
        ),
    )
    logradouro = forms.CharField(
        required=False,
        label="Logradouro",
        widget=forms.TextInput(
            attrs={"placeholder": "Digite o logradouro", "class": "form-control"}
        ),
    )


class PedidoSearchForm(forms.Form):
    id_pedido = forms.IntegerField(
        required=False,
        label="ID Pedido",
        widget=forms.TextInput(attrs={"placeholder": "Digite o ID do pedido"}),
    )
    pedido_start_date = forms.DateField(
        required=False,
        label="Data Inicial Pedido",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    pedido_end_date = forms.DateField(
        required=False,
        label="Data Final Pedido",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    entrega_start_date = forms.DateField(
        required=False,
        label="Data Inicial Entrega",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    entrega_end_date = forms.DateField(
        required=False,
        label="Data Final Entrega",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    status = forms.CharField(
        required=False,
        label="Status",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Digite o status do pedido"}),
    )
    cliente_id = forms.IntegerField(
        required=False,
        label="Cliente ID",
        widget=forms.TextInput(attrs={"placeholder": "Digite o ID do cliente"}),
    )
    forma_pagamento = forms.CharField(
        required=False,
        label="Forma de Pagamento",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Digite a forma de pagamento"}),
    )
    pagamento_start_date = forms.DateField(
        required=False,
        label="Data Inicial Pagamento",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    pagamento_end_date = forms.DateField(
        required=False,
        label="Data Final Pagamento",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    valor_total_min = forms.DecimalField(
        required=False,
        label="Valor Total Mínimo",
        widget=forms.NumberInput(attrs={"placeholder": "Valor mínimo (R$)"}),
    )
    valor_total_max = forms.DecimalField(
        required=False,
        label="Valor Total Máximo",
        widget=forms.NumberInput(attrs={"placeholder": "Valor máximo (R$)"}),
    )


class FornecedorSearchForm(forms.Form):
    id_fornecedor = forms.IntegerField(
        required=False,
        label="ID Fornecedor",
        widget=forms.TextInput(attrs={"placeholder": "Digite o ID do fornecedor"}),
    )
    nome = forms.CharField(
        required=False,
        label="Nome",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome do fornecedor"}),
    )
    avaliacao_min = forms.DecimalField(
        required=False,
        label="Avaliação Mínima",
        widget=forms.NumberInput(attrs={"placeholder": "Avaliação mínima"}),
    )
    avaliacao_max = forms.DecimalField(
        required=False,
        label="Avaliação Máxima",
        widget=forms.NumberInput(attrs={"placeholder": "Avaliação máxima"}),
    )
    materia_prima = forms.CharField(
        required=False,
        label="Matéria-Prima",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome da matéria-prima"}),
    )


class ProdutoSearchForm(forms.Form):
    id_produto = forms.IntegerField(
        required=False,
        label="ID Produto",
        widget=forms.TextInput(attrs={"placeholder": "Digite o ID do produto"}),
    )
    nome = forms.CharField(
        required=False,
        label="Nome",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome do produto"}),
    )
    estoque_disponivel_min = forms.IntegerField(
        required=False,
        label="Estoque Disponível Mínimo",
        widget=forms.NumberInput(attrs={"placeholder": "Estoque mínimo"}),
    )
    estoque_disponivel_max = forms.IntegerField(
        required=False,
        label="Estoque Disponível Máximo",
        widget=forms.NumberInput(attrs={"placeholder": "Estoque máximo"}),
    )
    custo_unitario_min = forms.DecimalField(
        required=False,
        label="Custo Unitário Mínimo",
        widget=forms.NumberInput(attrs={"placeholder": "Custo mínimo (R$)"}),
    )
    custo_unitario_max = forms.DecimalField(
        required=False,
        label="Custo Unitário Máximo",
        widget=forms.NumberInput(attrs={"placeholder": "Custo máximo (R$)"}),
    )


class MateriaPrimaSearchForm(forms.Form):
    id_materiaprima = forms.IntegerField(
        required=False,
        label="ID Matéria-Prima",
        widget=forms.TextInput(attrs={"placeholder": "Digite o ID da matéria-prima"}),
    )
    nome = forms.CharField(
        required=False,
        label="Nome",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome da matéria-prima"}),
    )
    estoque_disponivel_min = forms.IntegerField(
        required=False,
        label="Estoque Disponível Mínimo",
        widget=forms.NumberInput(attrs={"placeholder": "Estoque mínimo"}),
    )
    estoque_disponivel_max = forms.IntegerField(
        required=False,
        label="Estoque Disponível Máximo",
        widget=forms.NumberInput(attrs={"placeholder": "Estoque máximo"}),
    )
    custo_unitario_min = forms.DecimalField(
        required=False,
        label="Custo Unitário Mínimo",
        widget=forms.NumberInput(attrs={"placeholder": "Custo mínimo (R$)"}),
    )
    custo_unitario_max = forms.DecimalField(
        required=False,
        label="Custo Unitário Máximo",
        widget=forms.NumberInput(attrs={"placeholder": "Custo máximo (R$)"}),
    )


class OrdemSearchForm(forms.Form):
    id_ordem = forms.IntegerField(
        required=False,
        label="ID Ordem",
        widget=forms.TextInput(attrs={"placeholder": "Digite o ID da ordem"}),
    )
    status = forms.CharField(
        required=False,
        label="Status",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Digite o status da ordem"}),
    )
    custo_total_min = forms.DecimalField(
        required=False,
        label="Custo Total Mínimo",
        widget=forms.NumberInput(attrs={"placeholder": "Custo mínimo (R$)"}),
    )
    custo_total_max = forms.DecimalField(
        required=False,
        label="Custo Total Máximo",
        widget=forms.NumberInput(attrs={"placeholder": "Custo máximo (R$)"}),
    )
    data_criacao_start_date = forms.DateField(
        required=False,
        label="Data Inicial Criação",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    data_criacao_end_date = forms.DateField(
        required=False,
        label="Data Final Criação",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    data_conclusao_start_date = forms.DateField(
        required=False,
        label="Data Inicial Conclusão",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    data_conclusao_end_date = forms.DateField(
        required=False,
        label="Data Final Conclusão",
        widget=forms.DateInput(
            attrs={"placeholder": "AAAA-MM-DD", "class": "form-control"}
        ),
    )
    funcionario_nome = forms.CharField(
        required=False,
        label="Nome do Funcionário",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome do funcionário"}),
    )
    funcionario_cargo = forms.CharField(
        required=False,
        label="Cargo do Funcionário",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Digite o cargo do funcionário"}),
    )
    produto_nome = forms.CharField(
        required=False,
        label="Nome do Produto",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome do produto"}),
    )
    produto_quantidade_min = forms.IntegerField(
        required=False,
        label="Quantidade Mínima do Produto",
        widget=forms.NumberInput(attrs={"placeholder": "Quantidade mínima"}),
    )
    produto_quantidade_max = forms.IntegerField(
        required=False,
        label="Quantidade Máxima do Produto",
        widget=forms.NumberInput(attrs={"placeholder": "Quantidade máxima"}),
    )
