def calcular_media(valores):
    if len(valores) == 0:
        return 0
    return sum(valores) / len(valores)

def ler_dados_clientes(arquivo):
    clientes = []
    
    with open(arquivo, 'r') as file:
        for linha in file:
            dados = linha.strip().split(';')
            idade = int(dados[2])
            renda = float(dados[3])
            clientes.append((dados[0], dados[1], idade, renda))
    
    return clientes