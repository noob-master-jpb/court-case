from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import *






app = Flask(__name__, static_folder='frontend/public', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
migrate = Migrate(app,db)
db.init_app(app)
with app.app_context():
    db.create_all()
    
@app.route("/")
def base():
    return render_template('app.html')

@app.route("/<path:path>")
def spa_routing(path):
    try:
        return send_from_directory('frontend/public', path)
    except:
        return render_template('index.html') 

@app.get("/test")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True,port=8080)
