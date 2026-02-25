from collections import namedtuple
import psycopg2

Investimento = namedtuple('Investimento', ['nome', 'taxa', 'risco'])

INVESTIMENTOS_FIXOS = (
    Investimento("CDB", 0.12, 1),
    Investimento("LCI", 0.09, 1),
    Investimento("ACOES", 0.25, 3),
    Investimento("CRIPTO", 0.80, 4)
)



def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="invest_db",
        user="postgres",
        password="722406"
    )



def listar_investimentos():
    print("\n" + "=" * 45)
    print("      CATÁLOGO DE INVESTIMENTOS DISPONÍVEIS")
    print("=" * 45)
    for inv in INVESTIMENTOS_FIXOS:
        print(f"Ativo: {inv.nome:8} | Rendimento: {inv.taxa * 100:4.1f}% | Risco: {inv.risco}")
    print("=" * 45)




def cadastrar_cliente():
    print("\n--- Cadastro Bradesco Invest ---")
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
                # CREATE (C do CRUD)
                cur.execute(
                    "INSERT INTO clientes (nome, idade, salario, tolerancia) VALUES (%s, %s, %s, %s)",
                    (nome, idade, salario, tol)
                )
                conn.commit()
                print(f"\n[SUCESSO] Cliente '{nome}' cadastrado!")
    except psycopg2.errors.UniqueViolation:
        print("\n[ERRO] Este usuário já existe.")
    except Exception as e:
        print(f"\n[ERRO] Erro ao conectar: {e}")


def deletar_conta(id_usuario, nome_usuario):
    """Exclui o usuário e todos os dados vinculados (D do CRUD)"""
    print(f"\n!!! ATENÇÃO: EXCLUSÃO PERMANENTE DA CONTA DE {nome_usuario.upper()} !!!")
    confirmar = input("Tem certeza que deseja apagar tudo? (S/N): ").upper()

    if confirmar == 'S':
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    # DELETE
                    cur.execute("DELETE FROM clientes WHERE id = %s", (id_usuario,))
                    conn.commit()
            print("\n[SUCESSO] Seus dados foram removidos. Até a próxima!")
            return True
        except Exception as e:
            print(f"Erro ao deletar conta: {e}")
    return False


def menu_cliente(nome_usuario, id_usuario, tolerancia):
    while True:
        print(f"\n>>> LOGADO: {nome_usuario.upper()} | Perfil Risco: {tolerancia} <<<")
        print("1. Consultar e Comprar Ativos")
        print("2. Ver Minha Carteira (Extrato Detalhado)")
        print("3. Avançar Tempo (Simular e Salvar Rendimentos)")
        print("4. Encerrar Minha Conta (Excluir Tudo)")
        print("5. Logout")

        opcao = input("Escolha uma ação: ")

        if opcao == "1":
            listar_investimentos()
            compra = input("\nNome do ativo para comprar (ou 'S' para sair): ").upper()
            if compra == 'S': continue

            ativo = next((i for i in INVESTIMENTOS_FIXOS if i.nome == compra), None)

            if ativo and ativo.risco <= tolerancia:
                valor = float(input(f"Quanto deseja aplicar em {compra}? R$ "))
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO carteiras (cliente_id, nome_ativo, taxa, valor_acumulado) VALUES (%s, %s, %s, %s)",
                            (id_usuario, ativo.nome, ativo.taxa, valor)
                        )
                        conn.commit()
                print(f"Sucesso! {compra} adicionado à carteira.")
            else:
                print("Ativo inválido ou incompatível com seu risco.")

        elif opcao == "2":

            print(f"\n--- CARTEIRA CONSOLIDADA: {nome_usuario} ---")
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                SELECT nome_ativo, valor_antigo, lucro, valor_acumulado
                                FROM carteiras
                                WHERE cliente_id = %s
                                """, (id_usuario,))
                    itens = cur.fetchall()

                    if not itens:
                        print("Você ainda não possui investimentos.")
                    else:
                        total_geral = 0
                        for nome_at, v_ant, luc, v_at in itens:
                            print(
                                f"Ativo: {nome_at:8} | Antigo: R$ {v_ant:10.2f} | Lucro: R$ {luc:10.2f} | Atual: R$ {v_at:10.2f}")
                            total_geral += v_at
                        print("-" * 75)
                        print(f"PATRIMÔNIO TOTAL: R$ {total_geral:.2f}")

        elif opcao == "3":
            # UPDATE (U do CRUD)
            anos = int(input("Quantos anos deseja simular no futuro? "))
            print(f"\n--- PROCESSANDO RENDIMENTOS (+{anos} ANOS) ---")

            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, nome_ativo, valor_acumulado, taxa FROM carteiras WHERE cliente_id = %s",
                                (id_usuario,))
                    ativos = cur.fetchall()

                    for aid, nome_at, v_atual, taxa in ativos:
                        v_novo = v_atual * (1 + taxa) ** anos
                        lucro_gerado = v_novo - v_atual

                        print(f"Calculando {nome_at}... Lucro de R$ {lucro_gerado:.2f} gerado.")

                        cur.execute("""
                                    UPDATE carteiras
                                    SET valor_antigo    = %s,
                                        lucro           = %s,
                                        valor_acumulado = %s
                                    WHERE id = %s
                                    """, (v_atual, lucro_gerado, v_novo, aid))

                    conn.commit()
            print(">>> Todas as alterações foram salvas permanentemente no banco de dados!")

        elif opcao == "4":
            if deletar_conta(id_usuario, nome_usuario):
                break

        elif opcao == "5":
            break



def iniciar_sistema():
    while True:
        print("\n" + "#" * 30)
        print("       INVEST-GENIUS V3")
        print("       (SQL PERSISTENCE)")
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
                            menu_cliente(user_login, resultado[0], resultado[1])
                        else:
                            print("Usuário não encontrado.")
            except Exception as e:
                print(f"Erro no login: {e}")
        elif escolha == "3":
            print("Encerrando... Lucros salvos!")
            break


if __name__ == "__main__":
    iniciar_sistema()