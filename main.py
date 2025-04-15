from flask import Flask, jsonify
from dotenv import load_dotenv
from routes.chatgpt import openai_bp
# from routes.wpp_routes import wpp_bp
import responses

load_dotenv()

app = Flask(__name__)

# Registrando blueprints
app.register_blueprint(openai_bp, url_prefix='/chatgpt')

@app.route('/datetime')
def datetime():
    import datetime
    return jsonify(responses.Ok200("success",{ "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "timezone": "America/Sao_Paulo"}))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
