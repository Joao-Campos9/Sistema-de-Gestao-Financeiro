"""
Módulo responsável por organizar todos os dados armazenados, entrada do usuário e atualização dos dados. Esse módulo utiliza a biblioteca json para manipular o arquivo responsável pela permanência de dados.
"""

import json
import os

# Verifica se existe arquivo 'data.json', caso não, cria o arquivo na pasta 'database'
if not os.path.exists('./database/data.json'):
    with open('./database/data.json', "w+", encoding="utf-8") as file:
        json.dump([], file, indent=4)

# Lê todos os dados armazenado em 'data.json' e salve em uma variável
with open('./database/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Função que devolve todos os dados do 'data.json' para qualquer parte do sistema
def return_json():
    with open('./database/data.json', 'r', encoding='utf-8') as file:
        REGISTER = json.load(file)
        return REGISTER

# Função usado para listar todos os anos segundo os registros. Usado em todos filtros e atualizando-os conforme o cadastro do usuário
def list_years():
    # Pega todos os dados
    data = return_json()
    # Cria uma lista
    years = []
    
    # Percorre todos os dados
    for i in data:
        # Se o ano não estiver na lista, adicione
        if int(i['date'][0:4]) not in years:
            years.append(int(i['date'][0:4]))
            
    # Método Bubble que organiza todos os anos em forma crescente
    for i in range(0, len(years)):
        for j in range(0, len(years) - 1):
            if years[j] > years[j + 1]:
                x = years[j]
                years[j] = years[j + 1]
                years[j + 1] = x
    return years

# Adiciona um novo registro no arquivo 'data.json'
def add_register_json(description, value, category, type, date):
    # Chama variável com todos os dados do 'data.json' original
    global data

    # Organiza todos os dados digitados pelo usuário em um dicionário único
    register_dict = {} 
    register_dict['id'] = len(data) + 1
    register_dict['description'] = description
    register_dict['value'] = float(value)
    register_dict['category'] = category
    register_dict['type'] = type
    register_dict['date'] = date

    # Adiciona o dicionário dentro da varíavel
    data.append(register_dict)

    # Atualiza o arquivo 'data.json' com os dados adicionado dentro da variável data
    with open('./database/data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Remove um registro no arquivo 'data.json' pelo id
def remove_register_json(id):
    global data
    # Lista auxiliar para a manipulação de dados
    register_dict = []

    # Percorre todos os items dentro dos arquivos armazenados
    for i in data:
        
        # Para todos os items que não são o removido, adicionar na lista auxiliar
        if i['id'] != id:
            i['id'] = len(register_dict)+1
            register_dict.append(i)
    # Adicionar lista auxiliar com todos os items, menos o removido
    data = register_dict

    # Salvar novos dados dentro do arquivo original 'data.json'
    with open('./database/data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Função responsável por atualizar os dados de um determinado registro
def update_register_json(id, description, value, category, type, date):
    global data
    # Percorre todos os items dos dados armazenados
    for i in data:
        # Caso seja o id, adicionar novas informações
        if i['id'] == id:
            i['description'] = description
            i['value'] = float(value)
            i['category'] = category
            i['type'] = type
            i['date'] = date
            break
    # Atualizar dados armazenado com novo registro atualizado
    with open('./database/data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)