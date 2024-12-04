import util

def main():
    clientes = util.ler_dados_clientes('clientes.txt')

    idades = [cliente[2] for cliente in clientes]
    rendas = [cliente[3] for cliente in clientes]

    media_idade = util.calcular_media(idades)
    media_renda = util.calcular_media(rendas)

    print(f'Média de idade dos clientes: {media_idade:.2f}')
    print(f'Média de renda mensal dos clientes: {media_renda:.2f}')

if __name__ == "__main__":
    main()

