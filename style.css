/* ═══════════════════════════════════════════════
   DASHBOARD — Analytics JavaScript
   ═══════════════════════════════════════════════ */

const COLORS = {
  forest: '#2d5a27', amber: '#c9782a', blue: '#4a7ade', red: '#c0392b',
  green2: '#27ae60', purple: '#8e44ad', teal: '#16a085', orange: '#e67e22'
};

const PALETTE = [COLORS.forest, COLORS.amber, COLORS.blue, COLORS.red, COLORS.green2, COLORS.purple, COLORS.teal];

let charts = {};

function destroyChart(id) {
  if (charts[id]) { charts[id].destroy(); delete charts[id]; }
}

// ════ SEED ════
async function seedData() {
  const btn = document.querySelector('.seed-btn');
  btn.textContent = '⏳ Insertion...'; btn.disabled = true;
  try {
    const res = await fetch('/api/seed', { method: 'POST' });
    const d = await res.json();
    alert(d.message);
    loadAll();
  } catch(e) { alert('Erreur: ' + e.message); }
  finally { btn.textContent = '⚡ Données démo'; btn.disabled = false; }
}

// ════ LOAD ALL ════
async function loadAll() {
  document.getElementById('last-update').textContent = 'Actualisation...';
  try {
    const [global, dist] = await Promise.all([
      fetch('/api/stats/global').then(r => r.json()),
      fetch('/api/stats/distribution').then(r => r.json())
    ]);
    renderKPIs(global);
    renderChartAnimal(global.par_animal);
    renderChartLivraison(global.par_livraison);
    renderChartEtat(global.par_etat);
    renderChartDistribution(dist);
    renderChartEvolution(global.evolution);
    renderGrosseurs(global.par_grosseur);
    renderStatsTable(global.stats_montants);
    renderTopClients(global.top_clients);
    document.getElementById('last-update').textContent =
      'Mis à jour le ' + new Date().toLocaleString('fr-FR');
  } catch(e) {
    document.getElementById('last-update').textContent = 'Erreur de chargement — serveur hors ligne?';
  }
}

// ════ KPIs ════
function renderKPIs(data) {
  const r = data.resume;
  document.getElementById('kpi-total').textContent = r.total_commandes || 0;
  document.getElementById('kpi-revenu').textContent = (r.revenu_total || 0).toLocaleString() + ' FCFA';
  document.getElementById('kpi-livrees').textContent = r.commandes_livrees || 0;
  document.getElementById('kpi-taux').textContent = `Taux: ${r.taux_livraison || 0}%`;
  const panier = r.total_commandes ? Math.round(r.revenu_total / r.total_commandes) : 0;
  document.getElementById('kpi-panier').textContent = panier.toLocaleString();
}

// ════ CHART: Animal ════
function renderChartAnimal(data) {
  destroyChart('animal');
  if (!data || !data.length) return;
  const ctx = document.getElementById('chart-animal').getContext('2d');
  charts['animal'] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.map(d => d.animal === 'poulet' ? '🐔 Poulet' : '🐷 Porc'),
      datasets: [{ data: data.map(d => d.n), backgroundColor: [COLORS.amber, COLORS.forest], borderWidth: 0, hoverOffset: 6 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { font: { size: 11 } } } } }
  });
}

// ════ CHART: Livraison ════
function renderChartLivraison(data) {
  destroyChart('livraison');
  if (!data || !data.length) return;
  const ctx = document.getElementById('chart-livraison').getContext('2d');
  charts['livraison'] = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: data.map(d => d.livraison),
      datasets: [{ data: data.map(d => d.n), backgroundColor: PALETTE, borderWidth: 0, hoverOffset: 6 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } } }
  });
}

// ════ CHART: État ════
function renderChartEtat(data) {
  destroyChart('etat');
  if (!data || !data.length) return;
  const ctx = document.getElementById('chart-etat').getContext('2d');
  const labels = data.map(d => d.etat === 'vivant' ? '🐾 Vivant' : '✂️ Plumé/Brûlé');
  charts['etat'] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{ data: data.map(d => d.n), backgroundColor: [COLORS.blue, COLORS.red], borderWidth: 0, hoverOffset: 6 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { font: { size: 11 } } } } }
  });
}

// ════ CHART: Distribution ════
function renderChartDistribution(data) {
  destroyChart('distribution');
  if (!data || !data.bins || !data.bins.length) return;
  const ctx = document.getElementById('chart-distribution').getContext('2d');
  charts['distribution'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.bins,
      datasets: [{
        label: 'Nombre de commandes',
        data: data.values,
        backgroundColor: COLORS.forest + 'cc',
        borderColor: COLORS.forest,
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 1, font: { size: 11 } }, grid: { color: '#f0f0f0' } },
        x: { ticks: { font: { size: 10 } }, grid: { display: false } }
      }
    }
  });
}

// ════ CHART: Évolution ════
function renderChartEvolution(data) {
  destroyChart('evolution');
  if (!data || !data.length) return;
  const ctx = document.getElementById('chart-evolution').getContext('2d');
  charts['evolution'] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(d => d.jour),
      datasets: [
        {
          label: 'Commandes',
          data: data.map(d => d.n),
          borderColor: COLORS.forest, backgroundColor: COLORS.forest + '18',
          fill: true, tension: 0.4, yAxisID: 'y1',
          pointRadius: 4, pointHoverRadius: 6
        },
        {
          label: 'Revenu (FCFA)',
          data: data.map(d => d.revenu),
          borderColor: COLORS.amber, backgroundColor: 'transparent',
          borderDash: [5,4], tension: 0.4, yAxisID: 'y2',
          pointRadius: 3
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { position: 'top', labels: { font: { size: 11 } } } },
      scales: {
        y1: { type: 'linear', position: 'left', beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#f0f0f0' } },
        y2: { type: 'linear', position: 'right', beginAtZero: true, grid: { display: false } },
        x: { ticks: { font: { size: 9 } }, grid: { display: false } }
      }
    }
  });
}

// ════ CHART: Grosseurs ════
function renderGrosseurs(data) {
  const poulet = data.filter(d => d.animal === 'poulet');
  const porc = data.filter(d => d.animal === 'porc');

  destroyChart('grosseur-poulet');
  if (poulet.length) {
    const ctx = document.getElementById('chart-grosseur-poulet').getContext('2d');
    charts['grosseur-poulet'] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: poulet.map(d => d.grosseur),
        datasets: [{ label: 'Commandes', data: poulet.map(d => d.n),
          backgroundColor: COLORS.amber + 'cc', borderColor: COLORS.amber, borderWidth: 1, borderRadius: 5 }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } }, x: { ticks: { font: { size: 9 } } } } }
    });
  }

  destroyChart('grosseur-porc');
  if (porc.length) {
    const ctx = document.getElementById('chart-grosseur-porc').getContext('2d');
    charts['grosseur-porc'] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: porc.map(d => d.grosseur),
        datasets: [{ label: 'Commandes', data: porc.map(d => d.n),
          backgroundColor: COLORS.forest + 'cc', borderColor: COLORS.forest, borderWidth: 1, borderRadius: 5 }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } }, x: { ticks: { font: { size: 9 } } } } }
    });
  }
}

// ════ STATS TABLE ════
function renderStatsTable(stats) {
  const el = document.getElementById('stats-montants-grid');
  if (!stats || !stats.n) { el.innerHTML = '<p style="color:#999;font-size:.85rem">Pas assez de données</p>'; return; }

  const items = [
    { name: 'Effectif (n)', val: stats.n, unit: 'commandes' },
    { name: 'Minimum', val: stats.min?.toLocaleString(), unit: 'FCFA' },
    { name: 'Maximum', val: stats.max?.toLocaleString(), unit: 'FCFA' },
    { name: 'Moyenne', val: stats.mean?.toLocaleString(), unit: 'FCFA' },
    { name: 'Médiane', val: stats.median?.toLocaleString(), unit: 'FCFA' },
    { name: 'Écart-type', val: stats.std?.toLocaleString(), unit: 'FCFA' },
    { name: 'Variance', val: Math.round(stats.variance)?.toLocaleString(), unit: 'FCFA²' },
    { name: 'Q1 (25%)', val: stats.q1?.toLocaleString(), unit: 'FCFA' },
    { name: 'Q3 (75%)', val: stats.q3?.toLocaleString(), unit: 'FCFA' },
    { name: 'IQR', val: stats.iqr?.toLocaleString(), unit: 'FCFA' },
    { name: 'Étendue', val: stats.range?.toLocaleString(), unit: 'FCFA' },
    { name: 'CV (%)', val: stats.cv, unit: '%' }
  ];

  el.innerHTML = items.map(i => `
    <div class="stat-cell">
      <div class="stat-name">${i.name}</div>
      <div class="stat-val">${i.val ?? '—'}</div>
      <div class="stat-unit">${i.unit}</div>
    </div>`).join('');
}

// ════ TOP CLIENTS ════
function renderTopClients(clients) {
  const tbody = document.getElementById('top-clients-body');
  if (!clients || !clients.length) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#999">Aucune donnée</td></tr>';
    return;
  }
  tbody.innerHTML = clients.map((c, i) => `
    <tr>
      <td><strong>#${i + 1}</strong></td>
      <td>${c.nom}</td>
      <td>${c.telephone}</td>
      <td><strong>${c.nb_cmd}</strong></td>
      <td>${(c.total_depense || 0).toLocaleString()} FCFA</td>
    </tr>`).join('');
}

// ════ INIT ════
document.addEventListener('DOMContentLoaded', loadAll);
