"""
╔══════════════════════════════════════════════════════════════╗
║   CHEZ VIRGINIE — Backend Flask                              ║
║   Collecte & Analyse Descriptive des Données d'Élevage       ║
╚══════════════════════════════════════════════════════════════╝
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os
import math
from datetime import datetime
from collections import Counter

app = Flask(__name__)
CORS(app)



DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'elevage.db')

# ══════════════════════════════════════════════
#  BASE DE DONNÉES
# ══════════════════════════════════════════════

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS commandes (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            nom           TEXT NOT NULL,
            telephone     TEXT NOT NULL,
            adresse       TEXT,
            animal        TEXT NOT NULL,
            grosseur      TEXT NOT NULL,
            prix_unitaire REAL NOT NULL,
            etat          TEXT NOT NULL,
            services      TEXT DEFAULT '[]',
            quantite      INTEGER NOT NULL DEFAULT 1,
            livraison     TEXT NOT NULL,
            cout_livraison REAL NOT NULL DEFAULT 0,
            total         REAL NOT NULL,
            specimen_num  INTEGER,
            statut        TEXT NOT NULL DEFAULT 'en_attente',
            created_at    TEXT NOT NULL
        )
    ''')

    # Table des animaux en stock (pour les analyses)
    c.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            animal      TEXT NOT NULL,
            grosseur    TEXT NOT NULL,
            poids_kg    REAL,
            prix        REAL NOT NULL,
            disponible  INTEGER DEFAULT 1,
            created_at  TEXT NOT NULL
        )
    ''')

    # Insérer du stock de démo si vide
    c.execute('SELECT COUNT(*) FROM stock')
    if c.fetchone()[0] == 0:
        stock_demo = [
            ('poulet', 'Petit Poulet',  1.2, 3500),
            ('poulet', 'Petit Poulet',  1.1, 3500),
            ('poulet', 'Moyen Poulet',  1.8, 4500),
            ('poulet', 'Moyen Poulet',  2.0, 4500),
            ('poulet', 'Moyen Poulet',  1.9, 4500),
            ('poulet', 'Gros Poulet',   2.8, 6000),
            ('poulet', 'Gros Poulet',   3.1, 6000),
            ('porc',   'Porcelet',      8.0, 55000),
            ('porc',   'Porcelet',      7.5, 55000),
            ('porc',   'Porc Moyen',   45.0, 150000),
            ('porc',   'Porc Moyen',   50.0, 150000),
            ('porc',   'Gros Porc',    90.0, 350000),
            ('porc',   'Énorme Spécimen', 130.0, 700000),
        ]
        now = datetime.now().isoformat()
        for s in stock_demo:
            c.execute('INSERT INTO stock (animal, grosseur, poids_kg, prix, created_at) VALUES (?,?,?,?,?)',
                      (*s, now))

    conn.commit()
    conn.close()

# ══════════════════════════════════════════════
#  ROUTES PRINCIPALES
# ══════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ══════════════════════════════════════════════
#  API — COMMANDES
# ══════════════════════════════════════════════

@app.route('/api/commandes', methods=['POST'])
def create_commande():
    data = request.get_json()
    required = ['nom', 'telephone', 'animal', 'grosseur', 'prix_unitaire',
                'etat', 'quantite', 'livraison', 'cout_livraison', 'total']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Champ manquant: {field}'}), 400

    conn = get_db()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('''
        INSERT INTO commandes
        (nom, telephone, adresse, animal, grosseur, prix_unitaire, etat,
         services, quantite, livraison, cout_livraison, total, specimen_num, statut, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        data['nom'], data['telephone'], data.get('adresse', ''),
        data['animal'], data['grosseur'], data['prix_unitaire'],
        data['etat'], json.dumps(data.get('services', [])),
        data['quantite'], data['livraison'], data['cout_livraison'],
        data['total'], data.get('specimen_num'), 'en_attente', now
    ))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': new_id, 'message': f'Commande #{new_id} enregistrée'}), 201


@app.route('/api/commandes', methods=['GET'])
def get_commandes():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM commandes ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        row_dict = dict(r)
        row_dict['services'] = json.loads(row_dict['services'] or '[]')
        result.append(row_dict)
    return jsonify(result)


@app.route('/api/commandes/<int:order_id>', methods=['GET'])
def get_commande(order_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM commandes WHERE id = ?', (order_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Commande introuvable'}), 404
    row_dict = dict(row)
    row_dict['services'] = json.loads(row_dict['services'] or '[]')
    return jsonify(row_dict)


@app.route('/api/commandes/<int:order_id>/statut', methods=['PUT'])
def update_statut(order_id):
    data = request.get_json()
    statut = data.get('statut')
    if statut not in ['en_attente', 'confirmee', 'en_preparation', 'livree', 'annulee']:
        return jsonify({'error': 'Statut invalide'}), 400
    conn = get_db()
    conn.execute('UPDATE commandes SET statut=? WHERE id=?', (statut, order_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ══════════════════════════════════════════════
#  API — ANALYSES DESCRIPTIVES
# ══════════════════════════════════════════════

def calc_stats(values):
    """Statistiques descriptives complètes."""
    if not values:
        return {}
    n = len(values)
    mean = sum(values) / n
    sorted_v = sorted(values)
    median = sorted_v[n // 2] if n % 2 else (sorted_v[n//2-1] + sorted_v[n//2]) / 2
    variance = sum((x - mean) ** 2 for x in values) / n
    std = math.sqrt(variance)
    q1 = sorted_v[int(n * 0.25)]
    q3 = sorted_v[int(n * 0.75)]
    return {
        'n': n,
        'min': min(values),
        'max': max(values),
        'mean': round(mean, 2),
        'median': round(median, 2),
        'std': round(std, 2),
        'variance': round(variance, 2),
        'q1': round(q1, 2),
        'q3': round(q3, 2),
        'iqr': round(q3 - q1, 2),
        'range': round(max(values) - min(values), 2),
        'cv': round((std / mean * 100) if mean else 0, 2)
    }


@app.route('/api/stats/global')
def stats_global():
    conn = get_db()
    c = conn.cursor()

    # Totaux généraux
    c.execute('SELECT COUNT(*) as total, COALESCE(SUM(total),0) as revenu FROM commandes')
    totaux = dict(c.fetchone())

    c.execute("SELECT COUNT(*) FROM commandes WHERE statut='livree'")
    livrees = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM commandes WHERE statut='annulee'")
    annulees = c.fetchone()[0]

    # Répartition par animal
    c.execute('SELECT animal, COUNT(*) as n, SUM(total) as revenu FROM commandes GROUP BY animal')
    par_animal = [dict(r) for r in c.fetchall()]

    # Répartition par grosseur
    c.execute('SELECT animal, grosseur, COUNT(*) as n FROM commandes GROUP BY animal, grosseur ORDER BY animal, n DESC')
    par_grosseur = [dict(r) for r in c.fetchall()]

    # Répartition par état
    c.execute("SELECT etat, COUNT(*) as n FROM commandes GROUP BY etat")
    par_etat = [dict(r) for r in c.fetchall()]

    # Répartition par livraison
    c.execute("SELECT livraison, COUNT(*) as n FROM commandes GROUP BY livraison")
    par_livraison = [dict(r) for r in c.fetchall()]

    # Stats sur les totaux
    c.execute('SELECT total FROM commandes')
    totaux_vals = [r[0] for r in c.fetchall()]
    stats_total = calc_stats(totaux_vals)

    # Stats sur les quantités
    c.execute('SELECT quantite FROM commandes')
    qte_vals = [r[0] for r in c.fetchall()]
    stats_qte = calc_stats(qte_vals)

    # Évolution temporelle (par jour)
    c.execute('''SELECT substr(created_at,1,10) as jour, COUNT(*) as n, SUM(total) as revenu
                 FROM commandes GROUP BY jour ORDER BY jour''')
    evolution = [dict(r) for r in c.fetchall()]

    # Services les plus demandés
    c.execute('SELECT services FROM commandes')
    all_services = []
    for row in c.fetchall():
        svcs = json.loads(row[0] or '[]')
        all_services.extend(svcs)
    services_count = dict(Counter(all_services))

    # Top clients (par nombre de commandes)
    c.execute('''SELECT nom, telephone, COUNT(*) as nb_cmd, SUM(total) as total_depense
                 FROM commandes GROUP BY telephone ORDER BY nb_cmd DESC LIMIT 5''')
    top_clients = [dict(r) for r in c.fetchall()]

    conn.close()

    return jsonify({
        'resume': {
            'total_commandes': totaux['total'],
            'revenu_total': round(totaux['revenu'], 0),
            'commandes_livrees': livrees,
            'commandes_annulees': annulees,
            'taux_livraison': round(livrees / totaux['total'] * 100, 1) if totaux['total'] else 0
        },
        'par_animal': par_animal,
        'par_grosseur': par_grosseur,
        'par_etat': par_etat,
        'par_livraison': par_livraison,
        'stats_montants': stats_total,
        'stats_quantites': stats_qte,
        'evolution': evolution,
        'services': services_count,
        'top_clients': top_clients
    })


@app.route('/api/stats/animaux/<animal>')
def stats_animal(animal):
    """Statistiques détaillées par animal."""
    if animal not in ('poulet', 'porc'):
        return jsonify({'error': 'Animal invalide'}), 400

    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT total, quantite, prix_unitaire, grosseur FROM commandes WHERE animal=?', (animal,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    if not rows:
        return jsonify({'message': 'Aucune donnée', 'stats': {}})

    totaux = [r['total'] for r in rows]
    qtes   = [r['quantite'] for r in rows]
    prix   = [r['prix_unitaire'] for r in rows]

    grosseur_count = Counter(r['grosseur'] for r in rows)

    return jsonify({
        'animal': animal,
        'stats_montants': calc_stats(totaux),
        'stats_quantites': calc_stats(qtes),
        'stats_prix_unitaires': calc_stats(prix),
        'grosseur_distribution': dict(grosseur_count),
        'nb_commandes': len(rows)
    })


@app.route('/api/stats/distribution')
def distribution():
    """Distribution des montants pour histogramme."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT total, animal FROM commandes ORDER BY total')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    if not rows:
        return jsonify({'bins': [], 'values': []})

    totaux = [r['total'] for r in rows]
    min_v, max_v = min(totaux), max(totaux)
    n_bins = min(10, max(3, len(totaux) // 3))

    if max_v == min_v:
        return jsonify({'bins': [min_v], 'values': [len(totaux)]})

    step = (max_v - min_v) / n_bins
    bins = [min_v + i * step for i in range(n_bins + 1)]
    counts = [0] * n_bins
    for v in totaux:
        idx = min(int((v - min_v) / step), n_bins - 1)
        counts[idx] += 1

    bin_labels = [f"{int(bins[i]/1000)}k-{int(bins[i+1]/1000)}k" for i in range(n_bins)]
    return jsonify({'bins': bin_labels, 'values': counts, 'raw': totaux})


# ══════════════════════════════════════════════
#  API — STOCK
# ══════════════════════════════════════════════

@app.route('/api/stock')
def get_stock():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM stock ORDER BY animal, grosseur')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(rows)


# ══════════════════════════════════════════════
#  SEED — Données de démonstration
# ══════════════════════════════════════════════

@app.route('/api/seed', methods=['POST'])
def seed_data():
    """Insérer des données de démo pour les analyses."""
    import random
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM commandes')
    count = c.fetchone()[0]
    if count >= 30:
        return jsonify({'message': f'{count} commandes déjà présentes'})

    noms = ['Jean Mbarga', 'Marie Fouda', 'Paul Nkomo', 'Awa Biya', 'Eric Tagne',
            'Christine Mendo', 'Alain Fopa', 'Nadège Essono', 'Bruno Ateba', 'Sylvie Onana']
    animaux = ['poulet', 'poulet', 'poulet', 'porc', 'porc']
    grosseurs_poulet = [('Petit Poulet', 3500), ('Moyen Poulet', 4500), ('Gros Poulet', 6000)]
    grosseurs_porc = [('Porcelet', 55000), ('Porc Moyen', 150000), ('Gros Porc', 350000)]
    etats = ['vivant', 'vivant', 'plume']
    livraisons = [('Retrait boutique', 0), ('Proche', 500), ('Standard', 1000), ('Longue', 1500)]
    statuts = ['livree', 'livree', 'livree', 'confirmee', 'en_attente']

    for i in range(50):
        nom = random.choice(noms)
        animal = random.choice(animaux)
        grosseurs = grosseurs_poulet if animal == 'poulet' else grosseurs_porc
        grosseur, prix_u = random.choice(grosseurs)
        etat = random.choice(etats)
        qty = random.randint(1, 4)
        liv_label, liv_cout = random.choice(livraisons)
        services = []
        if animal == 'porc':
            if random.random() > 0.6: services.append('decoupe')
            if random.random() > 0.7: services.append('boyaux')
        frais_etat = 0
        if etat == 'plume':
            frais_etat = 250 if animal == 'poulet' else 12000
        svc_cout = (3000 if 'decoupe' in services else 0) + (4000 if 'boyaux' in services else 0)
        total = (prix_u + frais_etat + svc_cout) * qty + liv_cout

        # Date aléatoire dans les 30 derniers jours
        day_offset = random.randint(0, 29)
        from datetime import timedelta
        date = (datetime.now() - timedelta(days=day_offset)).isoformat()

        c.execute('''INSERT INTO commandes
            (nom, telephone, adresse, animal, grosseur, prix_unitaire, etat,
             services, quantite, livraison, cout_livraison, total, specimen_num, statut, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (nom, f'6{random.randint(50,99)}{random.randint(100000,999999)}',
             random.choice(['Bastos', 'Melen', 'Biyem-Assi', 'Mvog-Ada', 'Essos', '']),
             animal, grosseur, prix_u, etat, json.dumps(services), qty,
             liv_label, liv_cout, total, random.randint(1,7),
             random.choice(statuts), date))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': '50 commandes de démo insérées'})


# ══════════════════════════════════════════════
#  LANCEMENT
# ══════════════════════════════════════════════

# Initialiser la base de données (compatible gunicorn ET python app.py)
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
