# 🥩 Chez Virginie — Application de Collecte de Données d'Élevage

Application de collecte et analyse descriptive des données pour INF 232 EC2.

## Structure du projet

```
elevage_app/
├── app.py              # Backend Flask + API REST
├── requirements.txt    # Dépendances Python
├── Procfile            # Déploiement (Render/Railway)
├── templates/
│   ├── index.html      # Interface commande (frontend)
│   └── dashboard.html  # Tableau de bord analytique
├── static/
│   ├── css/
│   │   ├── style.css   # Style page commande
│   │   └── dashboard.css
│   └── js/
│       ├── script.js   # Logique commande
│       └── dashboard.js # Graphiques & stats
└── data/
    └── elevage.db      # Base SQLite (créée automatiquement)
```

## Lancement local

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

## API REST

| Méthode | Endpoint              | Description                  |
|---------|----------------------|------------------------------|
| POST    | /api/commandes        | Créer une commande           |
| GET     | /api/commandes        | Lister toutes les commandes  |
| GET     | /api/commandes/:id    | Détail d'une commande        |
| PUT     | /api/commandes/:id/statut | Mettre à jour le statut |
| GET     | /api/stats/global     | Statistiques descriptives    |
| GET     | /api/stats/animaux/:animal | Stats par animal      |
| GET     | /api/stats/distribution | Distribution des montants  |
| POST    | /api/seed             | Insérer données de démo      |

## Déploiement sur Render.com (gratuit)

1. Créer un compte sur https://render.com
2. New → Web Service → connecter votre dépôt GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Deploy → copier l'URL → envoyer au professeur

## Analyse descriptive disponible

- Effectif, Minimum, Maximum
- Moyenne, Médiane
- Écart-type, Variance
- Quartiles Q1, Q3, IQR
- Étendue, Coefficient de variation
- Graphiques : camembert, histogramme, courbe temporelle
