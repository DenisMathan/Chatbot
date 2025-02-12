import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import threading
from chatbot.LeChat import Chatbot
from perception.Perception import Perception

# Initialisierung der Flask-Anwendung
app = Flask(__name__)

# Konfiguration der Anwendung
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialisierung der Erweiterungen
csrf = CSRFProtect(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8081/", 'Access-Control-Allow-Origin': '*'}})

# Initialisierung der globalen Variablen
# alfred = Chatbot({"max_tokens": 512})
alfred = Chatbot({})
root_path = os.getenv('ROOT_PATH', "./")
perception = Perception(root_path=root_path, data_path=root_path+'/data.json', chroma_path=root_path+'/chroma/chromaDB')
lock = threading.Lock()

# Importieren der Routen
from app import routes