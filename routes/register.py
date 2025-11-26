from flask import Blueprint, render_template, request, redirect
from datetime import datetime
from utils.datastorage import add_register_json, return_json, remove_register_json, update_register_json, list_years

# Criação da blueprint de registro
register_route = Blueprint('register', __name__)

# Pega a data atual que é usada para redirecionar até a página correspondente
actual_date = datetime.now().strftime("%Y-%m-%d")

# Criação da rota da blueprint, no caso '/register/'
@register_route.route('/<int:month>/<int:year>')
def register_home(month, year):
    REGISTER = return_json() # Salva os dados do arquivo JSON em uma variável
    listYears = list_years()
    return render_template('registration.html', registry=REGISTER, month=month, year=year, actual_date=actual_date, listYears=listYears) # Rendererizar página com as variáveis

@register_route.route('/new', methods=['POST']) # Pegas as informações do formulário do método POST
def add_reigster():
    # Pede as informações do formulário
    description = request.form.get("description")
    value = request.form.get("value")
    category = request.form.get("category")
    type = request.form.get("type")
    date = request.form.get("date")
    # Módulo 'datastorage' responsável por salvar os dados adicionados no JSON
    add_register_json(description, value, category, type, date)
    # Redireciona para a página com mês e ano escolhidos pelo usuário
    return redirect(f'/register/{date[5:7]}/{date[0:4]}')

# Rota responsável por deletar um registro
@register_route.route('/delete/<int:id>/<int:month>/<int:year>', methods=['POST'])
def remover_register(id, month, year):
    #  Módulo 'datastorage' que é responsável por tirar as informações do JSON
    remove_register_json(id)
    # Redireciona para o mês e ano atual
    return redirect(f'/register/{month}/{year}')

# Rota de edição do registro pelo id
@register_route.route('/edit/<int:id>', methods=['POST'])
def edit_register(id):
    # Retorna toda a base dados
    REGISTER = return_json()

    # Cria uma variável com apenas o id selecionado
    registry = REGISTER[id-1]

    # Renderiza toda a página apenas com os dados do id atual
    return render_template('register_edit.html', registry=registry)

# Rota de atualização atráves do id
@register_route.route('/update/<int:id>', methods=['POST'])
def update_register(id):
    # Salva todos os dados fornecido pelo usuário nos formulários
    description = request.form.get("description")
    value = request.form.get("value")
    category = request.form.get("category")
    type = request.form.get("type")
    date = request.form.get("date")

    # Chama função que atualiza o arquivo JSON
    update_register_json(id, description, value, category, type, date)

    # Redirecionar para o mes e ano daquele determinado registro
    return redirect(f'/register/{date[5:7]}/{date[0:4]}')

# Rota para o filtro dos registro por mês e ano
@register_route.route('/search', methods=['POST'])
def search_route():
    # Salva entradas do usuário
    month = request.form.get("select_month")
    year = request.form.get("select_year")

    # Redireciona para a página correspondente ao mês e ano
    return redirect(f'/register/{month}/{year}')