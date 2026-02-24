from collections import namedtuple

#DEFS E TUPLA DE INVESTIMENTOS
Investimento = namedtuple('Investimento', ['nome', 'taxa', 'risco'])

INVESTIMENTOS_FIXOS = (
    Investimento("CDB", 0.12, 1),
    Investimento("LCI", 0.09, 1),
    Investimento("ACOES", 0.25, 3),
    Investimento("CRIPTO", 0.80, 4)
)

banco_dados_fake = {}

def listar_investimentos():
    print("\n--- Catálogo de Investimentos Disponíveis ---")
    for inv in INVESTIMENTOS_FIXOS:
        print(f"Ativo: {inv.nome:8} | Rendimento: {inv.taxa * 100:4.1f}% | Risco: {inv.risco}")

def cadastrar_cliente():
    print("\n--- Cadastro Invest ---")
    nome = input("Digite seu nome de usuário: ").strip()

    if nome in banco_dados_fake:
        print("Este usuário já existe!")
        return

    idade = int(input("Digite sua idade: "))
    if idade < 18:
        print(f"Cadastro negado. {nome} é menor de idade.")
        return

    salario = float(input("Qual seu salário mensal? R$ "))
    tol = int(input("Tolerância de Risco (1 a 4): "))

    while tol < 1 or tol > 4:
        print("Tolerância inválida! Use de 1 a 4.")
        tol = int(input("Tolerância de Risco (1 a 4): "))


    banco_dados_fake[nome] = {
        "dados": {"nome": nome, "idade": idade, "salário": salario, "tol": tol},
        "carteira": []
    }
    print(f"Conta para '{nome}' criada com sucesso!")


def menu_cliente(nome_usuario):
    cliente = banco_dados_fake[nome_usuario]

    while True:
        print(f"\n>> LOGADO COMO: {nome_usuario} <<")
        print("1. Consultar Recomendações e Comprar")
        print("2. Ver Minha Carteira (Saldo Atual)")
        print("3. Avançar Tempo (Simular Rendimentos)")
        print("4. Sair (Logout)")

        opcao = input("Escolha uma ação: ")

        if opcao == "1":
            listar_investimentos()
            print(f"\n--- Sugestões para seu perfil (Risco {cliente['dados']['tol']}) ---")
            for inv in INVESTIMENTOS_FIXOS:
                if inv.risco <= cliente['dados']['tol']:
                    print(f"-> {inv.nome} ({inv.taxa * 100}% a.a)")

            compra = input("\nNome do investimento para comprar (ou 'S' para sair): ").upper()
            encontrado = False
            for inv in INVESTIMENTOS_FIXOS:
                if inv.nome == compra:
                    valor = float(input(f"Quanto deseja aplicar em {inv.nome}? R$ "))

                    cliente['carteira'].append({
                        "nome": inv.nome,
                        "taxa": inv.taxa,
                        "valor_acumulado": valor
                    })
                    print(f"Sucesso! {inv.nome} adicionado à sua carteira.")
                    encontrado = True
                    break
            if compra != 'S' and not encontrado:
                print("Investimento não encontrado.")

        elif opcao == "2":
            print(f"\n--- Carteira Atualizada de {nome_usuario} ---")
            if not cliente['carteira']:
                print("Você ainda não possui investimentos.")
            else:
                total_patrimonio = 0
                for item in cliente['carteira']:
                    print(f"Ativo: {item['nome']:8} | Saldo: R$ {item['valor_acumulado']:10.2f}")
                    total_patrimonio += item['valor_acumulado']
                print("-" * 30)
                print(f"PATRIMÔNIO TOTAL: R$ {total_patrimonio:.2f}")

        elif opcao == "3":
            if not cliente['carteira']:
                print("Sua carteira está vazia. Não há o que render!")
                continue

            anos = int(input("Quantos anos você deseja simular no futuro? "))
            print(f"\n--- Simulando Rendimentos (+{anos} anos) ---")
            for item in cliente['carteira']:
                valor_antigo = item['valor_acumulado']
                item['valor_acumulado'] *= (1 + item['taxa']) ** anos
                lucro = item['valor_acumulado'] - valor_antigo
                print(f"{item['nome']}: Rendeu R$ {lucro:.2f}")
            print("Simulação concluída com sucesso!")

        elif opcao == "4":
            print(f"Até logo, {nome_usuario}!")
            break



while True:
    print("     INVEST-GENIUS V3   ")
    print("1. Criar Nova Conta")
    print("2. Acessar Minha Conta (Login)")
    print("3. Encerrar Sistema")

    escolha = input("Ação: ")

    if escolha == "1":
        cadastrar_cliente()
    elif escolha == "2":
        user_login = input("Nome de usuário: ").strip()
        if user_login in banco_dados_fake:
            menu_cliente(user_login)
        else:
            print("Usuário não cadastrado.")
    elif escolha == "3":
        print("Sistema encerrado.")
        break