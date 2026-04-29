<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Dashboard — Chez Virginie Analytics</title>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <link rel="stylesheet" href="/static/css/dashboard.css"/>
</head>
<body>

<div class="dash-layout">

  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-brand">
      <span class="brand-mark">✦</span>
      <div>
        <strong>Chez Virginie</strong>
        <small>Analytics</small>
      </div>
    </div>
    <nav class="sidebar-nav">
      <a href="/" class="nav-link">🛒 Commandes</a>
      <a href="#apercu" class="nav-link active">📊 Aperçu</a>
      <a href="#distribution" class="nav-link">📈 Distribution</a>
      <a href="#animaux" class="nav-link">🐾 Par Animal</a>
      <a href="#evolution" class="nav-link">📅 Évolution</a>
      <a href="#stats-table" class="nav-link">🔢 Statistiques</a>
    </nav>
    <button class="seed-btn" onclick="seedData()">⚡ Données démo</button>
  </aside>

  <!-- Main -->
  <main class="dash-main">
    <header class="dash-topbar">
      <div>
        <h1>Tableau de bord</h1>
        <p id="last-update">Chargement...</p>
      </div>
      <button class="refresh-btn" onclick="loadAll()">🔄 Actualiser</button>
    </header>

    <!-- ── KPI Cards ── -->
    <section id="apercu" class="kpi-grid">
      <div class="kpi-card kpi-green">
        <div class="kpi-label">Commandes totales</div>
        <div class="kpi-value" id="kpi-total">—</div>
        <div class="kpi-sub">Depuis l'ouverture</div>
      </div>
      <div class="kpi-card kpi-amber">
        <div class="kpi-label">Revenu total</div>
        <div class="kpi-value" id="kpi-revenu">—</div>
        <div class="kpi-sub">FCFA cumulés</div>
      </div>
      <div class="kpi-card kpi-blue">
        <div class="kpi-label">Commandes livrées</div>
        <div class="kpi-value" id="kpi-livrees">—</div>
        <div class="kpi-sub" id="kpi-taux">Taux: —%</div>
      </div>
      <div class="kpi-card kpi-red">
        <div class="kpi-label">Panier moyen</div>
        <div class="kpi-value" id="kpi-panier">—</div>
        <div class="kpi-sub">FCFA / commande</div>
      </div>
    </section>

    <!-- ── Charts Row 1 ── -->
    <div class="chart-row">
      <div class="chart-card">
        <h3>Répartition par animal</h3>
        <div class="chart-wrap-sm"><canvas id="chart-animal"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>Mode de livraison</h3>
        <div class="chart-wrap-sm"><canvas id="chart-livraison"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>État de l'animal</h3>
        <div class="chart-wrap-sm"><canvas id="chart-etat"></canvas></div>
      </div>
    </div>

    <!-- ── Distribution des montants ── -->
    <section id="distribution" class="chart-card full-width">
      <h3>Distribution des montants (FCFA)</h3>
      <p class="chart-desc">Histogramme de fréquence des commandes par tranche de prix</p>
      <div class="chart-wrap"><canvas id="chart-distribution"></canvas></div>
    </section>

    <!-- ── Évolution temporelle ── -->
    <section id="evolution" class="chart-card full-width">
      <h3>Évolution des commandes</h3>
      <p class="chart-desc">Nombre de commandes et revenu journalier</p>
      <div class="chart-wrap"><canvas id="chart-evolution"></canvas></div>
    </section>

    <!-- ── Grosseurs ── -->
    <div class="chart-row">
      <div class="chart-card">
        <h3>Grosseurs — Poulet</h3>
        <div class="chart-wrap-sm"><canvas id="chart-grosseur-poulet"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>Grosseurs — Porc</h3>
        <div class="chart-wrap-sm"><canvas id="chart-grosseur-porc"></canvas></div>
      </div>
    </div>

    <!-- ── Stats Table ── -->
    <section id="stats-table" class="chart-card full-width">
      <h3>Statistiques descriptives — Montants des commandes</h3>
      <p class="chart-desc">Indicateurs clés de tendance centrale et de dispersion</p>
      <div class="stats-grid" id="stats-montants-grid"></div>
    </section>

    <!-- ── Top Clients ── -->
    <section class="chart-card full-width">
      <h3>Top 5 Clients</h3>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr><th>#</th><th>Client</th><th>Téléphone</th><th>Commandes</th><th>Total dépensé</th></tr>
          </thead>
          <tbody id="top-clients-body"></tbody>
        </table>
      </div>
    </section>

  </main>
</div>

<script src="/static/js/dashboard.js"></script>
</body>
</html>
