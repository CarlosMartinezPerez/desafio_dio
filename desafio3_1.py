from datetime import date

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao:
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(f'Depósito de R$ {self.valor:.2f}')
        return True

class Saque(Transacao):
    def registrar(self, conta):
        if conta.saldo >= self.valor:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(f'Saque de R$ {self.valor:.2f}')
            return True
        return False

class Conta:
    def __init__(self, cliente, numero, agencia):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def nova_conta(self, cliente, numero):
        return Conta(cliente, numero, self.agencia)

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saques):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Exemplo de uso
cliente = PessoaFisica("12345678900", "João da Silva", date(1990, 1, 1), "Rua A, 123")
conta = ContaCorrente(cliente, 1, "001", 1000, 3)
cliente.adicionar_conta(conta)

print("Depósito:", cliente.realizar_transacao(conta, Deposito(500)))
print("Saque:", cliente.realizar_transacao(conta, Saque(200)))
print("Saldo:", conta.saldo)

for transacao in conta.historico.transacoes:
    print(transacao)
