def depositar(saldo, valor, extrato, /):
    if valor <= 0:
        print("[ERRO] Digite um valor válido!")

    else:
        saldo += valor
        extrato += f"+R${valor}\n"
        print("Concluído!")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques == limite_saques:
        print("[ERRO] Limite de saque diário excedido!")

    else:
        if valor > saldo:
            print("[ERRO] Saldo insuficiente!")
            
        elif valor > limite:
            print("[ERRO] Valor máximo excedido!")

        elif valor <= 0:
            print("[ERRO] Por favor, insira um valor válido!")

        else:
            saldo -= valor
            numero_saques += 1
            extrato += f"-R${valor}\n"
            print("Concluído!")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    if not extrato:
       return "Não foram realizadas movimentações!"

    else:
        return f"\nSaldo:\nR${saldo}\n\nExtrato:\n{extrato}"

def cadastrar_usuario(lista_usuarios):

    nome = input("Insira o seu nome: ")
    data_nascimento = input("Insira a sua data de nascimento [dd/mm/aaaa]: ")
    cpf = input("Digite o seu cpf: ")
    endereco = input("Digite o seu endereço [Logradouro, numero - bairro - cidade/sigla do estado[Ex: QQ1, 01 - Vila Madalena - São Paulo/SP]]: ")

    eliminar_pontos_hifens = ".-"
    for caractere in eliminar_pontos_hifens:
        cpf = cpf.replace(caractere, "")

    usuario = {
        "nome": nome,
        "data de nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    
    if verificar_cpf(cpf, lista_usuarios):
        print(f"Usuário de CPF {cpf} ja cadastrado!")
    
    else:
        lista_usuarios.append(usuario)
        print(f"Usuário {nome} cadastrado com sucesso!")
        return lista_usuarios

def verificar_cpf(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
    return False

def cadastrar_conta_corrente(*, agencia, cpf, lista_conta_corrente, lista_usuarios):
    numero_conta_corrente = len(lista_conta_corrente) + 1

    if verificar_cpf(cpf, lista_usuarios): 
        conta_corrente = {
            "AGENCIA": agencia,
            "numero_conta": numero_conta_corrente,
            "usuario": cpf
        }
        lista_conta_corrente.append(conta_corrente)
        
        print(f"Conta criada com sucesso!, segue os dados de sua conta corrente: {conta_corrente}")

        return lista_conta_corrente
    else:
        while True:
            criar_conta = input("Percebemos que você ainda não possui conta no nosso banco, deseja criar uma? [S/N]")
            if criar_conta == "s".lower():
                cadastrar_usuario(lista_usuarios=lista_usuarios)
                break
            elif criar_conta == "n".lower():
                print("Ok, fechando conexão!")
                return
            else:
                continue

def listar_contas(*, cpf, lista_usuarios, lista_conta_corrente,):
    lista_contas_usuario = []

    if verificar_cpf(cpf, lista_usuarios): 
        for conta_corrente in lista_conta_corrente:
            if conta_corrente["usuario"] == cpf:
                lista_contas_usuario.append(conta_corrente)
            else:
                continue
        if not lista_contas_usuario:
            return f"Não foi encontrada nenhuma conta pertencente ao cpf {cpf}"
        else:
            return lista_contas_usuario
    else:
        while True:
            criar_conta = input("Percebemos que você ainda não possui conta no nosso banco, deseja criar uma? [S/N]")
            if criar_conta == "s".lower():
                cadastrar_usuario(lista_usuarios=lista_usuarios)
                break
            elif criar_conta == "n".lower():
                print("Ok, fechando conexão!")
                return
            else:
                continue

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    conta_corrente = []

    saldo = 0
    extrato = ""
    limite = 500
    numero_saques = 0

    while True:
        opcao = input("[d]Depósito\n[s]Saque\n[e]Extrato\n[u]Cadastrar usuário\n[cc]Criar conta corrente\n[lc]Listar as contas que possui\n[q]Sair\nDigite:")
        opcao = opcao.lower()

        if opcao == "d":
            valor = float(input("Digite o valor para depositar: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Digite o valor para sacar [Máximo R$500]: "))

            saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            extrato = exibir_extrato(saldo, extrato=extrato)
            print(extrato)

        elif opcao == "u":
            cadastrar_usuario(lista_usuarios=usuarios)

        elif opcao == "cc":
            cpf = input("Digite o seu cpf: ")
            cadastrar_conta_corrente(cpf=cpf, lista_conta_corrente=conta_corrente, lista_usuarios=usuarios, agencia=AGENCIA)

        elif opcao == "lc":
            cpf = input("Digite o seu cpf: ")
            lista_contas = listar_contas(cpf=cpf, lista_usuarios=usuarios, lista_conta_corrente=conta_corrente)
            print(lista_contas)
            
        elif opcao == "q":
            print("Fechando conexão!")
            break
        
        else:
            print("Opção inválida, tente novamente!")

main()