from flask import Flask, render_template, request, redirect, flash
import sqlite3
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "secretkey"

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            culture TEXT,
            region TEXT,
            superficie REAL,
            production REAL,
            prix REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        culture = request.form['culture']
        region = request.form['region']
        superficie = request.form['superficie']
        production = request.form['production']
        prix = request.form['prix']

        if not culture or not region:
            flash("Tous les champs sont obligatoires")
            return redirect('/form')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO data (culture, region, superficie, production, prix) VALUES (?, ?, ?, ?, ?)",
                  (culture, region, superficie, production, prix))
        conn.commit()
        conn.close()

        return redirect('/stats')

    return render_template('form.html')

@app.route('/stats')
def stats():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT culture, production FROM data")
    data = c.fetchall()
    conn.close()

    if data:
        cultures = [d[0] for d in data]
        productions = [d[1] for d in data]

        plt.figure()
        plt.bar(cultures, productions)
        plt.title("Production par culture")
        plt.savefig('static/graph.png')
        plt.close()

    return render_template('stats.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
