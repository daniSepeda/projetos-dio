import datetime

# filtra cpfs válidos
def receber_cpf(msg):
    cpf = input(msg)
    if cpf.isdecimal() and len(cpf) == 11:
        return cpf
    else:
        print('CPF inválido! Digite somente os números, sem pontos e traços.')
        return receber_cpf(msg)

# recebe endereço
def receber_endereco():
    logradouro = input("Digite o seu logradouro: ")
    num = input("Digite o número da sua residência: ")
    bairro = input("Digite o nome do seu bairro: ")
    cidade = input("Digite o nome da sua cidade :")
    estado_sigla = input("Digite a sigla do seu estado: ")
    formatado = f'{logradouro}, {num} - {bairro} - {cidade}/{estado_sigla}'
    return formatado


# coloca dentro de contas_atuais todas as contas do usuario atual
def receber_contas_atuais(contas_atuais, contas, usuario_atual):
    contas_atuais.clear()
    for conta in contas:
        if conta['usuario'] == usuario_atual['cpf']:
            contas_atuais.append(conta)


# cria um usuario e retorna a lista com ele 
def criar_usuario(usuarios=[], usuario_atual={}):
    # vamos pegar o nome, data de nascimento, cpf e endereço
    dados = {}
    dados.fromkeys(('nome', 'data_nascimento', 'cpf', 'endereco'), '')
    cpf = receber_cpf('Insira seu CPF sem pontos e traços: ')
    if usuarios != []:
        lista_cpf = [usuarios[n]['cpf'] for n in range(len(usuarios))]
        if cpf in lista_cpf:
            # Perguntar se quer criar um nova conta com o mesmo ou não
            print("CPF já registrado!")
            return usuario_atual
        
    dados['cpf'] = cpf
    dados['nome'] = input('Digite seu nome: ')
    dados['data_nascimento'] = input('Digite sua data de nascimento no formato dd/mm/aaaa: ')
    dados['endereco'] = receber_endereco()
    usuarios.append(dados)
    return dados


# Apenas lista os nomes de todos os usuários
def listar_usuarios(usuarios):
    print("Contas: ")
    print('-'*30) 
    print(f"{'NOME':<15}{'CPF':>15}")
    for n in range(len(usuarios)):
        print(f"{'->  'if usuarios[n] == usuario_atual else '   '}{usuarios[n]['nome']:<15}{usuarios[n]['cpf']:>15}")
    print('-'*30)


# função para alterar de usuario de algum momento
# retorna a posição do usuário na lista de usuarios 
def alterar_usuario(usuarios=[], usuario_atual={}):
    listar_usuarios(usuarios)
    cpf = receber_cpf("Para qual CPF vc gostaria de mudar de conta?")
    for n in range(len(usuarios)):
        if (cpf == usuarios[n]['cpf']):
            print(f"\nTrocando para conta de {usuarios[n]['nome']}...")
            return usuarios[n]
    print("CPF não registrado!")
    return usuario_atual
    
  
# cria uma conta baseada no usuario atual
def criar_conta(contas=[], contas_atuais=[], usuario_atual={}):
    # salvar agencia, numero da conta e usuario, no caso seu cpf
    dados = {}
    dados['agencia'] = '0001'
    dados['num_conta'] = len(contas) + 1
    dados['usuario'] = usuario_atual['cpf']
    dados['saldo'] = 0
    dados['saques'] = {}
    dados['depositos'] = {}
    contas.append(dados)
    contas_atuais.append(dados)
    return dados


# acessar contas
def acessar_conta(contas, conta_atual, contas_atuais, usuario_atual):
    # voltar ao menu, criar uma conta ou trocar para uma conta já existe
    # retorna sempre a conta_atual
    indices = []
    print('-'*40)
    print(f"{'INDICE':<15}{'Número de conta':>10}")
    for n in range(len(contas_atuais)):
            print(f"{'-> ' if contas_atuais[n] == conta_atual else '   '}{n:<15}{contas_atuais[n]['num_conta']:>10}")
            indices.append(str(n))
            
    print('-'*40)

    while (True):
        print('''
    Opções:
    [0] Voltar ao menu
    [1] Criar nova conta e entrar nela
    [2] Trocar de conta
    ''')
        escolha = input("Escolha: ")
        if escolha == '0':
            return conta_atual
        elif escolha == '1':
            nova_conta_atual = criar_conta(contas=contas, usuario_atual=usuario_atual)
            contas_atuais.append(nova_conta_atual)
            return nova_conta_atual
        elif escolha == '2':
            indice = input("Escolha um indice para a acessar a conta correspondente: ")
            while indice not in indices:
                indice = input("Escolha um indice para a acessar a conta correspondente: ")
            return contas_atuais[int(indice)]
        else:
            print('Opção inválida!')


# mostrar extrato
def mostrar_extrato(conta_atual, saques, depositos, saldo):
    # Cria uma string com o extrato da conta
    extrato = f'\n{'~'*50}\n{'EXTRATO'.center(50)}\n{'~'*50}\n'

    extrato += f'Agência: {conta_atual['agencia']}\n'
    extrato += f'Número de Conta: {conta_atual['num_conta']}\n'
    extrato += f'CPF: {conta_atual['usuario']}\n'

    extrato += 'Depósitos: \n'
    if depositos:
        for valor, horario in depositos.items():
            extrato += f' + R${valor:<15.2f}{horario:>30}\n'
    else:
        extrato += '  Nenhum depósito registrado.\n'

    extrato += 'Saques: \n'
    if saques:
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

# receber deposito
def receber_deposito(deposito, saldo, /):
    # Itera para decobrir as contas do usuário
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

# sacar dinheiro 
def sacar_dinheiro(*, saques, saldo, limite_valor_saque):
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
[0] Sair do programa         [1] Criar novo usuário e conta
[2] Trocar de usuário        [3] Acessar contas     
[4] Ver minhas informações   [5] Consultar extrato
[6] Depositar valor          [7] Sacar valor 
'''

boas_vindas = f'''\n{'-'*40}\n{'BEM VINDO AO BANCO'.center(40)}\n{'-'*40}\n
Para poder acessar as funcionalidades do nosso banco, 
é necessário criar um usuário. 
'''

# Listas para armazenar os usuários e contas no total, e as contas do usuário atual
contas = []
contas_atuais = []
usuarios = []
LIMITE_VALOR_SAQUE = 500
LIMITE_SAQUES = 3

print(boas_vindas)

# criar o primeiro usuário e uma conta para ele retornar seu numero de usuario 
usuario_atual = criar_usuario(usuarios)
conta_atual = criar_conta(contas, contas_atuais, usuario_atual)

while (True):


    print(menu)
    escolha = input("Escolha: ")

    if escolha == '0':
        print('Saindo do programa...')
        break
    
    elif escolha == '1':
        # Criar novo usuario e receber o usuário atual
        usuario_atual = criar_usuario(usuarios)
        conta_atual = criar_conta(contas, contas_atuais, usuario_atual)

    elif escolha == '2':
        # Trocar de usuário e receber suas contas
        usuario_atual = alterar_usuario(usuarios, usuario_atual)
        receber_contas_atuais(contas_atuais, contas, usuario_atual)
        conta_atual = contas_atuais[0]

    elif escolha == '3':
        # Acessar contas 
        conta_atual = acessar_conta(contas, conta_atual, contas_atuais, usuario_atual)

    elif escolha == '4':
         # Ver minhas informações pessoais
         print(f'Nome: {usuario_atual['nome']}')
         print(f'Data de Nascimento: {usuario_atual['data_nascimento']}')
         print(f'Endereço: {usuario_atual['endereco']}')
         print(f'CPF: {usuario_atual['cpf']}')

    elif escolha == '5':
        # Mostrar extrato
        mostrar_extrato(conta_atual, conta_atual['saques'], conta_atual['depositos'], conta_atual['saldo'])

    elif escolha == '6':
        # Receber deposito
        conta_atual['saldo'] = receber_deposito(conta_atual['depositos'], conta_atual['saldo'])

    elif escolha == '7':

        # Sacar dinheiro
        if (len(conta_atual['saques'].keys()) < LIMITE_SAQUES):
            conta_atual['saldo'] = sacar_dinheiro(saques=conta_atual['saques'],  
                                                 saldo=conta_atual['saldo'], limite_valor_saque=LIMITE_VALOR_SAQUE)
        else:
            print('\nLimite de saques atingido!')
    
    else:
        print('\nOpção não válida! Tente Novamente.')



