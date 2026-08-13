const COLORS = {
  CLEAR: "#10b981",
  DARK: "#f59e0b",
  ARTIFACT: "#6b7280",
  REVIEW: "#3b82f6",
};

const VERDICT_ORDER = ["CLEAR", "DARK", "ARTIFACT", "REVIEW"];

let scenes = [];
let currentScene = null;
let currentFilter = "all";
let selectedContactId = null;

async function api(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatLatLon(lat, lon) {
  return `${lat.toFixed(4)}°, ${lon.toFixed(4)}°`;
}

function shortId(contactId) {
  return contactId.split("_").slice(-2).join("_");
}

function verdictDial(p, size = 52) {
  const r = size / 2 - 4;
  const cx = size / 2;
  const cy = size / 2;
  let start = -Math.PI / 2;
  const slices = VERDICT_ORDER.map((v) => {
    const angle = (p[`p_${v.toLowerCase()}`] || 0) * 2 * Math.PI;
    const end = start + angle;
    const large = angle > Math.PI ? 1 : 0;
    const x1 = cx + r * Math.cos(start);
    const y1 = cy + r * Math.sin(start);
    const x2 = cx + r * Math.cos(end);
    const y2 = cy + r * Math.sin(end);
    const d = `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2} Z`;
    const slice = { d, color: COLORS[v], label: v };
    start = end;
    return slice;
  });

  return `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
      <circle cx="${cx}" cy="${cy}" r="${r}" fill="#0b1b2b" />
      ${slices.map((s) => `<path d="${s.d}" fill="${s.color}" stroke="#0b1b2b" stroke-width="1.5" />`).join("")}
      <circle cx="${cx}" cy="${cy}" r="${r * 0.35}" fill="#112233" />
    </svg>
  `;
}

function renderStats(scene) {
  const counts = scene.summary.verdict_counts || {};
  const total = scene.verdicts.length;
  const order = ["DARK", "CLEAR", "ARTIFACT", "REVIEW"];
  document.getElementById("stats").innerHTML = order
    .map(
      (v) => `
      <div class="stat">
        <span class="stat-dot" style="background:${COLORS[v]}"></span>
        ${v}: ${counts[v] || 0}
      </div>
    `
    )
    .join("") + `<div class="stat">Total: ${total}</div>`;

  const date = scene.scene_id.includes("2024")
    ? `2024-${scene.scene_id.split("2024")[1].slice(0, 2)}-${scene.scene_id.split("2024")[1].slice(2, 4)}`
    : escapeHtml(scene.scene_id);
  document.getElementById("scene-meta").textContent = `${date} · ${total} contacts`;
}

function renderAlertList(scene) {
  const container = document.getElementById("alert-list");
  const contactsById = Object.fromEntries(scene.contacts.map((c) => [c.contact_id, c]));

  let items = scene.verdicts;
  if (currentFilter !== "all") {
    items = items.filter((v) => v.verdict === currentFilter);
  }

  // Rank DARK first, then by p_dark descending
  const rank = { DARK: 0, REVIEW: 1, CLEAR: 2, ARTIFACT: 3 };
  items = items.slice().sort((a, b) => {
    if (rank[a.verdict] !== rank[b.verdict]) return rank[a.verdict] - rank[b.verdict];
    return b.p_dark - a.p_dark;
  });

  if (items.length === 0) {
    container.innerHTML = `<div class="empty">No ${currentFilter === "all" ? "" : currentFilter.toLowerCase() + " "}contacts.</div>`;
    return;
  }

  container.innerHTML = items
    .map((v) => {
      const c = contactsById[v.contact_id] || {};
      const selected = v.contact_id === selectedContactId ? "selected" : "";
      const cardId = escapeHtml(shortId(v.contact_id));
      const staticName = v.static_object ? escapeHtml(v.static_object.name) : "—";
      const reason = escapeHtml(v.reasoning || "No reasoning recorded.");
      const thumbUrl = `/api/scenes/${encodeURIComponent(currentScene.scene_id)}/contacts/${encodeURIComponent(v.contact_id)}/thumbnail`;
      return `
      <article class="alert-card verdict-${v.verdict.toLowerCase()} ${selected}"
               data-id="${escapeHtml(v.contact_id)}" role="button" tabindex="0">
        <img class="card-thumb" src="${thumbUrl}" alt="" loading="lazy"
             onerror="this.style.visibility='hidden'" />
        <div class="dial-wrap">${verdictDial(v)}</div>
        <div class="card-main">
          <div class="card-title">
            <span class="verdict-badge ${v.verdict}">${v.verdict}</span>
            <span class="card-id">${cardId}</span>
          </div>
          <div class="card-coords">${formatLatLon(c.center_lat || 0, c.center_lon || 0)}</div>
          <div class="card-reason">${reason}</div>
        </div>
        <div class="card-meta">
          <span>AIS gate: ${v.n_tracks_within_gate || 0}</span>
          <span>p dark: ${(v.p_dark * 100).toFixed(0)}%</span>
          <span>${staticName}</span>
          ${c.persistence?.is_persistent ? `<span class="persist-badge">Persistent (${c.persistence.n_scenes} scenes)</span>` : ""}
        </div>
      </article>
    `;
    })
    .join("");

  container.querySelectorAll(".alert-card").forEach((card) => {
    card.addEventListener("click", () => selectContact(card.dataset.id));
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") selectContact(card.dataset.id);
    });
  });
}

function renderEvidencePanel(v, contact) {
  const panel = document.getElementById("evidence-panel");
  const assoc = v.nearest_association || v.best_association;
  const staticObj = v.static_object;

  const panelId = escapeHtml(shortId(v.contact_id));
  const assocMmsi = assoc?.mmsi ? escapeHtml(assoc.mmsi) : "—";
  const staticName = staticObj?.name ? escapeHtml(staticObj.name) : "—";
  const reason = escapeHtml(v.reasoning || "No reasoning recorded.");
  const zones = contact?.zones || [];

  panel.innerHTML = `
    <div class="evidence">
      <h3>${panelId}</h3>

      <div class="evidence-section">
        <h4>Verdict probabilities</h4>
        <div class="prob-bars">
          ${VERDICT_ORDER.map(
            (cls) => `
            <div class="prob-row">
              <span class="prob-label" style="color:${COLORS[cls]}">${cls}</span>
              <div class="prob-bar">
                <div class="prob-fill ${cls.toLowerCase()}" style="width:${(v[`p_${cls.toLowerCase()}`] * 100).toFixed(1)}%"></div>
              </div>
              <span class="prob-value">${(v[`p_${cls.toLowerCase()}`] * 100).toFixed(1)}%</span>
            </div>
          `
          ).join("")}
        </div>
      </div>

      <div class="evidence-section">
        <h4>Contact geometry</h4>
        <div class="evidence-row">
          <span class="label">Center</span>
          <span class="value">${formatLatLon(contact?.center_lat || 0, contact?.center_lon || 0)}</span>
        </div>
        <div class="evidence-row">
          <span class="label">Width / length</span>
          <span class="value">${contact?.width_m ? contact.width_m.toFixed(0) : "—"} m / ${contact?.length_m ? contact.length_m.toFixed(0) : "—"} m</span>
        </div>
        <div class="evidence-row">
          <span class="label">Detector confidence</span>
          <span class="value">${contact?.confidence ? (contact.confidence * 100).toFixed(1) : "—"}%</span>
        </div>
      </div>

      <div class="evidence-section">
        <h4>AIS context</h4>
        <div class="evidence-row">
          <span class="label">Tracks within gate</span>
          <span class="value">${v.n_tracks_within_gate || 0}</span>
        </div>
        <div class="evidence-row">
          <span class="label">Nearest MMSI</span>
          <span class="value">${assocMmsi}</span>
        </div>
        <div class="evidence-row">
          <span class="label">Distance</span>
          <span class="value">${assoc?.distance_m != null ? assoc.distance_m.toFixed(0) + " m" : "—"}</span>
        </div>
        <div class="evidence-row">
          <span class="label">P(match)</span>
          <span class="value">${assoc?.p_match != null ? (assoc.p_match * 100).toFixed(1) + "%" : "—"}</span>
        </div>
      </div>

      ${
        staticObj
          ? `<div class="evidence-section">
               <h4>Static object</h4>
               <div class="evidence-row">
                 <span class="label">Name</span>
                 <span class="value">${staticName}</span>
               </div>
               <div class="evidence-row">
                 <span class="label">Distance</span>
                 <span class="value">${staticObj.distance_m != null ? staticObj.distance_m.toFixed(0) + " m" : "—"}</span>
               </div>
             </div>`
          : ""
      }

      <div class="evidence-section">
        <h4>Persistence</h4>
        ${
          contact?.persistence?.is_persistent
            ? `<div class="reasoning">
                 ⭐ Persistent contact: seen in ${contact.persistence.n_scenes} scenes within a ${contact.persistence.cluster_size}-contact cluster.
               </div>`
            : `<div class="reasoning">Single-scene sighting; no repeat detections within 500 m in other processed scenes.</div>`
        }
      </div>

      <div class="evidence-section">
        <h4>Zones</h4>
        ${
          zones.length
            ? `<ul class="zone-list">${zones.map((z) => `<li>${escapeHtml(z.name || z.site_id || "Unnamed zone")} <span class="zone-meta">${escapeHtml(z.protection_level || "")}</span></li>`).join("")}</ul>`
            : `<div class="reasoning">No known MPA / EEZ / zone overlap.</div>`
        }
      </div>

      <div class="evidence-section">
        <h4>Reasoning</h4>
        <div class="reasoning">${reason}</div>
      </div>
    </div>
  `;
}

function selectContact(contactId) {
  selectedContactId = contactId;
  const v = currentScene.verdicts.find((x) => x.contact_id === contactId);
  const contact = currentScene.contacts.find((c) => c.contact_id === contactId);
  renderAlertList(currentScene);
  if (v) renderEvidencePanel(v, contact);
}

function loadScene(sceneId) {
  const scene = scenes.find((s) => s.scene_id === sceneId);
  if (!scene) return;
  currentScene = scene;
  selectedContactId = null;
  renderStats(scene);
  renderAlertList(scene);
  document.getElementById("evidence-panel").innerHTML = `<div class="empty">Select a contact to view evidence.</div>`;

  const mapFrame = document.getElementById("map-frame");
  mapFrame.src = `/api/scenes/${encodeURIComponent(sceneId)}/map`;

  const exportLink = document.getElementById("export-csv");
  exportLink.href = `/api/scenes/${encodeURIComponent(sceneId)}/export.csv`;
}

async function init() {
  const data = await api("/api/scenes");
  scenes = data.scenes;

  const select = document.getElementById("scene-select");
  select.innerHTML = scenes
    .map((s) => `<option value="${escapeHtml(s.scene_id)}">${escapeHtml(s.scene_id)}</option>`)
    .join("");

  select.addEventListener("change", (e) => loadScene(e.target.value));

  document.querySelectorAll(".filter-pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-pill").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.dataset.filter;
      if (currentScene) renderAlertList(currentScene);
    });
  });

  if (scenes.length > 0) {
    loadScene(scenes[0].scene_id);
  } else {
    document.getElementById("alert-list").innerHTML = `<div class="empty">No processed scenes found in data/processed.</div>`;
  }
}

init().catch((err) => {
  console.error(err);
  document.getElementById("alert-list").innerHTML = `<div class="empty">Failed to load dashboard: ${err.message}</div>`;
});
