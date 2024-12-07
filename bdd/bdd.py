import sqlite3

def create_db():
    # Connexion à la base de données (elle sera créée si elle n'existe pas)
    conn = sqlite3.connect('rasa.db')
    c = conn.cursor()
    
    # Création de la table des rendez-vous
    c.execute('''
    CREATE TABLE IF NOT EXISTS rendezvous (
        id INTEGER PRIMARY KEY, 
        user_name TEXT, 
        date TEXT, 
        time TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_db()

def add_rendezvous(user_name, date, time):
    conn = sqlite3.connect('rasa.db')
    c = conn.cursor()
    
    # Insertion d'un rendez-vous dans la table
    c.execute('''
    INSERT INTO rendezvous (user_name, date, time) 
    VALUES (?, ?, ?)
    ''', (user_name, date, time))
    
    conn.commit()
    conn.close()

def get_rendezvous(user_name):
    conn = sqlite3.connect('rasa.db')
    c = conn.cursor()
    
    # Sélectionner le rendez-vous de l'utilisateur
    c.execute('''
    SELECT date, time FROM rendezvous WHERE user_name = ?
    ''', (user_name,))
    
    result = c.fetchone()
    conn.close()
    
    return result
