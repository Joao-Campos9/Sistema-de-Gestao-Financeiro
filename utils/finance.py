"""
Módulo responsável por realizar o cálculo dos dados armazenados e configurar todas as informações em um dicionário único, que será usado no dashboard principal
"""

from utils.datastorage import return_json, list_years
from datetime import datetime

# Salva data local dentro de uma variável. Utilizado para as funções de redirecionamento de rotas
actual_date = datetime.now().strftime("%Y-%m-%d")

# Retorna todas as entradas e saídas do parâmentro da função
def entry_exit(data):
    # Cria variáveis para entrada e saídas
    entry = 0
    exit = 0

    # Percorre todos os dados armazenados
    for i in data:
        # Se o valor for maior ou igual a zero, somar a variável de entrada
        if i['value'] >= 0:
            entry += i['value']
        # Se o valor for menor que zero, somar a variável de saída
        elif i['value'] < 0:
            exit -= i['value'] * -1
    # Retorna os valores em uma tupla
    return entry, exit

# Retorna o saldo
def return_wallet(data):
    # Cria uma variável principal e acessa os valores de entrada e saída
    wallet = 0
    total = entry_exit(data)
    # Soma e retorna o saldo atual
    wallet = total[0] + total[1]
    return wallet

# Retorna a porcentagem das saídas sobre entradas
def prct_total(data):
    # Acessa a tupla de entradas e saídas
    total = entry_exit(data)
    # Para evitar divisão por zero, se a entrada for igual a zero, retorna 100.
    if total[0] == 0:
        return 100
    # Calcula a porcentagem de saídas sobre entradas
    else:
        prct = (abs(total[1]) / total[0]) * 100
        return prct 

# Retorna relatório dos gastos. Controlado para porcentagem menor ou igual a 80, Preocupante para maior que 80 e menor que 100, e negativado para maior que 100.
def account_status(data):
    # Pega a porcentagem geral
    prct = prct_total(data)

    # Faz a verificação seguindos os parâmetros de avaliação
    if prct < 80:
        return 'Controlado'
    elif prct < 100:
        return 'Preocupante'
    else:
        return 'Negativado'

# Retorna a quantidade de frequência de todos os tipos
def values_types(data):
    # Cria um dicionário para armazernar valores
    types_dict = {}

    # Percorre os dados armazenados
    for i in data:
        # Se não existe o tipo, adicionar no dicionário com valor 0, evitando erros.
        if i['type'] not in types_dict:
            types_dict[i['type']] = 0
        # Adiciona o valor para o tipo da transação
        types_dict[i['type']] += i['value']
    # Retorna o dicionário
    return types_dict

# Calcula a porcentagem para os tipos de entradas e saídas
def prct_types(data):
    # Acessa o dicionário de tipos e valores
    type_dict = values_types(data)

    # Cria dicionário para armazenar porcentagem
    prct_dict = {}
    # Cria variável para calcular o total dos valores
    total = 0
    # Cria uma lista com cada tipo
    types = ["Renda", "Necessidade", "Desejos", "Poupança"]

    # Se não existir o tipo, criar no dicionário para evitar erros
    for c in types:
        if c not in type_dict:
            type_dict[c] = 0

    # Percorre todos os items do dicionário, calculando o total
    for k, v in type_dict.items():
        if v < 0:
            total += v
    # Percorre todos os items
    for k, v in type_dict.items():
        # Se for menor que zero, ou seja gastos, calcular a porcentagem
        if v < 0:
            prct_dict[k] = (v / total) * 100
        # Caso seja positivo ou zero, valor se torna 0
        else:
            prct_dict[k] = 0
    # Retorna o valor de porcentagem de gastos de cada tipo
    return prct_dict

# Retorna uma lista com a quantidade de investimentos feitos em cada mês do ano
def investment_line(year): 
    # Pega todos os dados armazenados
    data = return_json()
    # Cria uma lista com cada mês
    months = [0 for i in range(12)]
    
    # Percorre todos os items armazenados
    for i in data:
        # Caso seja da categoria 'Poupança' e do ano selecionado, adicionar ao mês correspondente na lista
        if i['type'] == 'Poupança' and int(i['date'][0:4]) == year:
            months[(int(i['date'][5:7]))-1] += abs(i['value'])
    # Retorna lista com indices correspondente aos meses
    return months

# Retorna a soma de toda a lista de investimentos do ano
def total_investment(year):
    total = investment_line(year)
    total = sum(total)
    return total

# Função que filtra os investimentos apenas do mês
def month_investment(data):
    investments = 0
    for i in data:
        if i['type'] == 'Poupança':
            investments += abs(i['value'])
    return investments

# Retorna uma lista de dicionários, com a chave sendo a categoria e o valor a quantidade gasta nessa categoria
def values_categories(data):
    # Dicionário para guardar as categorias e seus valores
    categories = {}

    # Percorre todos os dados armazenados para criar chaves de categoria dentro do dicionário principal
    for i in data:
        # Cria a categoria e valor segundo os items armazenados
        category = i['category']
        valor = i['value']

        # Caso ainda não exista, cria a categoria selecionada atualmente dentro do dicionário principal
        if category not in categories:
            categories[category] = 0
        
        # Adiciona o valor da categoria atual no dicionário principal
        categories[category] += valor

    # Transformar todos os dicionário em listas para organização
    categories = list(categories.items())

    # Algoritmo Bubble, usado para organizar todos os items em ordem crescente, no caso, do mais negativo ao menos negativo
    for i in range(0, len(categories) + 1):
        for j in range(0, len(categories) - 1):
            if categories[j][1] > categories[j + 1][1]:
                x = categories[j]
                categories[j] = categories[j + 1]
                categories[j + 1] = x
    return categories

# Função que verifica a posição do mês e tranforma em string com o respectivo mês
def return_month_text(month):
    # Variável para todos os meses do ano em formato de string
    months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    # Se for 0, retornar 0 para mostrar todos os items
    if month == 0:
        return 0
    # Caso contrário, pegar o indice 'month' - 1 e salve conforme o mês correspondente
    else:
        month = months[month-1]
        return month

# Função principal responsável por filtrar o json para o mês e ano atual, chamando cada função desse módulo e retornando para o dashboard da página principal
def json_filtred_date(month, year):
    # Acessa os arquivos armazenados
    data = return_json()

    # Cria uma lista para guardar somente os dados do mês e ano atual
    json_filtred = []

    # Percorre todos os dados
    for i in data:

        # Se o mês for igual a zero, mostre todas as transações do ano
        if month == 0:
            # Se a transação pertence ao ano, guardar na lista
            if int(i['date'][0:4]) == year:
                json_filtred.append(i)
        
        # Caso não seja, mostre todas as transações do mês
        else:
            # Se a transação pertence ao mês, guardar na lista
            if int(i['date'][5:7]) == month and int(i['date'][0:4]) == year:
                json_filtred.append(i)
    # Configura todas as informações, retornando todos os dados processados e filtrados, para o dashboard principal
    return {
        "wallet": return_wallet(json_filtred),
        "prct": prct_total(json_filtred),
        "total": entry_exit(json_filtred),
        "types": prct_types(json_filtred),
        "status": account_status(json_filtred),
        "date": actual_date,
        "lineGraphic": investment_line(year),
        "totalInvestments": total_investment(year),
        "monthInvestments": month_investment(json_filtred),
        "rankingCategories": values_categories(json_filtred),
        "listYears": list_years()
    }
