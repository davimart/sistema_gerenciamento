from django.contrib import admin

from .models import (
    Cliente,
    Constituido,
    Contem,
    ContemOrdemProducao,
    Fornece,
    Fornecedor,
    Funcionario,
    MateriaPrima,
    OrdemProducao,
    Pedido,
    Produto,
    Realiza,
    Recebe,
)


class CustomSearchAdmin(admin.ModelAdmin):
    search_help_text = "Campos pesquisáveis: "

    def get_search_results(self, request, queryset, search_term):
        self.search_fields = list(self.get_search_fields(request))
        self.search_help_text += ", ".join(
            [f'"{field.upper()}"' for field in self.search_fields]
        )
        return super().get_search_results(request, queryset, search_term)


@admin.register(Cliente)
class ClienteAdmin(CustomSearchAdmin):
    list_display = (
        "id_cliente",
        "nome",
        "telefone",
        "email",
        "numero",
        "cep",
        "complemento",
        "logradouro",
    )
    search_fields = ("nome", "email")
    list_filter = ("cep",)
    search_help_text = 'Campos pesquisáveis: "NOME", "EMAIL"'


class ContemInline(admin.TabularInline):
    model = Contem
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id_pedido", "data_pedido", "data_entrega", "status", "cliente")
    search_fields = ("id_pedido", "cliente__nome")
    list_filter = ("status", "data_pedido")
    search_help_text = 'Campos pesquisáveis: "ID_PEDIDO", "CLIENTE__NOME"'
    inlines = [
        ContemInline,
    ]


class ConstituidoInline(admin.TabularInline):
    model = Constituido
    extra = 1


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "id_produto",
        "nome",
        "descricao",
        "estoque_disponivel",
        "custo_unitario",
    )
    search_fields = ("nome", "descricao")
    list_filter = ("estoque_disponivel",)
    search_help_text = 'Campos pesquisáveis: "NOME", "DESCRICAO"'
    inlines = [ConstituidoInline]


@admin.register(Contem)
class ContemAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "produto", "quantidade")
    search_fields = ("pedido__id_pedido", "produto__nome")
    list_filter = ("pedido", "produto")
    search_help_text = 'Campos pesquisáveis: "PEDIDO__ID_PEDIDO", "PRODUTO__NOME"'


class ContemOrdemProducaoInline(admin.TabularInline):
    model = ContemOrdemProducao
    extra = 1


class RealizaInline(admin.TabularInline):
    model = Realiza
    extra = 1


@admin.register(OrdemProducao)
class OrdemProducaoAdmin(admin.ModelAdmin):
    list_display = (
        "id_ordem",
        "status",
        "custo_total",
        "data_criacao",
        "data_conclusao",
    )
    inlines = [ContemOrdemProducaoInline, RealizaInline]


@admin.register(ContemOrdemProducao)
class ContemOrdemProducaoAdmin(CustomSearchAdmin):
    list_display = ("id", "produto", "ordem", "quantidade")
    search_fields = ("produto__nome", "ordem__id_ordem")
    list_filter = ("produto", "ordem")
    search_help_text = 'Campos pesquisáveis: "PRODUTO__NOME", "ORDEM__ID_ORDEM"'


@admin.register(MateriaPrima)
class MateriaPrimaAdmin(CustomSearchAdmin):
    list_display = ("id_materiaprima", "nome", "custo_unidade", "estoque_disponivel")
    search_fields = ("nome",)
    list_filter = ("estoque_disponivel",)
    search_help_text = 'Campos pesquisáveis: "NOME"'


@admin.register(Constituido)
class ConstituidoAdmin(CustomSearchAdmin):
    list_display = ("id", "produto", "materiaprima", "quantidade")
    search_fields = ("produto__nome", "materiaprima__nome")
    list_filter = ("produto", "materiaprima")
    search_help_text = 'Campos pesquisáveis: "PRODUTO__NOME", "MATERIAPRIMA__NOME"'


class ForneceInline(admin.TabularInline):
    model = Fornece
    extra = 1


@admin.register(Fornecedor)
class FornecedorAdmin(CustomSearchAdmin):
    list_display = ("id_fornecedor", "nome", "avaliacao", "telefone", "email")
    search_fields = ("nome", "email")
    list_filter = ("avaliacao",)
    search_help_text = 'Campos pesquisáveis: "NOME", "EMAIL"'
    inlines = [ForneceInline]


@admin.register(Fornece)
class ForneceAdmin(CustomSearchAdmin):
    list_display = ("id", "fornecedor", "materiaprima", "preco")
    search_fields = ("fornecedor__nome", "materiaprima__nome")
    list_filter = ("fornecedor", "materiaprima")
    search_help_text = 'Campos pesquisáveis: "FORNECEDOR__NOME", "MATERIAPRIMA__NOME"'


@admin.register(Funcionario)
class FuncionarioAdmin(CustomSearchAdmin):
    list_display = ("id_funcionario", "nome", "cargo", "salario")
    search_fields = ("nome", "cargo")
    list_filter = ("cargo",)
    search_help_text = 'Campos pesquisáveis: "NOME", "CARGO"'


@admin.register(Recebe)
class RecebeAdmin(CustomSearchAdmin):
    list_display = ("id", "funcionario", "pedido")
    search_fields = ("funcionario__nome", "pedido__id_pedido")
    list_filter = ("funcionario", "pedido")
    search_help_text = 'Campos pesquisáveis: "FUNCIONARIO__NOME", "PEDIDO__ID_PEDIDO"'


@admin.register(Realiza)
class RealizaAdmin(CustomSearchAdmin):
    list_display = ("id", "funcionario", "ordem")
    search_fields = ("funcionario__nome", "ordem__id_ordem")
    list_filter = ("funcionario", "ordem")
    search_help_text = 'Campos pesquisáveis: "FUNCIONARIO__NOME", "ORDEM__ID_ORDEM"'
