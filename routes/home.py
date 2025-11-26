"""
Blueprint responsável por organizar todos os dados registrados e organizar em dashboards. Esse módulo utiliza da biblioteca datetime, para salvar o horário local da máquina e utiliza as funções do módulo 'finance', módulo responsável pela extração e cálculo dos dados cadastrados pelo usuário.
"""

from flask import Blueprint, render_template, redirect, url_for, request
from datetime import datetime
import utils.finance as finance

actual_date = datetime.now().strftime("%Y-%m-%d") # Pega a data atual que é usada para redirecionar até a página correspondente

# Criação da blueprint
home_route = Blueprint('home', __name__)

@home_route.route('/') # Rota principal da blueprint, no caso '/'
def home_main():
    # Fatiamaneto de strings
    month = int(actual_date[5:7]) # Salva o mês em uma variável
    year = int(actual_date[0:4]) # Salva o ano em uma variável
    return redirect(url_for('home.home_main_page', month=month, year=year)) # redireciona para a página correspondente ao mes e ano

# Rota principal da blueprint, no caso '/mes/ano'
@home_route.route('/<int:month>/<int:year>') 
def home_main_page(month, year):
    # Pega todos os dados coletados dos registros e extrai para o template 'index.html'
    statistics = finance.json_filtred_date(month, year) 

    month = finance.return_month_text(month)

    # Carrega página principal com os dados e coloca na dashboard principal
    return render_template('index.html', statistics=statistics, month=month, year=year) 

# Rota que filtra os dados escolhidos pelo usuário, no caso mês e ano, e redireciona para a página correspondente
@home_route.route('/search', methods=['POST'])
def search_route():
    # Obtêm informações do formulário e redireciona
    month = request.form.get("select_month") 
    year = request.form.get("select_year")
    return redirect(f'/{month}/{year}')
