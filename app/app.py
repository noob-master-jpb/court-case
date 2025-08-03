from flask import Flask, send_from_directory, render_template
import random

app = Flask(__name__, static_folder='frontend/public', static_url_path='/static')

# Path for our main Svelte page
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
