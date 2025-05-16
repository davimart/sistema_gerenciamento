from django.core.validators import MinValueValidator, RegexValidator
from django.db import connection, models, transaction
from django.db.models import CheckConstraint, Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^[\w\.-]+@[\w\.-]+\.\w+$",
                message="Insira um email válido.",
            )
        ],
    )
    numero = models.IntegerField(
        validators=[
            MinValueValidator(0, message="Insira um número maior ou igual a 0.")
        ]
    )
    cep = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r"^\d{5}-\d{3}$",
                message="Insira um CEP válido.",
            )
        ],
    )
    complemento = models.CharField(max_length=100, blank=True, null=True)
    logradouro = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "cliente"
        verbose_name_plural = "Clientes"


class Pedido(models.Model):
    PENDENTE = "Pendente"
    PROCESSADO = "Processado"
    ENTREGUE = "Entregue"
    STATUS_CHOICES = [
        (PENDENTE, "Pendente"),
        (PROCESSADO, "Processado"),
        (ENTREGUE, "Entregue"),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ("Cartão de Crédito", "Cartão de Crédito"),
        ("Cartão de Débito", "Cartão de Débito"),
        ("Dinheiro", "Dinheiro"),
        ("Pix", "Pix"),
    ]

    id_pedido = models.AutoField(primary_key=True)
    data_pedido = models.DateField()
    data_entrega = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    data_pagamento = models.DateField()
    cliente = models.ForeignKey(
        "Cliente", on_delete=models.CASCADE, related_name="pedidos"
    )

    def __str__(self):
        return f"Pedido {self.id_pedido} feito por {self.cliente} - {self.status}"

    class Meta:
        db_table = "pedido"
        verbose_name_plural = "Pedidos"
        constraints = [
            CheckConstraint(
                check=Q(data_pedido__lte=models.functions.Now()),
                name="check_pedido_data_pedido_current_date",
            ),
            CheckConstraint(
                check=Q(data_entrega__gte=models.F("data_pedido"))
                & Q(data_entrega__gte=models.F("data_pagamento"))
                & Q(data_entrega__lte=models.functions.Now()),
                name="check_pedido_data_entrega",
            ),
            CheckConstraint(
                check=Q(status__in=["Pendente", "Processado", "Entregue"]),
                name="check_pedido_pedido_status_valid",
            ),
            CheckConstraint(
                check=Q(
                    forma_pagamento__in=[
                        "Cartão de Crédito",
                        "Cartão de Débito",
                        "Dinheiro",
                        "Pix",
                    ]
                ),
                name="check_pedido_forma_pagamento_valid",
            ),
            CheckConstraint(
                check=Q(data_pagamento__gte=models.F("data_pedido"))
                & Q(data_pagamento__lte=models.functions.Now()),
                name="check_pedido_data_pagamento",
            ),
        ]


class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    estoque_disponivel = models.IntegerField(default=0)
    limite_estoque_baixo = models.IntegerField(default=0)
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "produto"
        verbose_name_plural = "Produtos"
        constraints = [
            models.CheckConstraint(
                check=models.Q(custo_unitario__gte=0),
                name="check_produto_custo_unitario",
            )
        ]


class Contem(models.Model):
    id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey("Pedido", on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name="pedidos"
    )
    quantidade = models.IntegerField()

    class Meta:
        db_table = "contem"
        constraints = [
            models.UniqueConstraint(
                fields=["pedido", "produto"], name="unique_pedido_produto"
            ),
            models.CheckConstraint(
                check=models.Q(quantidade__gt=0),
                name="check_contem_quantidade_positive",
            ),
        ]
        verbose_name_plural = "Contem"

    def __str__(self):
        return f"{self.quantidade} de {self.produto.nome} no Pedido {self.pedido.id_pedido}"


@receiver(post_save, sender=Pedido)
def update_estoque_pedido(sender, instance, **kwargs):
    if instance.status == Pedido.PROCESSADO:
        transaction.on_commit(lambda: reduce_produto_estoque_pedido(instance))


def reduce_produto_estoque_pedido(instance):
    with connection.cursor() as cursor:
        contem_items_query = """
            SELECT Contem.id, Contem.quantidade, Contem.produto_id, Produto.estoque_disponivel
            FROM Contem
            JOIN Produto ON Contem.produto_id = Produto.id_produto
            WHERE Contem.pedido_id = %s
        """
        cursor.execute(contem_items_query, [instance.id_pedido])
        contem_items = cursor.fetchall()

        for item in contem_items:
            item_id, quantidade, produto_id, estoque_disponivel = item
            new_estoque_disponivel = estoque_disponivel - quantidade

            update_produto_query = """
                UPDATE Produto
                SET estoque_disponivel = %s
                WHERE id_produto = %s
            """
            cursor.execute(update_produto_query, [new_estoque_disponivel, produto_id])


class OrdemProducao(models.Model):
    PENDENTE = "Pendente"
    CONCLUIDO = "Concluído"
    STATUS_CHOICES = [
        (PENDENTE, "Pendente"),
        (CONCLUIDO, "Concluído"),
    ]

    id_ordem = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False)
    custo_total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    data_criacao = models.DateField(null=False)
    data_conclusao = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Ordem {self.id_ordem} - {self.status}"

    class Meta:
        db_table = "ordemproducao"
        verbose_name_plural = "OrdemProducao"
        constraints = [
            CheckConstraint(
                check=Q(status__in=["Pendente", "Concluído"]),
                name="check_ordemproducao_status_valid",
            ),
            CheckConstraint(
                check=Q(custo_total__gte=0),
                name="check_ordemproducao_custo_total_non_negative",
            ),
            CheckConstraint(
                check=Q(data_criacao__lte=models.functions.Now()),
                name="check_ordemproducao_data_criacao_current_date",
            ),
            CheckConstraint(
                check=Q(data_conclusao__gte=models.F("data_criacao"))
                & Q(data_conclusao__lte=models.functions.Now()),
                name="check_ordemproducao_data_conclusao",
            ),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == self.CONCLUIDO:
            increase_produto_estoque(self)


@receiver(post_save, sender=OrdemProducao)
def update_estoque_ordem_producao(sender, instance, **kwargs):
    if instance.status == instance.CONCLUIDO:
        transaction.on_commit(lambda: increase_produto_estoque(instance))


def increase_produto_estoque(instance):
    with connection.cursor() as cursor:
        contem_ordem_producao_query = """
            SELECT produto_id, quantidade
            FROM ContemOrdemProducao
            WHERE ordem_id = %s
        """
        cursor.execute(contem_ordem_producao_query, [instance.id_ordem])
        contem_items = cursor.fetchall()

        for item in contem_items:
            produto_id, quantidade = item
            update_produto_query = """
                UPDATE Produto
                SET estoque_disponivel = estoque_disponivel + %s
                WHERE id_produto = %s
            """
            cursor.execute(update_produto_query, [quantidade, produto_id])


class ContemOrdemProducao(models.Model):
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(
        "Produto", on_delete=models.CASCADE, related_name="ordens_producao"
    )
    ordem = models.ForeignKey(
        "OrdemProducao",
        on_delete=models.CASCADE,
        related_name="contemordemproducao_set",
    )
    quantidade = models.IntegerField()

    def __str__(self):
        return (
            f"{self.quantidade} de {self.produto.nome} na Ordem {self.ordem.id_ordem}"
        )

    class Meta:
        db_table = "contemordemproducao"
        constraints = [
            models.UniqueConstraint(
                fields=["produto", "ordem"], name="unique_produto_ordem"
            ),
            models.CheckConstraint(
                check=models.Q(quantidade__gt=0),
                name="check_contemordemproducao_quantidade_positive",
            ),
        ]
        verbose_name_plural = "ContemOrdemProducao"


class MateriaPrima(models.Model):
    id_materiaprima = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    custo_unidade = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_disponivel = models.IntegerField(default=0)
    limite_estoque_baixo = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "materiaprima"
        verbose_name_plural = "MateriaPrima"
        constraints = [
            models.CheckConstraint(
                check=models.Q(custo_unidade__gte=0),
                name="check_materiaprima_custo_unidade_non_negative",
            )
        ]


class Constituido(models.Model):
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(
        "Produto", on_delete=models.CASCADE, related_name="materias_primas"
    )
    materiaprima = models.ForeignKey(
        MateriaPrima, on_delete=models.CASCADE, related_name="produtos"
    )
    quantidade = models.IntegerField()

    def __str__(self):
        return f"{self.quantidade} de {self.materiaprima.nome} para Produto {self.produto.nome}"

    class Meta:
        db_table = "constituido"
        constraints = [
            models.UniqueConstraint(
                fields=["produto", "materiaprima"], name="unique_produto_materiaprima"
            ),
            models.CheckConstraint(
                check=models.Q(quantidade__gt=0),
                name="check_constituido_quantidade_positive",
            ),
        ]
        verbose_name_plural = "Constituido"


@receiver(post_save, sender=OrdemProducao)
def update_materiaprima_estoque(sender, instance, **kwargs):
    if instance.status == OrdemProducao.PENDENTE:
        transaction.on_commit(lambda: reduce_materiaprima_estoque(instance))


def reduce_materiaprima_estoque(instance):
    with connection.cursor() as cursor:
        contem_ordem_query = """
            SELECT produto_id, quantidade
            FROM ContemOrdemProducao
            WHERE ordem_id = %s
        """
        cursor.execute(contem_ordem_query, [instance.id_ordem])
        contem_ordens = cursor.fetchall()

        for contem_ordem in contem_ordens:
            produto_id, quantidade = contem_ordem

            constituidos_query = """
                SELECT materiaprima_id, quantidade
                FROM Constituido
                WHERE produto_id = %s
            """
            cursor.execute(constituidos_query, [produto_id])
            constituidos = cursor.fetchall()

            for constituido in constituidos:
                materiaprima_id, constituido_quantidade = constituido
                total_quantity = constituido_quantidade * quantidade

                update_materiaprima_query = """
                    UPDATE MateriaPrima
                    SET estoque_disponivel = estoque_disponivel - %s
                    WHERE id_materiaprima = %s
                """
                cursor.execute(
                    update_materiaprima_query, [total_quantity, materiaprima_id]
                )


class Fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    avaliacao = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True
    )
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "fornecedor"
        verbose_name_plural = "Fornecedores"
        constraints = [
            models.CheckConstraint(
                check=models.Q(avaliacao__gte=0) & models.Q(avaliacao__lte=5),
                name="check_fornecedor_avaliacao_between_0_and_5",
            ),
            models.CheckConstraint(
                check=models.Q(email__regex=r"^[\w\.-]+@[\w\.-]+\.\w+$"),
                name="check_fornecedor_email_format",
            ),
        ]


class Fornece(models.Model):
    id = models.AutoField(primary_key=True)
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        related_name="materias_primas",
    )
    materiaprima = models.ForeignKey(
        MateriaPrima,
        on_delete=models.CASCADE,
        related_name="fornecedores",
    )
    preco = models.IntegerField()

    def __str__(self):
        return f"Fornecimento de {self.materiaprima.nome} por {self.fornecedor.nome} a R${self.preco} por unidade"

    class Meta:
        db_table = "fornece"
        constraints = [
            models.UniqueConstraint(
                fields=["fornecedor", "materiaprima"],
                name="unique_fornecedor_materiaprima",
            ),
            models.CheckConstraint(
                check=models.Q(preco__gt=0), name="check_fornece_preco_positive"
            ),
        ]
        verbose_name_plural = "Fornece"


class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nome} - {self.cargo}"

    class Meta:
        db_table = "funcionario"
        verbose_name_plural = "Funcionario"
        constraints = [
            models.CheckConstraint(
                check=models.Q(salario__gt=0), name="check_funcionario_salario_positive"
            )
        ]


class Recebe(models.Model):
    id = models.AutoField(primary_key=True)
    funcionario = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, related_name="pedidos_recebidos"
    )
    pedido = models.ForeignKey(
        "Pedido", on_delete=models.CASCADE, related_name="funcionarios_responsaveis"
    )

    def __str__(self):
        return f"Funcionário {self.funcionario.nome} vinculado ao Pedido {self.pedido.id_pedido}"

    class Meta:
        db_table = "recebe"
        constraints = [
            models.UniqueConstraint(
                fields=["funcionario", "pedido"], name="unique_funcionario_pedido"
            )
        ]
        verbose_name_plural = "Recebe"


class Realiza(models.Model):
    id = models.AutoField(primary_key=True)
    funcionario = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, related_name="ordens_realizadas"
    )
    ordem = models.ForeignKey(
        "OrdemProducao",
        on_delete=models.CASCADE,
        related_name="funcionarios_envolvidos",
    )

    def __str__(self):
        return f"Funcionário {self.funcionario.nome} envolvido na Ordem {self.ordem.id_ordem}"

    class Meta:
        db_table = "realiza"
        constraints = [
            models.UniqueConstraint(
                fields=["funcionario", "ordem"], name="unique_funcionario_ordem"
            )
        ]
        verbose_name_plural = "Realiza"
