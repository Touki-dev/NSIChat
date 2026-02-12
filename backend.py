from flask import Flask, render_template, request, make_response, redirect, abort, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
from fonctions import *

app = Flask(__name__, static_folder='public')
app.config['SECRET_KEY'] = 'ta_cle_secrete'
socketio = SocketIO(app)

# Route pour la page d'accueil
@app.route('/')
def index():
    messages = get_messages()
    return render_template('index.html', messages=messages)

# Gestion des messages SocketIO
@socketio.on('send_message')
def handle_send_message(data):
    username = request.cookies.get('username') or data.get('username', 'Anonyme')
    message = data['message']
    save_message(username, message)
    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S") # format : 2026-02-12 21:27:06
    print(date)
    emit('new_message', {'username': username, 'message': message, 'date': temps_ecoule(date)}, broadcast=True)

# Route pour définir le username (via cookie)
@app.route('/set_username', methods=['POST'])
def set_username():
    username = request.form.get('username')
    response = make_response("OK")
    response.set_cookie('username', username, max_age=60*60*24*30)  # Cookie valide 30 jours
    return response

@app.route('/clear_messages')
def clear_messages():
    # Supprimer tous les messages de la base de données
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('DELETE FROM messages')  # Supprime tous les messages
    conn.commit()
    conn.close()

    # Rediriger vers la page d'accueil avec un message de confirmation
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialiser la base de données au démarrage
    socketio.run(app, debug=True)