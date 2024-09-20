from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor
    
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        if valor > self.saldo:
            print("[ERRO] Saldo insuficiente!")
        
        elif valor <= 0:
            print("[ERRO] Por favor, insira um valor válido!")

        else:
            self.saldo -= valor
            print("Concluído!")
            return True

        return False
    
    def depositar(self, valor):
        if valor <= 0:
            print("[ERRO] Digite um valor válido!")
            return False
        else:
            self.saldo += valor
            print("Concluído!")
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500.0, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = 0
        for transacao in self._historico.transacoes:
            if transacao["tipo"] == "Saque":
                numero_saques += 1

        if numero_saques == self.limite_saques:
            print("[ERRO] Limite de saque diário excedido!")

        else:
            if valor > self.limite:
                print(f"[ERRO] Seu limite de saque é de {self.limite}!")
            else:
                return super().sacar(valor)
            
        return False
    def __str__(self):
        return f'''
                Agência: {self._agencia}
                Número da conta: {self._numero}
                Cliente: {self._cliente}
        '''
    
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        saque = conta.sacar(self.valor)

        if saque:
            conta._historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        deposito = conta.depositar(self.valor)

        if deposito:
            conta._historico.adicionar_transacao(self)

def verificar_cpf(cpf, clientes):
    filtro_cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
    if filtro_cliente:    
        return filtro_cliente[0]
    else:
        return None
        
def contas_cliente(cliente):
    if not cliente.contas:
        print("[ERRO] Cliente não possui conta")
        return None
    else:
        return cliente.contas[0] 


def depositar(clientes):
    cpf = input("Digite o cpf do titular da conta: ")
    cliente = verificar_cpf(cpf, clientes)

    if not cliente:
        print(f"[ERRO] Não foi encontrado nenhum cliente com cpf {cpf}!")
        return

    conta = contas_cliente(cliente)
    if not conta:
        return 
    
    valor = float(input("Digite o valor para depositar: "))
    deposito = Deposito(valor)
    cliente.realizar_transacao(conta, deposito)


def sacar(clientes):
    cpf = input("Digite o cpf do titular da conta: ")
    cliente = verificar_cpf(cpf, clientes)

    if not cliente:
        print(f"[ERRO] Não foi encontrado nenhum cliente com cpf {cpf}!")
        return
    
    else:
        valor = float(input("Digite o valor para sacar: "))
        saque = Saque(valor)

        conta = contas_cliente(cliente)
        if not conta:
            return
        
        cliente.realizar_transacao(conta, saque)

def exibir_extrato(clientes):
    extrato = ""

    cpf = input("Digite o cpf do titular da conta: ")
    cliente = verificar_cpf(cpf, clientes)

    if not cliente:
        print(f"[ERRO] Não foi encontrado nenhum cliente com cpf {cpf}!")
        return
    
    conta = contas_cliente(cliente)
    transacoes = conta._historico.transacoes
    if not conta:
        return
    
    if not transacoes:
        extrato = "Não houveram transações"
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo']} - R$ {transacao['valor']} em {transacao['data']}\n"

    print(extrato)    

def cadastrar_usuario(clientes):
    cpf = input("Digite o cpf do titular da conta: ")
    cliente = verificar_cpf(cpf, clientes)

    if cliente:
        print(f"Usuário de CPF {cpf} ja cadastrado!")
        return
    else:
        nome = input("Insira o seu nome: ")
        data_nascimento = input("Insira a sua data de nascimento [dd/mm/aaaa]: ")
        endereco = input("Digite o seu endereço [Logradouro, numero - bairro - cidade/sigla do estado[Ex: QQ1, 01 - Vila Madalena - São Paulo/SP]]: ")

        cliente = PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nascimento=data_nascimento)
        clientes.append(cliente)

        print(f"Usuário {cliente.nome} cadastrado com sucesso!")

def cadastrar_conta_corrente(numero_conta, clientes, contas):
    cpf = input("Digite o cpf do titular da conta: ")
    cliente = verificar_cpf(cpf, clientes)

    if not cliente:
        print(f"[ERRO] Não foi encontrado nenhum cliente com cpf {cpf}!")
        return
    
    conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)

    cliente.adicionar_conta(conta) 

    contas.append(conta)
    print(f"Conta criada com sucesso!, segue os dados de sua conta corrente:\nAgência: {conta._agencia}\nNúmero da conta: {conta._numero}\nTitular: {conta._cliente.nome}")


def main():
    clientes = []
    contas = []

    while True:
        opcao = input("[d]Depósito\n[s]Saque\n[e]Extrato\n[u]Cadastrar usuário\n[cc]Criar conta corrente\n[q]Sair\nDigite:")
        opcao = opcao.lower()

        if opcao == "d":
            depositar(clientes=clientes)

        elif opcao == "s":
            sacar(clientes=clientes)

        elif opcao == "e":
            exibir_extrato(clientes=clientes)

        elif opcao == "u":
            cadastrar_usuario(clientes=clientes)

        elif opcao == "cc":
            numero_conta = len(contas) + 1
            cadastrar_conta_corrente(numero_conta=numero_conta,clientes=clientes,contas=contas)
            
        elif opcao == "q":
            print("Fechando conexão!")
            break
        
        else:
            print("Opção inválida, tente novamente!")

main()