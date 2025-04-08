from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = [] 

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def trocar_conta(self, num_conta):
        for conta in self.contas:
            if conta.numero == num_conta:
                return conta
        return False

class PessoaFisica(Cliente):
    def __init__(self, endereco, *, nome, cpf, data_nasc):
        super().__init__(endereco)
        self.nome = nome
        self._cpf = cpf
        self._data_nasc = data_nasc

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def data_nasc(self):
        return self._data_nasc

class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self):
        pass
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor
        })

class Conta:
    # lembrar que é possivel definir atributos sem os declarar como atributos de instância
    def __init__(self, cliente: PessoaFisica, numero: int):
        self._saldo = 0
        self.numero = numero
        self.agencia = '0001'
        self.cliente = cliente
        self.historico = Historico() #objeto do tipo historico

    @property
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print('Saldo insuficiente!')
        elif valor > 0:
            self._saldo -= valor
            print(f'Saque de {valor} realizado com sucesso!')
            return True
        else:
            print('Valor inválido!')

        return False


    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'Depósito de {valor} realizado com sucesso!')
            return True
        else:
            print('Valor inválido!')

        return False

class ContaCorrente(Conta):
    def __init__(self, cliente: PessoaFisica, numero:int, limite_saque = 3, limite_valor_saque = 500):
        ## super chama TODO o construtor __init da classe pai na classe na classe filha
        super().__init__(cliente=cliente, numero=numero)
        self.limite_saque = limite_saque
        self._limite_valor_saque = limite_valor_saque


    def sacar(self, valor):
        num_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == 'Saque'])

        if valor > self._limite_valor_saque:
            print('Valor de saque maior que o limite permitido!')
        elif num_saques >= 3:
            print('Limite de saques atingido!')
        else:
            return super().sacar(valor)
        return False
    
    def depositar(self, valor):
        if valor <= 0:
            print("Digite um valor válido para depositar.")
        else:
            return super().depositar(valor)
        return False
    
    def ver_extrato(self):
        extrato = f'\n{'~'*50}\n{'EXTRATO'.center(50)}\n{'~'*50}\n'

        extrato += f'Agência: {self.agencia}\n'
        extrato += f'Número da conta: {self.numero}\n'
        extrato += f'CPF: {self.cliente.cpf}\n'

        extrato += f'Depósitos: \n'
        depositos = [transicao for transicao in self.historico.transacoes if transicao['tipo'] == 'Deposito']
        for deposito in depositos:
            extrato += f'   + R${deposito["valor"]:.2f}\n'

        extrato += f'Saques: \n'
        saques = [transicao for transicao in self.historico.transacoes if transicao['tipo'] == 'Saque']
        for saque in saques:
            extrato += f'   - R${saque["valor"]:.2f}\n'

        extrato += f'\n\nSaldo: R${self.saldo:.2f}\n'

        extrato += ('~'*50) + '\n'


        print(extrato)
        input("Pressione ENTER para continuar...")

def receber_cpf(msg):
    cpf = input(msg)
    if cpf.isdecimal() and len(cpf) == 11:
        return cpf
    elif cpf == '999':
        print("Operacao cancelada")
        return cpf
    else:
        print('CPF inválido! Digite somente os números, sem pontos e traços.')
        return receber_cpf(msg)

def criar_usuario():
    cpfs = [cliente.cpf for cliente in clientes]
    cpf = receber_cpf('Digite o cpf do usuário: ')
    if cpf in cpfs:
        print("ERRO! CPF ja utilizado por outro usuario.")
        return criar_usuario()
    else:
        nome = input('Digite o nome do usuário: ')
        endereco = input('Digite o endereço do usuário: ')
        data_nasc = input('Digite a data de nascimento do usuário no formato dd/mm/aaaa: ')
        return PessoaFisica(endereco, nome=nome, data_nasc=data_nasc, cpf=cpf)

def criar_conta(usuario):
    conta_nova = ContaCorrente.nova_conta(cliente=usuario, numero=len(usuario.contas) + 1)
    usuario.adicionar_conta(conta_nova)
    return conta_nova

def trocar_usuario(clientes, usuario_atual):
    print("Usuários: ")
    print('-'*30) 
    print(f"{'NOME':<15}{'CPF':>15}")
    for cliente in clientes:
        print(f"{'-> 'if cliente == usuario_atual else '   '}{cliente.nome:<15}{cliente.cpf:>15}")
    print('Digite 999 para cancelar operacao')
    cpf = receber_cpf("Para qual CPF vc gostaria de mudar de conta?")
    if cpf != '999':
        for cliente in clientes:
            if cliente.cpf == cpf:
                print("Usuário alterado com sucesso")
                return cliente
        print("CPF nao encontrado.")
    return usuario_atual

def acessar_contas(usuario_atual, conta_atual):
    print('-'*30)
    for conta in usuario_atual.contas:
        print(f"{'->' if conta == conta_atual else '  '} Número de conta: {conta.numero}")
    print('-'*30)
    print('Digite 999 para cancelar operacao')
    num = int(input("Digite o número da conta que você deseja entrar: "))
    if num != 999:
        nova_conta = usuario_atual.trocar_conta(num)
        if not nova_conta:
            print("ERRO! ESSA CONTA NAO EXISTE")
        else:
            print("Conta trocada com sucesso!")
            return nova_conta
    return conta_atual

# Funcionamento: O programa funciona como se o usuário estivesse logado em um conta, onde pode realizar operações. Não permite criar um usuário sem contas.
# Assim não é necessário informar o cpf da conta para realizar qualquer operação

menu = f'''\n{'-'*40}\n{'MENU'.center(40)}\n{'-'*40}\n
Escolha alguma das opções abaixo:
[0] Sair do programa         [1] Criar nova conta 
[2] Criar novo usuário       [3] Trocar de usuário    
[4] Acessar contas           [5] Ver minhas informações
[6] Consultar extrato        [7] Depositar valor
[8] Sacar valor 
'''

boas_vindas = f'''\n{'-'*40}\n{'BEM VINDO AO BANCO'.center(40)}\n{'-'*40}\n
Para poder acessar as funcionalidades do nosso banco, 
é necessário criar um usuário. 
'''

clientes = []
agencia = '0001'

print(boas_vindas)

usuario_atual = criar_usuario()
conta_atual = criar_conta(usuario_atual)
clientes.append(usuario_atual)

while (True):
    print(menu)
    escolha = input("Escolha: ")

    if escolha == '0':
        print('Saindo do programa...')
        break

    elif escolha == '1':
        # criar nova conta
        conta_atual = criar_conta(usuario_atual)

    elif escolha == '2':
        # criar novo usuario
        usuario_atual = criar_usuario()
        conta_atual = criar_conta(usuario_atual)
        clientes.append(usuario_atual)

    elif escolha == '3':
        # Acessar contas
        usuario_atual = trocar_usuario(clientes, usuario_atual)
        conta_atual = usuario_atual.contas[0]

    elif escolha == '4':
         # trocar de conta
         conta_atual = acessar_contas(usuario_atual, conta_atual)

    elif escolha == '5':
        # Ver minhas informações pessoais
         #FIXME: criar __str__ para PessoaFisica() e usar em usuario_atual
         print(f'Nome: {usuario_atual.nome}')
         print(f'Data de Nascimento: {usuario_atual.data_nasc}')
         print(f'Endereço: {usuario_atual.endereco}')
         print(f'CPF: {usuario_atual.cpf}')

    elif escolha == '6':
        # Mostrar extrato
        conta_atual.ver_extrato()

    elif escolha == '7':
        # Receber deposito
        valor = float(input('Digite o valor a ser depositado: R$'))
        depositar = conta_atual.depositar(valor)
        if depositar:
            usuario_atual.realizar_transacao(conta_atual, Deposito(valor))

    elif escolha == '8':
        # receber saque
        valor = float(input('Digite o valor a ser sacado: R$'))
        sacar = conta_atual.sacar(valor)
        if sacar:
            usuario_atual.realizar_transacao(conta_atual, Saque(valor))

    else:
        print('\nOpção não válida! Tente Novamente.')