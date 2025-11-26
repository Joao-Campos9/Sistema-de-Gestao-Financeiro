from flask import Flask
from routes.home import home_route
from routes.register import register_route


app = Flask(__name__) # Inicialização do Flask
app.register_blueprint(home_route) # Ligação com blueprint da página principal
app.register_blueprint(register_route, url_prefix='/register/') # Blueprint página de registro de entradas e saídas

app.run() # Inicialização da página