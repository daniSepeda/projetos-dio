import datetime

def mostrarExtrato(saques, depositos, saldo):
    # Cria uma string com o extrato da conta
    extrato = f'\n{'~'*50}\n{'EXTRATO'.center(50)}\n{'~'*50}\n'

    extrato += 'Depósitos: \n'
    if (depositos):
        for valor, horario in depositos.items():
            extrato += f' + R${valor:<15.2f}{horario:>30}\n'
    else:
        extrato += '  Nenhum depósito registrado.\n'

    extrato += 'Saques: \n'
    if (saques):
        for valor, horario in saques.items():
            extrato += f' - R${valor:<15.2f}{horario:>30}\n'
    else:
        extrato += '  Nenhum saque registrado.\n'

    extrato += f'\nSaldo: R${saldo:.2f}\n'
    
    extrato += ('~'*50) + '\n'

    print(extrato)

    print('Pressione Enter para continuar...')
    input()

    return extrato


def receber_deposito(deposito, saldo):
    # Recebe o valor do depositado e retorna o saldo atualizado
    valor = float(input('Digite o valor a ser depositado na conta: R$'))

    digitos = str(valor)
    if '.' in digitos:
        digitos = digitos.replace('.', '')

    if not digitos.isdecimal() or valor <= 0:
        print('Valor inválido! Digite números positivos')
    else:
        saldo += valor
        horario = datetime.datetime.now()
        deposito[valor] = horario.strftime("%c")
    
    return saldo


def sacar_dinheiro(saques, saldo, limite_valor_saque):
    # Recebe o valor a ser sacado e retorna o saldo atualizado
    # O limite de saques diários é verificado fora dessa função
    valor = float(input('Digite o valor a ser retirado da conta: R$'))

    if valor > saldo:
        print('Retirada não permitida! Saldo insuficiente.')
    elif valor > limite_valor_saque:
        print(f'Valor de retirada inválido! Somente até R${limite_valor_saque:.2f}')
    elif valor <= 0:
        print('Valor inválido! Informe valores positivos')
    else:
        saldo -= valor
        horario = datetime.datetime.now()
        saques[valor] = horario.strftime("%c")      
    
    return saldo
    

#-----------------------------------


menu = f'''\n{'-'*40}\n{'MENU'.center(40)}\n{'-'*40}\n
Escolha alguma das opções abaixo:
[0] Sair do programa
[1] Consultar extrato
[2] Depositar valor
[3] Sacar valor
'''

extrato = ''
saques = {}
depositos = {}
saldo = 0
LIMITE_VALOR_SAQUE = 500
LIMITE_SAQUES = 3


while (True):

    print(menu)
    escolha = int(input("Escolha: "))

    if escolha == 0:
        print('Saindo do programa...')
        break
    elif escolha == 1:
        extrato = mostrarExtrato(saques, depositos, saldo)
    elif escolha == 2:
        saldo  = receber_deposito(depositos, saldo)
    elif escolha == 3:
        if (len(saques.keys()) < LIMITE_SAQUES):
            saldo = sacar_dinheiro(saques, saldo, LIMITE_VALOR_SAQUE)
        else:
            print('\nLimite de saques atingido!')
    else:
        print('\nOpção não válida! Tente Novamente.')



