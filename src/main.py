from flask import Flask
from src.routes.search import bp

app = Flask(__name__, static_folder="src/static", template_folder="src/templates")
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True) 