from flask import Flask
from database import mysql
from blueprints.users import user
from blueprints.bonos import bono

app = Flask(__name__)
app.register_blueprint(user, url_prefix="/")
app.register_blueprint(bono, url_prefix="/bono")

# Connect to data base
app.secret_key = 'mysecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bonos_app'
# Initialize MySQL
mysql.init_app(app)





if __name__ == '__main__':
    app.run(port = 5000, debug= True)