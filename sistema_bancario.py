saldo = 0
extrato = ""
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opção = input("[d]Depósito\n[s]Saque\n[e]Extrato\n[q]Sair\nDigite:")

    if opção == "d":
        depositar = float(input("Digite o valor para depositar: "))

        if depositar < 0:
            print("[ERRO] Digite um valor válido!")

        saldo += depositar

        print("Concluído!")

        extrato += f"+R${depositar}\n"


    elif opção == "s":
        print(f"Seu número de saques diários é de {numero_saques}, lembre-se, você pode sacar no máximo 3 vezes ao dia!")

        if numero_saques == LIMITE_SAQUES:
            print("[ERRO] Limite de saque diário excedido!")

        else:
            sacar = float(input("Digite o valor para sacar [Máximo R$500]: "))

            if sacar > saldo:
                print("[ERRO] Saldo insuficiente!")
                continue

            elif sacar > limite:
                print("[ERRO] Valor máximo excedido!")
                continue

            elif sacar <= 0:
                print("[ERRO] Por favor, insira um valor condizente!")
                continue

            else:
                saldo -= sacar
                numero_saques += 1
                print("Concluído!")

        extrato += f"-R${sacar}\n"

    elif opção == "e":
        if not extrato:
            print("Não foram realizadas movimentações!")

        else:
            print(f"\nSaldo:\nR${saldo}\n\nExtrato:\n{extrato}")
    
    elif opção == "q":
        break

    else:
        print("Opção inválida, tente novamente!")
