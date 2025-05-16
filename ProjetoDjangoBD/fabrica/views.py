from django.db import connection
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from .forms import (
    ClienteSearchForm,
    FornecedorSearchForm,
    MateriaPrimaSearchForm,
    OrdemSearchForm,
    PedidoSearchForm,
    ProdutoSearchForm,
)
from .models import (
    Cliente,
    Contem,
    ContemOrdemProducao,
    Fornece,
    Fornecedor,
    Funcionario,
    MateriaPrima,
    OrdemProducao,
    Pedido,
    Produto,
)


class ClientesListView(View):
    """Mostra todos os clientes que se enquadram nos filtros selecionados na
    pagina de clientes"""

    def get(self, request):
        form = ClienteSearchForm(request.GET)
        base_query = """
            SELECT *
            FROM Cliente
        """
        where_clauses = []
        params = []

        if form.is_valid():
            if form.cleaned_data.get("id_cliente"):
                where_clauses.append("id_cliente = %s")
                params.append(form.cleaned_data.get("id_cliente"))
            if form.cleaned_data.get("nome"):
                where_clauses.append("nome LIKE %s")
                params.append(f"%{form.cleaned_data.get('nome')}%")
            if form.cleaned_data.get("telefone"):
                where_clauses.append("telefone LIKE %s")
                params.append(f"%{form.cleaned_data.get('telefone')}%")
            if form.cleaned_data.get("email"):
                where_clauses.append("email LIKE %s")
                params.append(f"%{form.cleaned_data.get('email')}%")
            if form.cleaned_data.get("numero"):
                where_clauses.append("numero = %s")
                params.append(form.cleaned_data.get("numero"))
            if form.cleaned_data.get("cep"):
                where_clauses.append("cep LIKE %s")
                params.append(f"%{form.cleaned_data.get('cep')}%")
            if form.cleaned_data.get("complemento"):
                where_clauses.append("complemento LIKE %s")
                params.append(f"%{form.cleaned_data.get('complemento')}%")
            if form.cleaned_data.get("logradouro"):
                where_clauses.append("logradouro LIKE %s")
                params.append(f"%{form.cleaned_data.get('logradouro')}%")

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        clientes = Cliente.objects.raw(base_query, params)

        return render(
            request, "lista_clientes.html", {"clientes": clientes, "form": form}
        )


class ClienteDetailView(View):
    """Detalhes do cliente."""

    def get(self, request, pk):
        cliente = list(
            Cliente.objects.raw(
                """SELECT *
                   FROM Cliente
                   WHERE id_cliente = %s""",
                [pk],
            )
        )

        if cliente:
            cliente = cliente[0]
        else:
            cliente = get_object_or_404(Cliente, pk=pk)

        pedidos_last_30_days_query = """
            SELECT
                p.*,
                pr.id_produto,
                pr.nome AS produto_nome,
                pr.descricao,
                pr.estoque_disponivel,
                pr.limite_estoque_baixo,
                pr.custo_unitario,
                c.quantidade,
                (pr.custo_unitario * c.quantidade) AS subtotal,
                SUM(pr.custo_unitario * c.quantidade) OVER (PARTITION BY p.id_pedido) AS valor_total
            FROM
                Contem c
                JOIN Produto pr ON c.produto_id = pr.id_produto
                JOIN Pedido p ON c.pedido_id = p.id_pedido
            WHERE
                p.cliente_id = %s
                AND p.data_pedido BETWEEN CURRENT_DATE - INTERVAL '30 days'
                AND CURRENT_DATE
            ORDER BY
                p.data_pedido DESC;
        """
        pedidos_last_30_days = list(
            Pedido.objects.raw(pedidos_last_30_days_query, [pk])
        )

        pedidos_dict = {}
        for pedido in pedidos_last_30_days:
            if pedido.id_pedido not in pedidos_dict:
                pedidos_dict[pedido.id_pedido] = {"pedido": pedido, "produtos": []}
            pedidos_dict[pedido.id_pedido]["produtos"].append(pedido)

        return render(
            request,
            "detalhe_cliente.html",
            {
                "cliente": cliente,
                "pedidos_dict": pedidos_dict,
            },
        )


class EstoqueListView(View):
    def get(self, request):
        produto_form = ProdutoSearchForm(
            request.GET if "id_produto" in request.GET else None
        )
        materia_prima_form = MateriaPrimaSearchForm(
            request.GET if "id_materiaprima" in request.GET else None
        )

        produtos_query = """
            SELECT *, (limite_estoque_baixo - estoque_disponivel) AS diff
            FROM Produto
        """
        materias_primas_query = """
            SELECT *, (limite_estoque_baixo - estoque_disponivel) AS diff
            FROM MateriaPrima
        """

        produto_params = []
        produto_conditions = []

        if produto_form.is_valid():
            if produto_form.cleaned_data.get("id_produto"):
                produto_conditions.append("id_produto = %s")
                produto_params.append(produto_form.cleaned_data["id_produto"])
            if produto_form.cleaned_data.get("nome"):
                produto_conditions.append("nome LIKE %s")
                produto_params.append(f"%{produto_form.cleaned_data['nome']}%")
            if produto_form.cleaned_data.get("estoque_disponivel_min") is not None:
                produto_conditions.append("estoque_disponivel >= %s")
                produto_params.append(
                    produto_form.cleaned_data["estoque_disponivel_min"]
                )
            if produto_form.cleaned_data.get("estoque_disponivel_max") is not None:
                produto_conditions.append("estoque_disponivel <= %s")
                produto_params.append(
                    produto_form.cleaned_data["estoque_disponivel_max"]
                )
            if produto_form.cleaned_data.get("custo_unitario_min") is not None:
                produto_conditions.append("custo_unitario >= %s")
                produto_params.append(produto_form.cleaned_data["custo_unitario_min"])
            if produto_form.cleaned_data.get("custo_unitario_max") is not None:
                produto_conditions.append("custo_unitario <= %s")
                produto_params.append(produto_form.cleaned_data["custo_unitario_max"])

        if produto_conditions:
            produtos_query += " WHERE " + " AND ".join(produto_conditions)

        materiaprima_params = []
        materiaprima_conditions = []

        if materia_prima_form.is_valid():
            if materia_prima_form.cleaned_data.get("id_materiaprima"):
                materiaprima_conditions.append("id_materiaprima = %s")
                materiaprima_params.append(
                    materia_prima_form.cleaned_data["id_materiaprima"]
                )
            if materia_prima_form.cleaned_data.get("nome"):
                materiaprima_conditions.append("nome LIKE %s")
                materiaprima_params.append(
                    f"%{materia_prima_form.cleaned_data['nome']}%"
                )
            if (
                materia_prima_form.cleaned_data.get("estoque_disponivel_min")
                is not None
            ):
                materiaprima_conditions.append("estoque_disponivel >= %s")
                materiaprima_params.append(
                    materia_prima_form.cleaned_data["estoque_disponivel_min"]
                )
            if (
                materia_prima_form.cleaned_data.get("estoque_disponivel_max")
                is not None
            ):
                materiaprima_conditions.append("estoque_disponivel <= %s")
                materiaprima_params.append(
                    materia_prima_form.cleaned_data["estoque_disponivel_max"]
                )
            if materia_prima_form.cleaned_data.get("custo_unitario_min") is not None:
                materiaprima_conditions.append("custo_unidade >= %s")
                materiaprima_params.append(
                    materia_prima_form.cleaned_data["custo_unitario_min"]
                )
            if materia_prima_form.cleaned_data.get("custo_unitario_max") is not None:
                materiaprima_conditions.append("custo_unidade <= %s")
                materiaprima_params.append(
                    materia_prima_form.cleaned_data["custo_unitario_max"]
                )

        if materiaprima_conditions:
            materias_primas_query += " WHERE " + " AND ".join(materiaprima_conditions)

        produtos_query += " ORDER BY diff DESC"
        materias_primas_query += " ORDER BY diff DESC"

        produtos = Produto.objects.raw(produtos_query, produto_params)
        materias_primas = MateriaPrima.objects.raw(
            materias_primas_query, materiaprima_params
        )

        produtos_baixo_estoque_query = """
            SELECT *
            FROM Produto
            WHERE estoque_disponivel < limite_estoque_baixo
        """
        materias_primas_baixo_estoque_query = """
            SELECT *
            FROM MateriaPrima
            WHERE estoque_disponivel < limite_estoque_baixo
        """

        produtos_baixo_estoque = Produto.objects.raw(produtos_baixo_estoque_query)
        materias_primas_baixo_estoque = MateriaPrima.objects.raw(
            materias_primas_baixo_estoque_query
        )

        return render(
            request,
            "estoque.html",
            {
                "produtos": produtos,
                "materias_primas": materias_primas,
                "produtos_baixo_estoque": produtos_baixo_estoque,
                "materias_primas_baixo_estoque": materias_primas_baixo_estoque,
                "produto_form": produto_form,
                "materia_prima_form": materia_prima_form,
            },
        )


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class PedidosListView(View):
    def get(self, request):
        form = PedidoSearchForm(request.GET)

        query_filters = []
        query_params = []
        having_filters = []

        base_query = """
            SELECT
                Pedido.*,
                SUM(Produto.custo_unitario * Contem.quantidade) AS valor_total
            FROM Pedido
                JOIN Contem ON Pedido.id_pedido = Contem.pedido_id
                JOIN Produto ON Contem.produto_id = Produto.id_produto
        """

        if form.is_valid():
            if form.cleaned_data.get("id_pedido"):
                query_filters.append("Pedido.id_pedido = %s")
                query_params.append(form.cleaned_data["id_pedido"])
            if form.cleaned_data.get("status"):
                query_filters.append("Pedido.status LIKE %s")
                query_params.append(f"%{form.cleaned_data['status']}%")
            if form.cleaned_data.get("cliente_id"):
                query_filters.append("Pedido.cliente_id = %s")
                query_params.append(form.cleaned_data["cliente_id"])
            if form.cleaned_data.get("forma_pagamento"):
                query_filters.append("Pedido.forma_pagamento LIKE %s")
                query_params.append(f"%{form.cleaned_data['forma_pagamento']}%")

            pedido_start_date = form.cleaned_data.get("pedido_start_date")
            pedido_end_date = form.cleaned_data.get("pedido_end_date")
            entrega_start_date = form.cleaned_data.get("entrega_start_date")
            entrega_end_date = form.cleaned_data.get("entrega_end_date")
            pagamento_start_date = form.cleaned_data.get("pagamento_start_date")
            pagamento_end_date = form.cleaned_data.get("pagamento_end_date")

            if pedido_start_date and pedido_end_date:
                query_filters.append("Pedido.data_pedido BETWEEN %s AND %s")
                query_params.extend([pedido_start_date, pedido_end_date])
            elif pedido_start_date:
                query_filters.append("Pedido.data_pedido >= %s")
                query_params.append(pedido_start_date)
            elif pedido_end_date:
                query_filters.append("Pedido.data_pedido <= %s")
                query_params.append(pedido_end_date)

            if entrega_start_date and entrega_end_date:
                query_filters.append(
                    "(Pedido.data_entrega BETWEEN %s AND %s OR Pedido.data_entrega IS NULL)"
                )
                query_params.extend([entrega_start_date, entrega_end_date])
            elif entrega_start_date:
                query_filters.append(
                    "(Pedido.data_entrega >= %s OR Pedido.data_entrega IS NULL)"
                )
                query_params.append(entrega_start_date)
            elif entrega_end_date:
                query_filters.append(
                    "(Pedido.data_entrega <= %s OR Pedido.data_entrega IS NULL)"
                )
                query_params.append(entrega_end_date)

            if pagamento_start_date and pagamento_end_date:
                query_filters.append("Pedido.data_pagamento BETWEEN %s AND %s")
                query_params.extend([pagamento_start_date, pagamento_end_date])
            elif pagamento_start_date:
                query_filters.append("Pedido.data_pagamento >= %s")
                query_params.append(pagamento_start_date)
            elif pagamento_end_date:
                query_filters.append("Pedido.data_pagamento <= %s")
                query_params.append(pagamento_end_date)

            valor_total_min = form.cleaned_data.get("valor_total_min")
            valor_total_max = form.cleaned_data.get("valor_total_max")
            if valor_total_min is not None:
                having_filters.append(
                    "SUM(Produto.custo_unitario * Contem.quantidade) >= %s"
                )
                query_params.append(valor_total_min)
            if valor_total_max is not None:
                having_filters.append(
                    "SUM(Produto.custo_unitario * Contem.quantidade) <= %s"
                )
                query_params.append(valor_total_max)

        filtered_query = f"{base_query}"
        if query_filters:
            filtered_query += f" WHERE {' AND '.join(query_filters)}"
        filtered_query += " GROUP BY Pedido.id_pedido"
        if having_filters:
            filtered_query += f" HAVING {' AND '.join(having_filters)}"
        filtered_query += " ORDER BY Pedido.data_pedido DESC"

        pedidos = Pedido.objects.raw(filtered_query, query_params)

        produtos_query = """
            SELECT
                Contem.*,
                Produto.*,
                Produto.custo_unitario * Contem.quantidade AS subtotal
            FROM Contem
                JOIN Produto ON Contem.produto_id = Produto.id_produto
                JOIN Pedido ON Contem.pedido_id = Pedido.id_pedido
        """
        produtos = Contem.objects.raw(produtos_query)

        return render(
            request,
            "pedidos.html",
            {"pedidos": pedidos, "produtos": produtos, "form": form},
        )


class FornecedoresListView(View):
    def get(self, request):
        form = FornecedorSearchForm(request.GET)

        query_filters = []
        query_params = []

        base_query = """
            SELECT *
            FROM Fornecedor
        """

        if form.is_valid():
            if form.cleaned_data.get("id_fornecedor"):
                query_filters.append("id_fornecedor = %s")
                query_params.append(form.cleaned_data["id_fornecedor"])
            if form.cleaned_data.get("nome"):
                query_filters.append("nome LIKE %s")
                query_params.append(f"%{form.cleaned_data['nome']}%")
            avaliacao_min = form.cleaned_data.get("avaliacao_min")
            avaliacao_max = form.cleaned_data.get("avaliacao_max")
            if avaliacao_min is not None:
                query_filters.append("avaliacao >= %s")
                query_params.append(avaliacao_min)
            if avaliacao_max is not None:
                query_filters.append("avaliacao <= %s")
                query_params.append(avaliacao_max)
            if form.cleaned_data.get("materia_prima"):
                query_filters.append("""
                    id_fornecedor IN (
                        SELECT fornecedor_id
                        FROM Fornece
                            JOIN MateriaPrima ON Fornece.materiaprima_id = MateriaPrima.id_materiaprima
                        WHERE MateriaPrima.nome LIKE %s
                    )
                """)
                query_params.append(f"%{form.cleaned_data['materia_prima']}%")

        if query_filters:
            filtered_query = f"{base_query} WHERE {' AND '.join(query_filters)} ORDER BY avaliacao DESC"
        else:
            filtered_query = f"{base_query} ORDER BY avaliacao DESC"

        fornecedores = Fornecedor.objects.raw(filtered_query, query_params)

        fornecimentos_query = """
            SELECT Fornece.*, Fornecedor.*, MateriaPrima.*
            FROM Fornece
                JOIN Fornecedor ON Fornece.fornecedor_id = Fornecedor.id_fornecedor
                JOIN MateriaPrima ON Fornece.materiaprima_id = MateriaPrima.id_materiaprima
        """
        fornecimentos = Fornece.objects.raw(fornecimentos_query)

        return render(
            request,
            "fornecedores.html",
            {
                "fornecedores": fornecedores,
                "fornecimentos": fornecimentos,
                "form": form,
            },
        )

    def post(self, request):
        fornecedor_id = request.POST.get("fornecedor_id")
        avaliacao = request.POST.get("avaliacao")
        if fornecedor_id and avaliacao:
            Fornecedor.objects.raw(
                "UPDATE Fornecedor SET avaliacao = %s WHERE id_fornecedor = %s",
                [float(avaliacao), fornecedor_id],
            )
            return redirect("fornecedores")


class ComprarMateriaPrimaView(View):
    def get(self, request, pk):
        materiaprima = list(
            MateriaPrima.objects.raw(
                """
                   SELECT *
                   FROM MateriaPrima
                   WHERE id_materiaprima = %s
                """,
                [pk],
            )
        )[0]

        fornecimentos_query = """
            SELECT Fornece.*, Fornecedor.*
            FROM Fornece
                JOIN Fornecedor ON Fornece.fornecedor_id = Fornecedor.id_fornecedor
            WHERE Fornece.materiaprima_id = %s
            ORDER BY Fornece.preco, Fornecedor.avaliacao DESC
        """
        fornecimentos = Fornece.objects.raw(fornecimentos_query, [pk])

        default_quantity = (
            max(materiaprima.limite_estoque_baixo - materiaprima.estoque_disponivel, 0)
            if materiaprima.estoque_disponivel < materiaprima.limite_estoque_baixo
            else ""
        )

        return render(
            request,
            "comprar_materiaprima.html",
            {
                "materia": materiaprima,
                "fornecimentos": fornecimentos,
                "default_quantity": default_quantity,
            },
        )

    def post(self, request, pk):
        quantidade = int(request.POST.get("quantidade"))

        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE MateriaPrima
                   SET estoque_disponivel = estoque_disponivel + %s
                   WHERE id_materiaprima = %s""",
                [quantidade, pk],
            )

        return redirect("comprar_materiaprima", pk=pk)


class OrdemProducaoView(View):
    def get(self, request):
        form = OrdemSearchForm(request.GET)

        query_filters = []
        query_params = []

        base_query = """
            SELECT *
            FROM OrdemProducao
        """

        if form.is_valid():
            if form.cleaned_data.get("id_ordem"):
                query_filters.append("id_ordem = %s")
                query_params.append(form.cleaned_data["id_ordem"])
            if form.cleaned_data.get("status"):
                query_filters.append("status LIKE %s")
                query_params.append(f"%{form.cleaned_data['status']}%")

            data_criacao_start_date = form.cleaned_data.get("data_criacao_start_date")
            data_criacao_end_date = form.cleaned_data.get("data_criacao_end_date")
            if data_criacao_start_date and data_criacao_end_date:
                query_filters.append("data_criacao BETWEEN %s AND %s")
                query_params.extend([data_criacao_start_date, data_criacao_end_date])
            elif data_criacao_start_date:
                query_filters.append("data_criacao >= %s")
                query_params.append(data_criacao_start_date)
            elif data_criacao_end_date:
                query_filters.append("data_criacao <= %s")
                query_params.append(data_criacao_end_date)

            data_conclusao_start_date = form.cleaned_data.get(
                "data_conclusao_start_date"
            )
            data_conclusao_end_date = form.cleaned_data.get("data_conclusao_end_date")
            if data_conclusao_start_date and data_conclusao_end_date:
                query_filters.append("data_conclusao BETWEEN %s AND %s")
                query_params.extend(
                    [data_conclusao_start_date, data_conclusao_end_date]
                )
            elif data_conclusao_start_date:
                query_filters.append("data_conclusao >= %s")
                query_params.append(data_conclusao_start_date)
            elif data_conclusao_end_date:
                query_filters.append("data_conclusao <= %s")
                query_params.append(data_conclusao_end_date)

            custo_total_min = form.cleaned_data.get("custo_total_min")
            custo_total_max = form.cleaned_data.get("custo_total_max")
            if custo_total_min is not None:
                query_filters.append("custo_total >= %s")
                query_params.append(custo_total_min)
            if custo_total_max is not None:
                query_filters.append("custo_total <= %s")
                query_params.append(custo_total_max)

        if query_filters:
            filtered_query = f"{base_query} WHERE {' AND '.join(query_filters)} ORDER BY status DESC, data_criacao"
        else:
            filtered_query = f"{base_query} ORDER BY status DESC, data_criacao"

        ordens = OrdemProducao.objects.raw(filtered_query, query_params)

        funcionario_nome = form.cleaned_data.get("funcionario_nome")
        funcionario_cargo = form.cleaned_data.get("funcionario_cargo")
        dados_ordens = []

        for ordem in ordens:
            produtos_query = """
                SELECT ContemOrdemProducao.*, Produto.*
                FROM ContemOrdemProducao
                    JOIN Produto ON ContemOrdemProducao.produto_id = Produto.id_produto
                WHERE ContemOrdemProducao.ordem_id = %s
            """
            produto_filters = []
            produto_params = [ordem.id_ordem]

            if form.cleaned_data.get("produto_nome"):
                produto_filters.append("Produto.nome LIKE %s")
                produto_params.append(f"%{form.cleaned_data['produto_nome']}%")

            produto_quantidade_min = form.cleaned_data.get("produto_quantidade_min")
            produto_quantidade_max = form.cleaned_data.get("produto_quantidade_max")
            if produto_quantidade_min and produto_quantidade_max:
                produto_filters.append(
                    "ContemOrdemProducao.quantidade BETWEEN %s AND %s"
                )
                produto_params.extend([produto_quantidade_min, produto_quantidade_max])
            elif produto_quantidade_min:
                produto_filters.append("ContemOrdemProducao.quantidade >= %s")
                produto_params.append(produto_quantidade_min)
            elif produto_quantidade_max:
                produto_filters.append("ContemOrdemProducao.quantidade <= %s")
                produto_params.append(produto_quantidade_max)

            if produto_filters:
                produtos_query += " AND " + " AND ".join(produto_filters)

            produtos = ContemOrdemProducao.objects.raw(produtos_query, produto_params)

            funcionarios_query = """
                SELECT Funcionario.*
                FROM Funcionario
                    JOIN Realiza ON Funcionario.id_funcionario = Realiza.funcionario_id
                WHERE Realiza.ordem_id = %s
            """
            funcionario_params = [ordem.id_ordem]

            if funcionario_nome:
                funcionarios_query += " AND Funcionario.nome LIKE %s"
                funcionario_params.append(f"%{funcionario_nome}%")
            if funcionario_cargo:
                funcionarios_query += " AND Funcionario.cargo LIKE %s"
                funcionario_params.append(f"%{funcionario_cargo}%")

            funcionarios = Funcionario.objects.raw(
                funcionarios_query, funcionario_params
            )

            if funcionarios and produtos:
                dados_ordens.append(
                    {
                        "ordem": ordem,
                        "funcionarios": funcionarios,
                        "produtos": produtos,
                    }
                )

        return render(
            request,
            "ordens_producao.html",
            {
                "dados_ordens": dados_ordens,
                "form": form,
            },
        )
