-- Tabela Cliente
CREATE TABLE Cliente (
    ID_Cliente SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Telefone VARCHAR(15) NOT NULL,
    Email VARCHAR(50) NOT NULL CHECK (EMAIL LIKE '%@%.%'),
    Numero INT NOT NULL CHECK (Numero >= 0),
    CEP VARCHAR(9) NOT NULL CHECK (CEP LIKE '_____-___'),
    Complemento VARCHAR(100),
    Logradouro VARCHAR(100)
);

-- Tabela Pedido
CREATE TABLE Pedido (
    ID_Pedido SERIAL PRIMARY KEY,
    Data_Pedido DATE NOT NULL CHECK (Data_Pedido <= CURRENT_DATE),
    Data_Entrega DATE CHECK (Data_Entrega >= Data_Pedido AND Data_Entrega >= Data_Pagamento AND Data_Entrega <= CURRENT_DATE),
    Status VARCHAR(20) NOT NULL CHECK (STATUS IN ('Pendente', 'Processado', 'Entregue')),
    Forma_Pagamento VARCHAR(20) NOT NULL CHECK (Forma_Pagamento IN ('Cartão de Crédito', 'Cartão de Débito', 'Dinheiro', 'Pix')),
    Data_Pagamento DATE NOT NULL CHECK (Data_Pagamento >= Data_Pedido AND Data_Pagamento <= CURRENT_DATE),
    Cliente_ID INT,
    FOREIGN KEY (Cliente_ID) REFERENCES Cliente(ID_Cliente) ON DELETE CASCADE
);

-- Tabela Produto
CREATE TABLE Produto (
    ID_Produto SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Descricao TEXT,
    Estoque_Disponivel INT DEFAULT 0,
    Limite_Estoque_Baixo INT DEFAULT 0,
    Custo_Unitario DECIMAL(10, 2) NOT NULL CHECK (Custo_Unitario >= 0)
);

-- Tabela Contém (relacionamento entre Pedido e Produto)
CREATE TABLE Contem (
    ID SERIAL PRIMARY KEY, -- O Django nao suporta chaves primarias compostas
    Pedido_ID INT,
    Produto_ID INT,
    Quantidade INT NOT NULL CHECK (Quantidade > 0),
    FOREIGN KEY (Pedido_ID) REFERENCES Pedido(ID_Pedido) ON DELETE CASCADE,
    FOREIGN KEY (Produto_ID) REFERENCES Produto(ID_Produto) ON DELETE CASCADE
);

-- Tabela Ordem de Produção
CREATE TABLE OrdemProducao (
    ID_Ordem SERIAL PRIMARY KEY,
    Status VARCHAR(20) NOT NULL CHECK (Status IN ('Pendente', 'Concluído')),
    Custo_Total DECIMAL(10, 2) CHECK (Custo_Total >= 0),
    Data_Criacao DATE NOT NULL CHECK (Data_Criacao <= CURRENT_DATE),
    Data_Conclusao DATE CHECK (Data_Conclusao >= Data_Criacao AND Data_Conclusao <= CURRENT_DATE)
);

-- Tabela Contém (relacionamento entre Produto e Ordem de Produção)
CREATE TABLE ContemOrdemProducao (
    ID SERIAL PRIMARY KEY, -- O Django nao suporta chaves primarias compostas
    Produto_ID INT,
    Ordem_ID INT,
    Quantidade INT NOT NULL CHECK (Quantidade > 0),
    FOREIGN KEY (Produto_ID) REFERENCES Produto(ID_Produto) ON DELETE CASCADE,
    FOREIGN KEY (Ordem_ID) REFERENCES OrdemProducao(ID_Ordem) ON DELETE CASCADE
);

-- Tabela Matéria-Prima
CREATE TABLE MateriaPrima (
    ID_MateriaPrima SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Custo_Unidade DECIMAL(10, 2) NOT NULL CHECK (Custo_Unidade >= 0),
    Estoque_Disponivel INT DEFAULT 0,
    Limite_Estoque_Baixo INT DEFAULT 0
);

-- Tabela Constituido (relacionamento entre Produto e Materia-Prima)
CREATE TABLE Constituido (
    ID SERIAL PRIMARY KEY, -- O Django nao suporta chaves primarias compostas
    Produto_ID INT,
    MateriaPrima_ID INT,
    Quantidade INT NOT NULL CHECK (Quantidade > 0),
    FOREIGN KEY (Produto_ID) REFERENCES Produto(ID_Produto) ON DELETE CASCADE,
    FOREIGN KEY (MateriaPrima_ID) REFERENCES MateriaPrima(ID_MateriaPrima) ON DELETE CASCADE
);

-- Tabela Fornecedor
CREATE TABLE Fornecedor (
    ID_Fornecedor SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Avaliacao DECIMAL(3, 2) CHECK (AVALIACAO BETWEEN 0 AND 5),
    Telefone VARCHAR(15) NOT NULL,
    Email VARCHAR(50) NOT NULL CHECK (EMAIL LIKE '%@%.%')
);

-- Tabela Fornece (relacionamento entre Fornecedor e Materia-Prima)
CREATE TABLE Fornece (
    ID SERIAL PRIMARY KEY, -- O Django nao suporta chaves primarias compostas
    Fornecedor_ID INT,
    MateriaPrima_ID INT,
    Preco INT NOT NULL,
    FOREIGN KEY (Fornecedor_ID) REFERENCES Fornecedor(ID_Fornecedor) ON DELETE CASCADE,
    FOREIGN KEY (MateriaPrima_ID) REFERENCES MateriaPrima(ID_MateriaPrima) ON DELETE CASCADE
);

-- Tabela Funcionário
CREATE TABLE Funcionario (
    ID_Funcionario SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Cargo VARCHAR(50) NOT NULL,
    Salario DECIMAL(10, 2) NOT NULL CHECK (Salario > 0)
);

-- Tabela Recebe (relacionamento entre Funcionário e Pedido)
CREATE TABLE Recebe (
    ID SERIAL PRIMARY KEY, -- O Django nao suporta chaves primarias compostas
    Funcionario_ID INT,
    Pedido_ID INT,
    FOREIGN KEY (Funcionario_ID) REFERENCES Funcionario(ID_Funcionario) ON DELETE CASCADE,
    FOREIGN KEY (Pedido_ID) REFERENCES Pedido(ID_Pedido) ON DELETE CASCADE
);

-- Tabela Realiza (relacionamento entre Funcionário e Ordem de Produção)
CREATE TABLE Realiza (
    ID SERIAL PRIMARY KEY, -- O Django nao suporta chaves primarias compostas
    Funcionario_ID INT,
    Ordem_ID INT,
    FOREIGN KEY (Funcionario_ID) REFERENCES Funcionario(ID_Funcionario) ON DELETE CASCADE,
    FOREIGN KEY (Ordem_ID) REFERENCES OrdemProducao(ID_Ordem) ON DELETE CASCADE
);

INSERT INTO Cliente (Nome, Telefone, Email, Numero, CEP, Complemento, Logradouro) VALUES
('Alice Silva', '11987654321', 'alice@example.com', 101, '01001-000', 'Apto 10', 'Rua A'),
('Bruno Souza', '21987654321', 'bruno@example.com', 102, '02002-000', 'Casa', 'Rua B'),
('Carla Mendes', '31987654321', 'carla@example.com', 103, '03003-000', 'Casa', 'Rua C'),
('Diego Costa', '41987654321', 'diego@example.com', 104, '04004-000', 'Apto 20', 'Rua D'),
('Elisa Santos', '51987654321', 'elisa@example.com', 105, '05005-000', 'Apto 30', 'Rua E'),
('Fabio Lima', '61987654321', 'fabio@example.com', 106, '06006-000', 'Casa', 'Rua F'),
('Gabriela Rocha', '71987654321', 'gabriela@example.com', 107, '07007-000', 'Casa', 'Rua G'),
('Henrique Alves', '81987654321', 'henrique@example.com', 108, '08008-000', 'Apto 40', 'Rua H'),
('Isabela Pereira', '91987654321', 'isabela@example.com', 109, '09009-000', 'Apto 50', 'Rua I'),
('João Ferreira', '10198765432', 'joao@example.com', 110, '10010-000', 'Casa', 'Rua J'),
('Laura Ribeiro', '11198765432', 'laura@example.com', 111, '11011-000', 'Casa', 'Rua K'),
('Marco Xavier', '12198765432', 'marco@example.com', 112, '12012-000', 'Apto 60', 'Rua L'),
('Natalia Martins', '13198765432', 'natalia@example.com', 113, '13013-000', 'Casa', 'Rua M'),
('Oscar Teixeira', '14198765432', 'oscar@example.com', 114, '14014-000', 'Apto 70', 'Rua N'),
('Patricia Oliveira', '15198765432', 'patricia@example.com', 115, '15015-000', 'Casa', 'Rua O'),
('Quintino Barreto', '16198765432', 'quintino@example.com', 116, '16016-000', 'Casa', 'Rua P'),
('Renata Gomes', '17198765432', 'renata@example.com', 117, '17017-000', 'Apto 80', 'Rua Q'),
('Sergio Faria', '18198765432', 'sergio@example.com', 118, '18018-000', 'Casa', 'Rua R'),
('Tania Barros', '19198765432', 'tania@example.com', 119, '19019-000', 'Apto 90', 'Rua S'),
('Ulysses Silva', '20198765432', 'ulysses@example.com', 120, '20020-000', 'Casa', 'Rua T');

INSERT INTO Pedido (Data_Pedido, Data_Entrega, Status, Forma_Pagamento, Data_Pagamento, Cliente_ID) VALUES
('2024-10-01', '2024-10-05', 'Entregue', 'Cartão de Crédito', '2024-10-05', 1),
('2024-10-02', '2024-10-06', 'Entregue', 'Cartão de Débito', '2024-10-06', 2),
('2024-10-03', '2024-10-07', 'Entregue', 'Cartão de Crédito', '2024-10-07', 3),
('2024-10-04', '2024-10-08', 'Entregue', 'Dinheiro', '2024-10-08', 4),
('2024-10-05', '2024-10-09', 'Entregue', 'Cartão de Crédito', '2024-10-09', 5),
('2024-10-06', '2024-10-10', 'Entregue', 'Cartão de Débito', '2024-10-10', 6),
('2024-10-07', '2024-10-11', 'Entregue', 'Cartão de Crédito', '2024-10-11', 7),
('2024-10-08', '2024-10-12', 'Entregue', 'Dinheiro', '2024-10-12', 8),
('2024-10-09', '2024-10-13', 'Entregue', 'Cartão de Crédito', '2024-10-13', 9),
('2024-10-10', '2024-10-14', 'Entregue', 'Cartão de Débito', '2024-10-14', 10),
('2024-11-11', '2024-11-15', 'Entregue', 'Cartão de Crédito', '2024-11-11', 11),
('2024-11-12', '2024-11-16', 'Entregue', 'Dinheiro', '2024-11-12', 12),
('2024-11-13', '2024-11-17', 'Entregue', 'Cartão de Crédito', '2024-11-13', 13),
('2024-11-14', '2024-11-18', 'Entregue', 'Cartão de Débito', '2024-11-14', 14),
('2024-11-15', '2024-11-19', 'Entregue', 'Cartão de Crédito', '2024-11-15', 15),
('2024-11-16', '2024-11-20', 'Entregue', 'Dinheiro', '2024-11-16', 16),
('2024-11-17', '2024-11-21', 'Entregue', 'Cartão de Crédito', '2024-11-17', 17),
('2024-11-18', '2024-11-22', 'Entregue', 'Cartão de Débito', '2024-11-18', 18),
('2024-11-19', '2024-11-23', 'Entregue', 'Cartão de Crédito', '2024-11-19', 19),
('2024-11-20', '2024-11-24', 'Entregue', 'Dinheiro', '2024-11-20', 20);

INSERT INTO Produto (Nome, Descricao, Estoque_Disponivel, Limite_Estoque_baixo, Custo_Unitario) VALUES
('Produto A', 'Descrição A', 100, 100, 10.00),
('Produto B', 'Descrição B', 200, 100, 15.00),
('Produto C', 'Descrição C', 150, 100, 12.00),
('Produto D', 'Descrição D', 80, 100, 20.00),
('Produto E', 'Descrição E', 100, 60, 25.00),
('Produto F', 'Descrição F', 90, 100, 18.00),
('Produto G', 'Descrição G', 70, 100, 22.00),
('Produto H', 'Descrição H', 110, 100, 19.00),
('Produto I', 'Descrição I', 130, 100, 17.00),
('Produto J', 'Descrição J', 120, 100, 14.00),
('Produto K', 'Descrição K', 140, 100, 16.00),
('Produto L', 'Descrição L', 50, 100, 30.00),
('Produto M', 'Descrição M', 40, 100, 28.00),
('Produto N', 'Descrição N', 200, 100, 26.00),
('Produto O', 'Descrição O', 180, 100, 24.00),
('Produto P', 'Descrição P', 160, 100, 23.00),
('Produto Q', 'Descrição Q', 170, 100, 22.00),
('Produto R', 'Descrição R', 80, 100, 21.00),
('Produto S', 'Descrição S', 100, 100, 27.00),
('Produto T', 'Descrição T', 50, 100, 29.00);

INSERT INTO Contem (Pedido_ID, Produto_ID, Quantidade) VALUES
(1, 1, 5),
(2, 2, 10),
(3, 3, 15),
(4, 4, 20),
(5, 5, 25),
(6, 6, 30),
(7, 7, 35),
(8, 8, 40),
(9, 9, 45),
(10, 10, 50),
(11, 11, 55),
(12, 12, 60),
(13, 13, 65),
(14, 14, 70),
(15, 15, 75),
(16, 16, 80),
(17, 17, 85),
(18, 18, 90),
(19, 19, 95),
(20, 20, 100);

INSERT INTO OrdemProducao (Status, Custo_Total, Data_Criacao, Data_Conclusao) VALUES
('Concluído', 500.00, '2024-01-01', '2024-01-10'),
('Concluído', 600.00, '2024-02-01', '2024-02-10'),
('Concluído', 700.00, '2024-03-01', '2024-03-10'),
('Concluído', 800.00, '2024-04-01', '2024-04-10'),
('Concluído', 900.00, '2024-05-01', '2024-05-10'),
('Concluído', 1000.00, '2024-06-01', '2024-06-10'),
('Concluído', 1100.00, '2024-07-01', '2024-07-10'),
('Concluído', 1200.00, '2024-08-01', '2024-08-10'),
('Concluído', 1300.00, '2024-09-01', '2024-09-10'),
('Concluído', 1400.00, '2024-10-01', '2024-10-10'),
('Concluído', 1500.00, '2024-11-01', '2024-11-10'),
('Concluído', 1600.00, '2024-11-02', '2024-11-11'),
('Concluído', 1700.00, '2024-01-01', '2024-01-10'),
('Concluído', 1800.00, '2024-02-01', '2024-02-10'),
('Concluído', 1900.00, '2024-03-01', '2024-03-10'),
('Concluído', 2000.00, '2024-04-01', '2024-04-10'),
('Concluído', 2100.00, '2024-05-01', '2024-05-10'),
('Concluído', 2200.00, '2024-06-01', '2024-06-10'),
('Concluído', 2300.00, '2024-07-01', '2024-07-10'),
('Concluído', 2400.00, '2024-08-01', '2024-08-10');

INSERT INTO ContemOrdemProducao (Produto_ID, Ordem_ID, Quantidade) VALUES
(1, 1, 10),
(2, 2, 20),
(3, 3, 30),
(4, 4, 40),
(5, 5, 50),
(6, 6, 60),
(7, 7, 70),
(8, 8, 80),
(9, 9, 90),
(10, 10, 100),
(11, 11, 110),
(12, 12, 120),
(13, 13, 130),
(14, 14, 140),
(15, 15, 150),
(16, 16, 160),
(17, 17, 170),
(18, 18, 180),
(19, 19, 190),
(20, 20, 200);

INSERT INTO MateriaPrima (Nome, Custo_Unidade, Estoque_Disponivel, Limite_Estoque_baixo) VALUES
('Matéria-Prima A', 5.00, 100, 1000),
('Matéria-Prima B', 6.00, 200, 1000),
('Matéria-Prima C', 7.00, 300, 1000),
('Matéria-Prima D', 8.00, 400, 1000),
('Matéria-Prima E', 9.00, 500, 1000),
('Matéria-Prima F', 10.00, 600, 1000),
('Matéria-Prima G', 11.00, 700, 1000),
('Matéria-Prima H', 12.00, 800, 1000),
('Matéria-Prima I', 13.00, 900, 1000),
('Matéria-Prima J', 14.00, 1000, 1000),
('Matéria-Prima K', 15.00, 1100, 1000),
('Matéria-Prima L', 16.00, 1200, 1000),
('Matéria-Prima M', 17.00, 1300, 1000),
('Matéria-Prima N', 18.00, 1400, 1000),
('Matéria-Prima O', 19.00, 1500, 1000),
('Matéria-Prima P', 20.00, 1600, 1000),
('Matéria-Prima Q', 21.00, 1700, 1000),
('Matéria-Prima R', 22.00, 1800, 1000),
('Matéria-Prima S', 23.00, 1900, 1000),
('Matéria-Prima T', 24.00, 2000, 1000);

INSERT INTO Constituido (Produto_ID, MateriaPrima_ID, Quantidade) VALUES
(1, 1, 50),
(2, 2, 60),
(3, 3, 70),
(4, 4, 80),
(5, 5, 90),
(6, 6, 100),
(7, 7, 110),
(8, 8, 120),
(9, 9, 130),
(10, 10, 140),
(11, 11, 150),
(12, 12, 160),
(13, 13, 170),
(14, 14, 180),
(15, 15, 190),
(16, 16, 200),
(17, 17, 210),
(18, 18, 220),
(19, 19, 230),
(20, 20, 240);

INSERT INTO Fornecedor (Nome, Avaliacao, Telefone, Email) VALUES
('Fornecedor A', 4.5, '11987654321', 'fornecedora@example.com'),
('Fornecedor B', 4.6, '21987654321', 'fornecedorb@example.com'),
('Fornecedor C', 4.7, '31987654321', 'fornecedorc@example.com'),
('Fornecedor D', 4.8, '41987654321', 'fornecedord@example.com'),
('Fornecedor E', 4.9, '51987654321', 'fornecedore@example.com'),
('Fornecedor F', 4.3, '61987654321', 'fornecedorf@example.com'),
('Fornecedor G', 4.1, '71987654321', 'fornecedorg@example.com'),
('Fornecedor H', 4.0, '81987654321', 'fornecedorh@example.com'),
('Fornecedor I', 3.9, '91987654321', 'fornecedori@example.com'),
('Fornecedor J', 3.8, '10198765432', 'fornecedorj@example.com'),
('Fornecedor K', 3.7, '11198765432', 'fornecedork@example.com'),
('Fornecedor L', 3.6, '12198765432', 'fornecedorl@example.com'),
('Fornecedor M', 3.5, '13198765432', 'fornecedorm@example.com'),
('Fornecedor N', 3.4, '14198765432', 'fornecedorn@example.com'),
('Fornecedor O', 3.3, '15198765432', 'fornecedoro@example.com'),
('Fornecedor P', 3.2, '16198765432', 'fornecedorp@example.com'),
('Fornecedor Q', 3.1, '17198765432', 'fornecedorq@example.com'),
('Fornecedor R', 3.0, '18198765432', 'fornecedorr@example.com'),
('Fornecedor S', 2.9, '19198765432', 'fornecedors@example.com'),
('Fornecedor T', 2.8, '20198765432', 'fornecedort@example.com');

INSERT INTO Fornece (Fornecedor_ID, MateriaPrima_ID, Preco) VALUES
(1, 1, 100),
(2, 2, 200),
(3, 3, 300),
(4, 4, 400),
(5, 5, 500),
(6, 6, 600),
(7, 7, 700),
(8, 8, 800),
(9, 9, 900),
(10, 10, 1000),
(11, 11, 1100),
(12, 12, 1200),
(13, 13, 1300),
(14, 14, 1400),
(15, 15, 1500),
(16, 16, 1600),
(17, 17, 1700),
(18, 18, 1800),
(19, 19, 1900),
(20, 20, 2000);

INSERT INTO Funcionario (Nome, Cargo, Salario) VALUES
('Funcionario A', 'Cargo A', 5000.00),
('Funcionario B', 'Cargo B', 3000.00),
('Funcionario C', 'Cargo C', 2500.00),
('Funcionario D', 'Cargo D', 4500.00),
('Funcionario E', 'Cargo E', 2000.00),
('Funcionario F', 'Cargo F', 3500.00),
('Funcionario G', 'Cargo G', 4000.00),
('Funcionario H', 'Cargo H', 4800.00),
('Funcionario I', 'Cargo I', 1500.00),
('Funcionario J', 'Cargo J', 5500.00),
('Funcionario K', 'Cargo K', 3000.00),
('Funcionario L', 'Cargo L', 6000.00),
('Funcionario M', 'Cargo M', 4200.00),
('Funcionario N', 'Cargo N', 2500.00),
('Funcionario O', 'Cargo O', 2200.00),
('Funcionario P', 'Cargo P', 2000.00),
('Funcionario Q', 'Cargo Q', 4600.00),
('Funcionario R', 'Cargo R', 5200.00),
('Funcionario S', 'Cargo S', 3800.00),
('Funcionario T', 'Cargo T', 4500.00);

INSERT INTO Recebe (Funcionario_ID, Pedido_ID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15),
(16, 16),
(17, 17),
(18, 18),
(19, 19),
(20, 20);

INSERT INTO Realiza (Funcionario_ID, Ordem_ID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15),
(16, 16),
(17, 17),
(18, 18),
(19, 19),
(20, 20);
