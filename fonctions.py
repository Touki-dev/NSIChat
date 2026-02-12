from datetime import datetime, timedelta
import sqlite3

def temps_ecoule(date_str: str) -> str:
    """
    Prend une date au format 'YYYY-MM-DD HH:MM:SS'
    et retourne une chaîne comme :
    'à l’instant', 'il y a 3 minutes', 'il y a 2 jours', etc.
    """
    print(date_str)
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "date invalide"

    now = datetime.now()
    delta = now - date - timedelta(hours=1)
    seconds = int(delta.total_seconds())
    # Cas très récent
    if seconds < 10:
        return "à l’instant"
    if seconds < 60:
        return f"il y a {seconds} seconde{'s' if seconds > 1 else ''}"

    minutes = seconds // 60
    if minutes < 60:
        return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"

    hours = minutes // 60
    if hours < 24:
        return f"il y a {hours} heure{'s' if hours > 1 else ''}"

    days = hours // 24
    if days < 30:
        return f"il y a {days} jour{'s' if days > 1 else ''}"

    months = days // 30
    return f"il y a {months} mois"

        
# Initialiser la base de données
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Récupérer les messages depuis la base de données
def get_messages():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT username, message, timestamp FROM messages ORDER BY timestamp ASC')
    messages = [{'username': row[0], 'message': row[1], 'date': temps_ecoule(row[2])} for row in c.fetchall()]
    conn.close()
    return messages

# Insérer un message dans la base de données
def save_message(username, message):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))
    conn.commit()
    conn.close()