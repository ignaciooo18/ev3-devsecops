from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/')
def home():
    return "<h1>Aplicacion Segura - DevSecOps</h1>"

@app.route('/hello')
def hello():
    name = escape(request.args.get('name', 'Invitado'))
    return f"<h2>Hola, {name}!</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)