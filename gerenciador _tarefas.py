import json
import os

ARQUIVO = "tarefas.json"


def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except (json.JSONDecodeError, OSError):
            print("Aviso: arquivo de tarefas corrompido ou ilegível. Iniciando lista vazia.")
            return []
    return []


def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)


def escolher_prioridade():
    print("Escolha a prioridade:")
    print("1 - Alta")
    print("2 - Média")
    print("3 - Baixa")

    opcao_prioridade = input("Digite a prioridade: ").strip()

    if opcao_prioridade == "1":
        return "Alta"
    elif opcao_prioridade == "2":
        return "Média"
    elif opcao_prioridade == "3":
        return "Baixa"
    else:
        print("Opção inválida, prioridade definida como Baixa por padrão.")
        return "Baixa"


def adicionar_tarefa(tarefas):
    print("Digite as tarefas, uma por vez.")
    print("Quando terminar, pressione ENTER sem digitar nada.\n")

    quantidade_adicionada = 0

    while True:
        descricao = input("Digite a tarefa (ou ENTER para encerrar): ").strip()

        if not descricao:
            break

        prioridade = escolher_prioridade()

        tarefas.append({
            "descricao": descricao,
            "prioridade": prioridade,
            "concluida": False
        })
        quantidade_adicionada += 1
        print("Tarefa adicionada!\n")

    if quantidade_adicionada > 0:
        salvar_tarefas(tarefas)
        print(f"\n{quantidade_adicionada} tarefa(s) adicionada(s) com sucesso!")
    else:
        print("\nNenhuma tarefa foi adicionada.")


def listar_tarefas(tarefas):
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    print("\n=== LISTA DE TAREFAS ===")
    for i, tarefa in enumerate(tarefas, start=1):
        status = "✅" if tarefa["concluida"] else "x"
        prioridade = tarefa.get("prioridade", "Baixa")
        print(f"{i}. [{status}] ({prioridade}) {tarefa['descricao']}")


def ler_indices(tarefas, mensagem):
    entrada = input(mensagem).strip()

    if not entrada:
        return []

    partes = entrada.replace(",", " ").split()

    indices_validos = []
    indices_invalidos = []

    for parte in partes:
        try:
            numero = int(parte)
            indice = numero - 1

            if 0 <= indice < len(tarefas):
                if indice not in indices_validos:
                    indices_validos.append(indice)
            else:
                indices_invalidos.append(parte)

        except ValueError:
            indices_invalidos.append(parte)

    if indices_invalidos:
        print(f"Ignorado(s) por serem inválidos: {', '.join(indices_invalidos)}")

    return sorted(indices_validos)


def concluir_tarefa(tarefas):
    listar_tarefas(tarefas)

    if not tarefas:
        return

    print("\nVocê pode digitar vários números separados por vírgula ou espaço.")
    print("Exemplo: 1, 3, 5  ou  1 3 5")

    indices = ler_indices(tarefas, "Digite o(s) número(s) da(s) tarefa(s) concluída(s): ")

    if not indices:
        print("Nenhuma tarefa válida foi selecionada.")
        return

    contador_concluidas = 0
    contador_ja_concluidas = 0

    for indice in indices:
        if tarefas[indice]["concluida"]:
            contador_ja_concluidas += 1
        else:
            tarefas[indice]["concluida"] = True
            contador_concluidas += 1

    if contador_concluidas > 0:
        salvar_tarefas(tarefas)

    print(f"\n{contador_concluidas} tarefa(s) marcada(s) como concluída(s).")
    if contador_ja_concluidas > 0:
        print(f"{contador_ja_concluidas} já estava(m) concluída(s).")


def remover_tarefa(tarefas):
    listar_tarefas(tarefas)

    if not tarefas:
        return

    print("\nVocê pode digitar vários números separados por vírgula ou espaço.")
    print("Exemplo: 1, 3, 5  ou  1 3 5")

    indices = ler_indices(tarefas, "Digite o(s) número(s) da(s) tarefa(s) para remover: ")

    if not indices:
        print("Nenhuma tarefa válida foi selecionada.")
        return

    print("\nTarefas selecionadas para remoção:")
    for indice in indices:
        print(f"- {tarefas[indice]['descricao']}")

    confirmacao = input("\nTem certeza que deseja remover essas tarefas? (s/n): ").strip().lower()

    if confirmacao != "s":
        print("Remoção cancelada.")
        return

    removidas = []
    for indice in sorted(indices, reverse=True):
        removidas.append(tarefas.pop(indice)["descricao"])

    salvar_tarefas(tarefas)

    print(f"\n{len(removidas)} tarefa(s) removida(s):")
    for descricao in removidas:
        print(f"- {descricao}")


def menu():
    tarefas = carregar_tarefas()

    while True:
        print("\n=== GERENCIADOR DE TAREFAS ===")
        print("1 - Adicionar tarefa(s)")
        print("2 - Listar tarefas")
        print("3 - Concluir tarefa(s)")
        print("4 - Remover tarefa(s)")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_tarefa(tarefas)

        elif opcao == "2":
            listar_tarefas(tarefas)

        elif opcao == "3":
            concluir_tarefa(tarefas)

        elif opcao == "4":
            remover_tarefa(tarefas)

        elif opcao == "5":
            print("Encerrando sistema!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()