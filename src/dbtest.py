import sqlite3

# Connexion à la base de données
new_con = sqlite3.connect(r"C:\Users\22206844\Desktop\toudou-0.1\data\testdata.db")
new_cur = new_con.cursor()

# Création de la table movie
new_cur.execute("CREATE TABLE IF NOT EXISTS movie(title TEXT, year INTEGER, score REAL)")

# Ajout de données fictives dans la table movie
movies_data = [
    ("Monty Python and the Holy Grail", 1975, 8.2),
    ("Monty Python's Life of Brian", 1979, 8.1),
    ("Monty Python's The Meaning of Life", 1983, 7.6)
]
new_cur.executemany("INSERT INTO movie(title, year, score) VALUES (?, ?, ?)", movies_data)
new_con.commit()

# Sélection des données dans la table movie ordonnées par score décroissant
new_cur.execute("SELECT title, year FROM movie ORDER BY score DESC")

# Récupération du premier résultat (le film avec le score le plus élevé)
result = new_cur.fetchone()

# Affichage des résultats
if result:
    title, year = result
    print(f"The highest scoring Monty Python movie is {title!r}, released in {year}")
else:
    print("No data found")

# Fermeture de la connexion à la base de données
new_con.close()
