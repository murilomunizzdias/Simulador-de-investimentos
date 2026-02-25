from collections import namedtuple
import psycopg2

Investimento = namedtuple('Investimento', ['nome', 'taxa', 'risco'])

INVESTIMENTOS_FIXOS = (
    Investimento("CDB", 0.12, 1),
    Investimento("LCI", 0.09, 1),
    Investimento("ACOES", 0.25, 3),
    Investimento("CRIPTO", 0.80, 4)
)


# 2. CONEXÃO COM O BANCO
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="invest_db",
        user="postgres",
        password="722406"
    )



def listar_investimentos():
    print("   CATÁLOGO DE INVESTIMENTOS")
    for inv in INVESTIMENTOS_FIXOS:
        print(f"Ativo: {inv.nome:8} | Rendimento: {inv.taxa * 100:4.1f}% | Risco: {inv.risco}")

def cadastrar_cliente():
    print("\n--- Cadastro Invest-Genius ---")
    nome = input("Digite seu nome de usuário: ").strip()
    idade = int(input("Digite sua idade: "))

    if idade < 18:
        print(f"Cadastro negado. {nome} é menor de idade.")
        return

    salario = float(input("Qual seu salário mensal? R$ "))
    tol = int(input("Tolerância de Risco (1 a 4): "))

    while tol < 1 or tol > 4:
        print("Tolerância inválida! Use de 1 a 4.")
        tol = int(input("Tolerância de Risco (1 a 4): "))

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO clientes (nome, idade, salario, tolerancia) VALUES (%s, %s, %s, %s)",
                    (nome, idade, salario, tol)
                )
                conn.commit()
                print(f"\n[SUCESSO] Cliente '{nome}' cadastrado no banco de dados!")
    except psycopg2.errors.UniqueViolation:
        print("\n[ERRO] Este usuário já existe no sistema.")
    except Exception as e:
        print(f"\n[ERRO] Falha ao conectar ao banco: {e}")


def menu_cliente(nome_usuario, id_usuario, tolerancia):
    while True:
        print(f"\n>>> ÁREA DO CLIENTE: {nome_usuario.upper()} (Risco: {tolerancia}) <<<")
        print("1. Consultar e Comprar Ativos")
        print("2. Ver Minha Carteira (Saldo)")
        print("3. Avançar Tempo (Simular Rendimentos)")
        print("4. Logout")

        opcao = input("Escolha uma ação: ")

        if opcao == "1":
            listar_investimentos()
            print(f"Sugestões para seu perfil:")
            for inv in INVESTIMENTOS_FIXOS:
                if inv.risco <= tolerancia:
                    print(f" -> {inv.nome} ({inv.taxa * 100}% a.a)")

            compra = input("\nNome do ativo para comprar (ou 'S' para sair): ").upper()
            if compra == 'S': continue

            ativo_valido = next((i for i in INVESTIMENTOS_FIXOS if i.nome == compra), None)

            if ativo_valido:
                valor = float(input(f"Quanto deseja aplicar em {compra}? R$ "))
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO carteiras (cliente_id, nome_ativo, taxa, valor_acumulado) VALUES (%s, %s, %s, %s)",
                            (id_usuario, ativo_valido.nome, ativo_valido.taxa, valor)
                        )
                        conn.commit()
                print(f"Sucesso! {compra} adicionado à sua carteira.")
            else:
                print("Ativo inválido ou não encontrado.")

        elif opcao == "2":
            print(f"\n--- EXTRATO CONSOLIDADO: {nome_usuario} ---")
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT nome_ativo, valor_acumulado FROM carteiras WHERE cliente_id = %s",
                                (id_usuario,))
                    itens = cur.fetchall()

                    if not itens:
                        print("Sua carteira está vazia.")
                    else:
                        total = 0
                        for nome_at, valor_ac in itens:
                            print(f"Ativo: {nome_at:8} | Saldo: R$ {valor_ac:10.2f}")
                            total += valor_ac
                        print("-" * 35)
                        print(f"PATRIMÔNIO TOTAL: R$ {total:.2f}")

        elif opcao == "3":
            anos = int(input("Quantos anos deseja simular no futuro? "))
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, valor_acumulado, taxa FROM carteiras WHERE cliente_id = %s", (id_usuario,))
                    carteira = cur.fetchall()

                    for item_id, valor, taxa in carteira:
                        novo_valor = valor * (1 + taxa) ** anos
                        cur.execute("UPDATE carteiras SET valor_acumulado = %s WHERE id = %s", (novo_valor, item_id))
                    conn.commit()
            print(f"Simulação concluída! Saldos atualizados para daqui a {anos} anos.")

        elif opcao == "4":
            print(f"Saindo da conta de {nome_usuario}...")
            break


# 6. LOOP PRINCIPAL DO SISTEMA
def iniciar_sistema():
    while True:
        print("\n" + "#" * 30)
        print("       INVEST-GENIUS V3")
        print("       (PostgreSQL Edition)")
        print("#" * 30)
        print("1. Criar Nova Conta")
        print("2. Login (Acessar Conta)")
        print("3. Encerrar")

        escolha = input("\nAção: ")

        if escolha == "1":
            cadastrar_cliente()

        elif escolha == "2":
            user_login = input("Nome de usuário: ").strip()
            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT id, tolerancia FROM clientes WHERE nome = %s", (user_login,))
                        resultado = cur.fetchone()

                        if resultado:
                            # resultado[0] = ID, resultado[1] = Tolerância
                            menu_cliente(user_login, resultado[0], resultado[1])
                        else:
                            print("Usuário não encontrado.")
            except Exception as e:
                print(f"Erro ao tentar login: {e}")

        elif escolha == "3":
            print("Desligando motores... Até a próxima!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    iniciar_sistema()