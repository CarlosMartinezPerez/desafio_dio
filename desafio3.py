class Usuario:
    def __init__(self, nome, id_usuario, email):
        self.nome = nome
        self.id_usuario = id_usuario
        self.email = email

class ContaBancaria:
    def __init__(self, numero_conta, usuario):
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.transacoes = []

    def depositar(self, valor):
        self.saldo += valor
        self.transacoes.append(f'Depósito de {valor}')

    def sacar(self, valor):
        if len([t for t in self.transacoes if t.startswith('Saque')]) >= 3:
            print("Limite de saques diários atingido.")
            return
        elif valor > 500:
            print("Limite de saque excedido.")
            return
        elif self.saldo < valor:
            print("Saldo insuficiente.")
            return
        self.saldo -= valor
        self.transacoes.append(f'Saque de {valor}')

    def extrato(self):
        print(f"Extrato da conta {self.numero_conta}:")
        for t in self.transacoes:
            print(t)

class SistemaBancario:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def cadastrar_usuario(self, nome, id_usuario, email):
        usuario = Usuario(nome, id_usuario, email)
        self.usuarios.append(usuario)
        return usuario

    def recuperar_usuario(self, id_usuario):
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario
        return None

    def atualizar_usuario(self, id_usuario, nome=None, email=None):
        usuario = self.recuperar_usuario(id_usuario)
        if usuario:
            if nome:
                usuario.nome = nome
            if email:
                usuario.email = email
            return True
        return False

    def deletar_usuario(self, id_usuario):
        usuario = self.recuperar_usuario(id_usuario)
        if usuario:
            self.usuarios.remove(usuario)
            return True
        return False

    def abrir_conta(self, usuario):
        numero_conta = len(self.contas) + 1  # Pode ser melhorado para gerar um número único
        conta = ContaBancaria(numero_conta, usuario)
        self.contas.append(conta)
        return conta

def exibir_menu():
    print("\nMenu:")
    print("1. Cadastrar usuário")
    print("2. Recuperar usuário")
    print("3. Atualizar usuário")
    print("4. Deletar usuário")
    print("5. Abrir conta bancária")
    print("6. Depositar")
    print("7. Sacar")
    print("8. Emitir extrato")
    print("0. Sair")

def main():
    sistema = SistemaBancario()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do usuário: ")
            id_usuario = input("Digite o ID do usuário: ")
            email = input("Digite o email do usuário: ")
            sistema.cadastrar_usuario(nome, id_usuario, email)
            print("Usuário cadastrado com sucesso!")

        elif opcao == "2":
            id_usuario = input("Digite o ID do usuário a ser recuperado: ")
            usuario = sistema.recuperar_usuario(id_usuario)
            if usuario:
                print(f"Usuário encontrado: {usuario.nome}, {usuario.email}")
            else:
                print("Usuário não encontrado.")

        elif opcao == "3":
            id_usuario = input("Digite o ID do usuário a ser atualizado: ")
            nome = input("Digite o novo nome (deixe em branco para manter o mesmo): ")
            email = input("Digite o novo email (deixe em branco para manter o mesmo): ")
            if sistema.atualizar_usuario(id_usuario, nome, email):
                print("Usuário atualizado com sucesso!")
            else:
                print("Usuário não encontrado.")

        elif opcao == "4":
            id_usuario = input("Digite o ID do usuário a ser deletado: ")
            if sistema.deletar_usuario(id_usuario):
                print("Usuário deletado com sucesso!")
            else:
                print("Usuário não encontrado.")

        elif opcao == "5":
            id_usuario = input("Digite o ID do usuário para abrir a conta bancária: ")
            usuario = sistema.recuperar_usuario(id_usuario)
            if usuario:
                conta = sistema.abrir_conta(usuario)
                print(f"Conta bancária aberta com sucesso! Número da conta: {conta.numero_conta}")
            else:
                print("Usuário não encontrado.")

        elif opcao == "6":
            # Implemente a lógica de depósito
            pass

        elif opcao == "7":
            # Implemente a lógica de saque
            pass

        elif opcao == "8":
            # Implemente a lógica de emissão de extrato
            pass

        elif opcao == "0":
            print("Obrigado por usar o sistema bancário. Até mais!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
