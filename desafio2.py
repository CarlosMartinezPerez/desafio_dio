import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    saldo = 0
    quant_saques = 0
    lim_sq_dia = 500
    extrato = ""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)


    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "saldo": saldo, "quant_saques": quant_saques, 
                "lim_sq_dia": lim_sq_dia, "extrato": extrato, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def escolher_conta(contas):
    print("Escolha a conta:")
    for i, conta in enumerate(contas):
        print(f"{i + 1}. Conta {conta['numero_conta']} - {conta['usuario']['cpf']} - {conta['usuario']['nome']}")
    
    escolha = input("Informe o número da conta ou '0' para voltar ao menu principal: ")
    if escolha == "0":
        return None
    
    try:
        indice_conta = int(escolha) - 1
        return contas[indice_conta]
    except (ValueError, IndexError):
        print("\n@@@ Opção inválida! @@@")
        return None


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(f"Seu depósito de R$ {valor} foi realizado com sucesso!")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, quant_saques, lim_sq_dia,):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > lim_sq_dia
    excedeu_saques = quant_saques >= 3

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite de saque diário. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        quant_saques += 1
        lim_sq_dia -= valor
        print(f"Seu saque de R$ {valor} foi realizado com sucesso!")
        
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return(saldo, extrato, quant_saques, lim_sq_dia)
    

def exibir_extrato(saldo, quant_saques, lim_sq_dia, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}\n")
    if lim_sq_dia > 0:
        print(f"Você ainda pode sacar R$ {lim_sq_dia} hoje!")
    else:
        print("Você excedeu o valor máximo de retirada hoje!")
    
    saques_disp = 3 - quant_saques
    if saques_disp > 0:
        print(f"Você ainda tem {saques_disp} saques disponíveis hoje!")
    else:
        print("Você não tem mais saques disponíveis hoje!")
    
    print("\nBanco X - SEMPRE A SEU DISPOR!")
    print("==========================================")


def main():
 
    AGENCIA = "0001"
    usuarios = []
    contas = []
    

    while True:
        opcao = menu()

        if opcao == "nu":
           criar_usuario(usuarios)
        

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
             
        
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break


        elif opcao in ["d", "s", "e"]:
            conta_escolhida = escolher_conta(contas)

            
            
            if conta_escolhida:
                if opcao == "d":
                    valor = float(input("Informe o valor do depósito: "))
                    conta_escolhida["saldo"], conta_escolhida["extrato"] = depositar(
                        conta_escolhida["saldo"], valor, conta_escolhida["extrato"])
                    

                elif opcao == "s":
                    valor = round(float(input("Informe o valor do saque: ")), 2)
                    conta_escolhida["saldo"], conta_escolhida["extrato"], conta_escolhida["quant_saques"], conta_escolhida["lim_sq_dia"] = sacar(
                    saldo=conta_escolhida["saldo"],
                    valor=valor,
                    extrato=conta_escolhida["extrato"],
                    quant_saques=conta_escolhida["quant_saques"],
                    lim_sq_dia=conta_escolhida["lim_sq_dia"])

                    
                elif opcao == "e":
                    exibir_extrato(conta_escolhida["saldo"], conta_escolhida["quant_saques"], conta_escolhida["lim_sq_dia"], extrato=conta_escolhida["extrato"])
            else:
                print("\n@@@ Conta não encontrada! @@@")
                continue

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()