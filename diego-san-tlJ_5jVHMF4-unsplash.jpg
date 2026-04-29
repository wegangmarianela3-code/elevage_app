/* ════════════════════════════════════════════════════
   CHEZ VIRGINIE — Frontend Script (API-connected)
   ════════════════════════════════════════════════════ */

const API = '';  // même domaine

const pouletImages = [
  { src: 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=300&q=70', label: 'Lot en croissance – poulailler' },
  { src: 'https://images.unsplash.com/photo-1518492104633-130d0cc84637?w=300&q=70', label: 'Gros poulets de chair' },
  { src: 'https://images.unsplash.com/photo-1612170153139-6f881ff067e0?w=300&q=70', label: 'Poulets en ferme – arrivage frais' },
  { src: 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&q=70', label: 'Sélection premium – lot A' },
  { src: 'https://images.unsplash.com/photo-1621570169574-4b39b6a32090?w=300&q=70', label: 'Poulets plumés – prêts à cuire' },
  { src: 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=300&q=70', label: 'Lot conditionné – livraison' }
];

const porcImages = [
  { src: 'https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb?w=300&q=70', label: 'Porc adulte – pâturage' },
  { src: 'https://images.unsplash.com/photo-1574068468668-a05a11f871da?w=300&q=70', label: 'Beau spécimen – sélection' },
  { src: 'https://images.unsplash.com/photo-1615947534769-80d45c7f50c0?w=300&q=70', label: 'Porcelet – poids léger' },
  { src: 'https://images.unsplash.com/photo-1528190336454-13cd56b45b5a?w=300&q=70', label: 'Gros porc – qualité supérieure' },
  { src: 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=300&q=70', label: 'Élevage régional – fermier' },
  { src: 'https://images.unsplash.com/photo-1574068468668-a05a11f871da?w=300&q=70', label: 'Porc moyen – bon état' }
];

const DATA = {
  poulet: {
    sizes: [
      { id: 'p1', label: 'Petit Poulet',  price: 3500 },
      { id: 'p2', label: 'Moyen Poulet',  price: 4500 },
      { id: 'p3', label: 'Gros Poulet',   price: 6000 }
    ]
  },
  porc: {
    sizes: [
      { id: 's1', label: 'Porcelet',          price: 55000  },
      { id: 's2', label: 'Porc Moyen',         price: 150000 },
      { id: 's3', label: 'Gros Porc',          price: 350000 },
      { id: 's4', label: 'Énorme Spécimen',    price: 700000 }
    ]
  }
};

let selection = { animal: null, size: null, state: 'vivant', services: [], qty: 1, specimen: null };
let deliveryVal = 0;
let deliveryLabel = 'Retrait boutique';
let historique = [];
let pendingSpecimenIndex = null;

// ════ ÉTAPE 1 : Animal ════
function selectAnimal(type) {
  selection.animal = type;
  selection.size = null; selection.specimen = null; selection.services = [];

  ['card-state','card-services','card-final','price-box'].forEach(id =>
    document.getElementById(id).classList.add('hidden'));
  document.getElementById('btn-order').disabled = true;
  document.getElementById('btn-order').textContent = 'Compléter la sélection';

  document.querySelectorAll('.animal-card').forEach(b => b.classList.remove('selected'));
  document.getElementById('opt-' + type).classList.add('selected');
  document.getElementById('card-size').classList.remove('hidden');

  // Hint plumage
  document.getElementById('plume-price-hint').textContent =
    type === 'poulet' ? '+250 FCFA' : '+12 000 FCFA';

  // Step number
  document.getElementById('step-final-num').textContent =
    type === 'porc' ? '5' : '4';

  // Tailles
  const cont = document.getElementById('opts-size');
  cont.innerHTML = '';
  DATA[type].sizes.forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'size-row';
    btn.id = 'size-' + s.id;
    btn.innerHTML = `<span>${s.label}</span><span class="size-row-price">${s.price.toLocaleString()} FCFA</span>`;
    btn.onclick = () => selectSize(s, btn);
    cont.appendChild(btn);
  });

  refreshStock();
  updatePrice();
}

// ════ ÉTAPE 2 : Taille ════
function selectSize(sizeObj, btn) {
  selection.size = sizeObj;
  document.querySelectorAll('.size-row').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  document.getElementById('card-state').classList.remove('hidden');
  updatePrice();
}

// ════ GALERIE ════
function refreshStock() {
  if (!selection.animal) return;
  selection.specimen = null;
  document.getElementById('card-final').classList.add('hidden');
  document.getElementById('card-services').classList.add('hidden');

  const gallery = document.getElementById('stock-gallery');
  gallery.innerHTML = '';
  const images = selection.animal === 'poulet' ? pouletImages : porcImages;

  images.forEach((imgData, i) => {
    const div = document.createElement('div');
    div.className = 'stock-item'; div.id = 'stock-item-' + i;

    const img = document.createElement('img');
    img.src = imgData.src; img.alt = imgData.label;
    img.onerror = function() {
      this.style.display = 'none';
      div.classList.add('img-error');
      div.innerHTML += `<span class="img-fallback">${selection.animal === 'poulet' ? '🐔' : '🐷'}<br><small>${imgData.label}</small></span>`;
    };

    const lbl = document.createElement('div');
    lbl.className = 'stock-label'; lbl.textContent = imgData.label;

    const zoom = document.createElement('button');
    zoom.className = 'zoom-btn'; zoom.textContent = '🔍';
    zoom.onclick = e => { e.stopPropagation(); openSpecimenModal(i, imgData); };

    div.append(img, lbl, zoom);
    div.onclick = () => selectSpecimen(i, imgData, div);
    gallery.appendChild(div);
  });
}

function selectSpecimen(index, imgData, divEl) {
  document.querySelectorAll('.stock-item').forEach(d => d.classList.remove('selected'));
  divEl.classList.add('selected');
  selection.specimen = index + 1;
  selection.specimenData = imgData;
  document.getElementById('card-final').classList.remove('hidden');
  if (selection.animal === 'porc') document.getElementById('card-services').classList.remove('hidden');
  updatePrice();
}

function openSpecimenModal(index, imgData) {
  pendingSpecimenIndex = index;
  document.getElementById('specimen-zoom-img').src = imgData.src;
  document.getElementById('specimen-zoom-label').textContent = imgData.label;
  document.getElementById('modal-specimen').classList.remove('hidden');
}
function closeSpecimenModal() {
  document.getElementById('modal-specimen').classList.add('hidden');
  pendingSpecimenIndex = null;
}
function confirmSpecimen() {
  if (pendingSpecimenIndex === null) return;
  const images = selection.animal === 'poulet' ? pouletImages : porcImages;
  const imgData = images[pendingSpecimenIndex];
  document.querySelectorAll('.stock-item').forEach(d => d.classList.remove('selected'));
  const t = document.getElementById('stock-item-' + pendingSpecimenIndex);
  if (t) t.classList.add('selected');
  selection.specimen = pendingSpecimenIndex + 1;
  selection.specimenData = imgData;
  document.getElementById('card-final').classList.remove('hidden');
  if (selection.animal === 'porc') document.getElementById('card-services').classList.remove('hidden');
  closeSpecimenModal();
  updatePrice();
}

// ════ ÉTAT ════
function selectState(s) {
  selection.state = s;
  document.querySelectorAll('.state-card').forEach(b => b.classList.remove('selected'));
  document.getElementById('state-' + s).classList.add('selected');
  updatePrice();
}

// ════ SERVICES ════
function toggleService(s) {
  if (selection.services.includes(s)) {
    selection.services = selection.services.filter(x => x !== s);
    document.getElementById('chk-' + s).classList.remove('selected');
  } else {
    selection.services.push(s);
    document.getElementById('chk-' + s).classList.add('selected');
  }
  updatePrice();
}

// ════ QUANTITÉ ════
function changeQty(n) {
  let q = parseInt(document.getElementById('qty-display').textContent) + n;
  if (q < 1) q = 1;
  document.getElementById('qty-display').textContent = q;
  selection.qty = q;
  updatePrice();
}

// ════ LIVRAISON ════
function selectDelivery(btn, val, label) {
  document.querySelectorAll('.delivery-opt').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  deliveryVal = val;
  deliveryLabel = label;
  updatePrice();
}

// ════ CALCUL PRIX ════
function updatePrice() {
  if (!selection.size || !selection.specimen) { validateButton(); return; }

  let base = selection.size.price;
  if (selection.state === 'plume') base += (selection.animal === 'poulet' ? 250 : 12000);
  if (selection.services.includes('decoupe')) base += 3000;
  if (selection.services.includes('boyaux'))  base += 4000;

  const qty = parseInt(document.getElementById('qty-display').textContent);
  const total = base * qty + deliveryVal;

  document.getElementById('price-box').classList.remove('hidden');
  document.getElementById('pr-total').textContent = total.toLocaleString() + ' FCFA';
  validateButton();
}

function validateButton() {
  const nom = document.getElementById('inp-nom').value.trim();
  const tel = document.getElementById('inp-tel').value.trim();
  const btn = document.getElementById('btn-order');
  const ready = !!(nom && tel && selection.specimen && selection.size);
  btn.disabled = !ready;
  btn.textContent = ready ? '🛒 Confirmer la commande' : 'Compléter la sélection';
}

// ════ ONGLETS ════
function switchTab(t, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + t).classList.add('active');
}

// ════ RÉCAP ════
function openRecap() {
  const nom = document.getElementById('inp-nom').value.trim();
  const tel = document.getElementById('inp-tel').value.trim();
  const adresse = document.getElementById('inp-adresse').value.trim();
  const qty = parseInt(document.getElementById('qty-display').textContent);
  const total = document.getElementById('pr-total').textContent;
  const etatLabel = selection.state === 'vivant' ? '🐾 Vivant' : '✂️ Plumé/Brûlé';
  const svcsLabel = selection.services.length
    ? selection.services.map(s => s === 'decoupe' ? '🔪 Découpe' : '🧹 Boyaux').join(', ')
    : 'Aucun';
  const specimenData = selection.specimenData;

  document.getElementById('recap-content').innerHTML = `
    ${specimenData ? `<div class="recap-specimen"><img src="${specimenData.src}" alt="${specimenData.label}"/><small>${specimenData.label}</small></div>` : ''}
    <table class="recap-table">
      <tr><td>👤 Client</td><td><strong>${nom}</strong></td></tr>
      <tr><td>📞 Téléphone</td><td>${tel}</td></tr>
      ${adresse ? `<tr><td>📍 Adresse</td><td>${adresse}</td></tr>` : ''}
      <tr><td>🐾 Animal</td><td>${selection.animal === 'poulet' ? '🐔 Poulet' : '🐷 Porc'}</td></tr>
      <tr><td>⚖️ Grosseur</td><td>${selection.size.label}</td></tr>
      <tr><td>🏷️ État</td><td>${etatLabel}</td></tr>
      ${selection.animal === 'porc' ? `<tr><td>🔧 Services</td><td>${svcsLabel}</td></tr>` : ''}
      <tr><td>🔢 Quantité</td><td>${qty}</td></tr>
      <tr><td>🚚 Livraison</td><td>${deliveryLabel}</td></tr>
      <tr class="total-row"><td>💰 TOTAL</td><td><strong>${total}</strong></td></tr>
    </table>`;
  document.getElementById('modal-recap').classList.remove('hidden');
}
function closeRecap() { document.getElementById('modal-recap').classList.add('hidden'); }

// ════ CONFIRMATION (POST vers API) ════
async function confirmOrder() {
  const nom = document.getElementById('inp-nom').value.trim();
  const tel = document.getElementById('inp-tel').value.trim();
  const adresse = document.getElementById('inp-adresse').value.trim();
  const qty = parseInt(document.getElementById('qty-display').textContent);
  const totalStr = document.getElementById('pr-total').textContent.replace(/[^\d]/g, '');
  const total = parseInt(totalStr) || 0;

  const payload = {
    nom, telephone: tel, adresse,
    animal: selection.animal,
    grosseur: selection.size.label,
    prix_unitaire: selection.size.price,
    etat: selection.state,
    services: selection.services,
    quantite: qty,
    livraison: deliveryLabel,
    cout_livraison: deliveryVal,
    total,
    specimen_num: selection.specimen
  };

  try {
    const res = await fetch(API + '/api/commandes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    const orderId = data.id || '?';

    // Ajouter à historique local
    historique.unshift({
      id: orderId, nom, tel, total: total.toLocaleString() + ' FCFA',
      animal: selection.animal, size: selection.size.label,
      qty, state: selection.state, services: [...selection.services],
      statut: 'en_attente',
      date: new Date().toLocaleDateString('fr-FR') + ' à ' + new Date().toLocaleTimeString('fr-FR', {hour:'2-digit', minute:'2-digit'})
    });
    renderHistorique();
    closeRecap();
    document.getElementById('success-msg').textContent =
      `Merci ${nom} ! Commande #${orderId} (${total.toLocaleString()} FCFA) enregistrée. Nous vous contacterons au ${tel}.`;
    document.getElementById('modal-success').classList.remove('hidden');
  } catch (err) {
    // Fallback hors-ligne
    const id = historique.length + 1;
    historique.unshift({
      id, nom, tel, total: total.toLocaleString() + ' FCFA',
      animal: selection.animal, size: selection.size.label,
      qty, state: selection.state, services: [...selection.services],
      statut: 'en_attente',
      date: new Date().toLocaleDateString('fr-FR') + ' à ' + new Date().toLocaleTimeString('fr-FR', {hour:'2-digit', minute:'2-digit'})
    });
    renderHistorique();
    closeRecap();
    document.getElementById('success-msg').textContent =
      `Merci ${nom} ! Commande #${id} enregistrée localement.`;
    document.getElementById('modal-success').classList.remove('hidden');
  }
}

function closeSuccess() {
  document.getElementById('modal-success').classList.add('hidden');
  resetForm();
}

// ════ RESET ════
function resetForm() {
  selection = { animal: null, size: null, state: 'vivant', services: [], qty: 1, specimen: null };
  deliveryVal = 0; deliveryLabel = 'Retrait boutique';
  ['inp-nom','inp-tel','inp-adresse'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('qty-display').textContent = '1';
  ['card-size','card-state','card-services','card-final','price-box'].forEach(id =>
    document.getElementById(id).classList.add('hidden'));
  document.querySelectorAll('.animal-card,.size-row,.state-card,.service-row,.delivery-opt').forEach(b => b.classList.remove('selected'));
  const btn = document.getElementById('btn-order');
  btn.disabled = true; btn.textContent = 'Compléter la sélection';
  window.scrollTo({ top: 0, behavior: 'smooth' });
  // Sélectionner livraison par défaut
  const defDlv = document.querySelector('.delivery-opt[data-value="0"]');
  if (defDlv) defDlv.classList.add('selected');
}

// ════ HISTORIQUE ════
function renderHistorique() {
  const list = document.getElementById('historique-list');
  const badge = document.getElementById('hist-badge');
  badge.textContent = historique.length;
  if (!historique.length) {
    list.innerHTML = '<p class="empty-msg">Aucune commande pour l\'instant.</p>';
    return;
  }
  list.innerHTML = historique.map(c => {
    const svcs = c.services.length ? c.services.map(s => s==='decoupe'?'Découpe':'Boyaux').join(', ') : '';
    const statutClass = `statut-${c.statut || 'en_attente'}`;
    return `<div class="histo-item">
      <div class="histo-header">
        <span class="histo-num">Commande #${c.id}</span>
        <span class="histo-date">${c.date}</span>
      </div>
      <div class="histo-body">
        <span>${c.animal === 'poulet' ? '🐔' : '🐷'} ${c.size} × ${c.qty} (${c.state==='vivant'?'Vivant':'Plumé/Brûlé'})</span>
        <strong>${c.total}</strong>
      </div>
      ${svcs ? `<div class="histo-services">🔧 ${svcs}</div>` : ''}
      <div class="histo-client">👤 ${c.nom} — 📞 ${c.tel}</div>
      <span class="histo-statut ${statutClass}">${c.statut?.replace('_', ' ') || 'en attente'}</span>
    </div>`;
  }).join('');
}

// Charger historique depuis API au démarrage
async function loadHistoriqueFromAPI() {
  try {
    const res = await fetch(API + '/api/commandes');
    const data = await res.json();
    historique = data.map(c => ({
      id: c.id, nom: c.nom, tel: c.telephone,
      total: c.total.toLocaleString() + ' FCFA',
      animal: c.animal, size: c.grosseur,
      qty: c.quantite, state: c.etat,
      services: c.services, statut: c.statut,
      date: c.created_at.substring(0,16).replace('T', ' à ')
    }));
    renderHistorique();
  } catch (e) { /* offline, garder vide */ }
}

document.addEventListener('DOMContentLoaded', () => {
  // Sélection livraison par défaut
  const defDlv = document.querySelector('.delivery-opt[data-value="0"]');
  if (defDlv) defDlv.classList.add('selected');
  loadHistoriqueFromAPI();
});
