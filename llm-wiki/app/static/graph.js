/* Wissensgraph (/graph): Force-Directed-Graph auf Basis von /api/graph.
 *
 * Die Daten sind bereits serverseitig gefiltert (app/graph.py) - dieses Skript
 * zeigt nur an, was es bekommt, und hat keinen eigenen Zugriffsweg.
 * Kein Framework ausser D3, kein Build-Schritt.
 */
(function () {
  "use strict";

  var wrap = document.getElementById("graph-canvas-wrap");
  var svgEl = document.getElementById("graph-canvas");
  var messageEl = document.getElementById("graph-message");
  var tooltipEl = document.getElementById("graph-tooltip");
  if (!wrap || !svgEl) return;

  function showMessage(text) {
    if (!messageEl) return;
    messageEl.textContent = text;
    messageEl.hidden = false;
    svgEl.style.display = "none";
  }

  if (!window.d3) {
    showMessage(
      "Graph-Bibliothek konnte nicht geladen werden. " +
      "Ohne Internetzugang zum CDN bleibt die Fläche leer - die Daten liegen weiterhin unter /api/graph."
    );
    return;
  }

  var d3 = window.d3;

  // Feste Palette: Marke (Magenta/Orange/Lila/Grau) plus vier weitere Toene.
  var PALETTE = [
    "#e5007d", "#f59342", "#7c4c79", "#b09aac",
    "#2fb8a8", "#4a8fe7", "#8fd14f", "#ffd166"
  ];
  var COLOR_PROPOSAL = "#f59342";
  var COLOR_ROLE = "#b09aac";
  var COLOR_DOMAIN = "#f5eef1";

  var LINK_STYLE = {
    domain: { color: "#5c5560", width: 1.0, dash: null },
    herkunft: { color: "#7c4c79", width: 1.0, dash: "4 3" },
    link: { color: "#e5007d", width: 2.0, dash: null },
    similar: { color: "#4a8fe7", width: 1.0, dash: "2 4" }
  };

  var state = {
    nodes: [],
    links: [],
    showDomain: true,
    showRole: true,
    showSimilar: true,
    query: "",
    hovered: null,
    zoomScale: 1
  };
  var neighbours = {};   // id -> Set der Nachbar-Ids
  var degree = {};       // id -> Grad
  var domainColor = {};

  var svg = d3.select(svgEl);
  var root = svg.append("g").attr("class", "graph-root");
  var linkLayer = root.append("g").attr("class", "graph-links");
  var nodeLayer = root.append("g").attr("class", "graph-nodes");
  var labelLayer = root.append("g").attr("class", "graph-labels");

  var simulation = null;
  var linkSel = null;
  var nodeSel = null;
  var labelSel = null;

  function size() {
    var r = wrap.getBoundingClientRect();
    return { w: Math.max(320, r.width), h: Math.max(240, r.height) };
  }

  function nodeRadius(n) {
    var base = { page: 6, proposal: 6, domain: 11, role: 9 }[n.type] || 6;
    return base + Math.min(9, Math.sqrt(degree[n.id] || 0) * 2.2);
  }

  function nodeFill(n) {
    if (n.type === "domain" || n.type === "role") return "none";
    if (n.type === "proposal") return COLOR_PROPOSAL;
    return domainColor[n.domaene] || PALETTE[3];
  }

  function nodeStroke(n) {
    if (n.type === "domain") return COLOR_DOMAIN;
    if (n.type === "role") return COLOR_ROLE;
    if (n.type === "proposal") return "#3a1d06";
    return "#1c1a1c";
  }

  function nodeShape(n) {
    var r = nodeRadius(n);
    if (n.type === "proposal") {
      // Raute: eigene Form fuer Projektvorschlaege
      return d3.symbol().type(d3.symbolDiamond).size(r * r * 3.4)();
    }
    return d3.symbol().type(d3.symbolCircle).size(Math.PI * r * r)();
  }

  function linkVisible(l) {
    if (l.kind === "similar" && !state.showSimilar) return false;
    var s = typeof l.source === "object" ? l.source : nodeById(l.source);
    var t = typeof l.target === "object" ? l.target : nodeById(l.target);
    return nodeVisible(s) && nodeVisible(t);
  }

  function nodeVisible(n) {
    if (!n) return false;
    if (n.type === "domain") return state.showDomain;
    if (n.type === "role") return state.showRole;
    return true;
  }

  var byId = {};
  function nodeById(id) { return byId[id]; }

  function matchesQuery(n) {
    if (!state.query) return false;
    return (n.label || "").toLowerCase().indexOf(state.query) !== -1;
  }

  function isNear(n) {
    if (!state.hovered) return false;
    if (n.id === state.hovered) return true;
    var set = neighbours[state.hovered];
    return !!(set && set[n.id]);
  }

  function labelVisible(n) {
    if (!nodeVisible(n)) return false;
    if (n.type === "domain" || n.type === "role") return true;   // Hubs immer
    if (state.hovered) return isNear(n);
    if (state.query) return matchesQuery(n);
    return state.zoomScale >= 0.8;
  }

  function nodeOpacity(n) {
    if (!nodeVisible(n)) return 0;
    if (state.hovered) return isNear(n) ? 1 : 0.12;
    if (state.query) return matchesQuery(n) ? 1 : 0.15;
    return 1;
  }

  function linkOpacity(l) {
    if (!linkVisible(l)) return 0;
    var s = l.source.id || l.source;
    var t = l.target.id || l.target;
    if (state.hovered) {
      return (s === state.hovered || t === state.hovered) ? 0.95 : 0.05;
    }
    if (state.query) return 0.12;
    return l.kind === "link" ? 0.75 : 0.4;
  }

  function paint() {
    if (!nodeSel) return;
    nodeSel
      .attr("opacity", nodeOpacity)
      .attr("pointer-events", function (n) { return nodeVisible(n) ? "auto" : "none"; })
      .attr("stroke-width", function (n) { return matchesQuery(n) ? 3 : (n.type === "domain" || n.type === "role" ? 2 : 1.2); })
      .attr("stroke", function (n) { return matchesQuery(n) ? "#ffd166" : nodeStroke(n); });
    linkSel.attr("opacity", linkOpacity);
    labelSel
      .attr("opacity", function (n) { return labelVisible(n) ? (state.hovered && !isNear(n) ? 0.1 : 0.95) : 0; })
      .attr("pointer-events", "none");
  }

  function applyFilters() {
    // Simulation laeuft weiter: ausgeblendete Kanten fallen nur aus der Kraft.
    simulation.force("link").links(state.links.filter(linkVisible));
    simulation.alpha(0.3).restart();
    paint();
  }

  function tooltip(n, event) {
    if (!tooltipEl) return;
    if (!n) { tooltipEl.hidden = true; return; }
    var kind = { page: "Seite", proposal: "Projektvorschlag", domain: "Domäne", role: "Rolle" }[n.type] || n.type;
    var extra = "";
    if (n.type === "page" || n.type === "proposal") {
      extra = "<br>" + (n.domaene || "") + " · " + (n.vertraulichkeit || "");
    }
    tooltipEl.innerHTML = "<strong>" + escapeHtml(n.label) + "</strong><br>" + kind + extra;
    tooltipEl.hidden = false;
    var r = wrap.getBoundingClientRect();
    tooltipEl.style.left = Math.min(r.width - 220, event.clientX - r.left + 14) + "px";
    tooltipEl.style.top = (event.clientY - r.top + 14) + "px";
  }

  function shortLabel(s) {
    var text = String(s == null ? "" : s);
    return text.length > 28 ? text.slice(0, 27).trim() + "…" : text;
  }

  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function render(data) {
    state.nodes = data.nodes || [];
    state.links = (data.links || []).map(function (l) {
      return { source: l.source, target: l.target, kind: l.kind, weight: l.weight };
    });

    if (!state.nodes.length) {
      showMessage(
        "Noch nichts zu sehen: In deiner Sicht gibt es kein Wissen, das sich verknüpfen ließe. " +
        "Lege eine Seite an oder wechsle in der Seitenleiste die Rolle."
      );
      return;
    }

    byId = {};
    state.nodes.forEach(function (n) { byId[n.id] = n; });

    // Domaenen-Farben stabil in alphabetischer Reihenfolge vergeben
    var domains = state.nodes
      .filter(function (n) { return n.type === "page"; })
      .map(function (n) { return n.domaene; })
      .filter(function (d, i, arr) { return d && arr.indexOf(d) === i; })
      .sort();
    domains.forEach(function (d, i) { domainColor[d] = PALETTE[i % PALETTE.length]; });

    degree = {};
    neighbours = {};
    state.links.forEach(function (l) {
      degree[l.source] = (degree[l.source] || 0) + 1;
      degree[l.target] = (degree[l.target] || 0) + 1;
      (neighbours[l.source] = neighbours[l.source] || {})[l.target] = true;
      (neighbours[l.target] = neighbours[l.target] || {})[l.source] = true;
    });

    var dim = size();
    svg.attr("viewBox", "0 0 " + dim.w + " " + dim.h);

    linkSel = linkLayer.selectAll("line")
      .data(state.links)
      .join("line")
      .attr("stroke", function (l) { return (LINK_STYLE[l.kind] || {}).color || "#666"; })
      .attr("stroke-width", function (l) {
        var st = LINK_STYLE[l.kind] || {};
        return l.kind === "similar" ? 0.6 + (l.weight || 0) * 6 : (st.width || 1);
      })
      .attr("stroke-dasharray", function (l) { return (LINK_STYLE[l.kind] || {}).dash; });

    nodeSel = nodeLayer.selectAll("path")
      .data(state.nodes, function (n) { return n.id; })
      .join("path")
      .attr("d", nodeShape)
      .attr("fill", nodeFill)
      .attr("stroke", nodeStroke)
      .attr("stroke-width", 1.2)
      .attr("class", function (n) { return "gnode gnode-" + n.type; })
      .style("cursor", function (n) { return n.url ? "pointer" : "grab"; });

    labelSel = labelLayer.selectAll("text")
      .data(state.nodes, function (n) { return n.id; })
      .join("text")
      .text(function (n) { return shortLabel(n.label); })
      .attr("class", function (n) { return "glabel glabel-" + n.type; })
      .attr("text-anchor", "middle");

    simulation = d3.forceSimulation(state.nodes)
      .force("link", d3.forceLink(state.links)
        .id(function (n) { return n.id; })
        .distance(function (l) {
          if (l.kind === "link") return 65;
          if (l.kind === "domain") return 95;
          if (l.kind === "herkunft") return 130;
          return 140;
        })
        .strength(function (l) {
          if (l.kind === "link") return 0.6;
          if (l.kind === "domain") return 0.35;
          if (l.kind === "herkunft") return 0.12;
          return Math.min(0.5, (l.weight || 0.1) * 2);
        }))
      .force("charge", d3.forceManyBody().strength(-420).distanceMax(900))
      .force("center", d3.forceCenter(dim.w / 2, dim.h / 2))
      .force("collide", d3.forceCollide().radius(function (n) { return nodeRadius(n) + 18; }))
      .on("tick", tick);

    function tick() {
      linkSel
        .attr("x1", function (l) { return l.source.x; })
        .attr("y1", function (l) { return l.source.y; })
        .attr("x2", function (l) { return l.target.x; })
        .attr("y2", function (l) { return l.target.y; });
      nodeSel.attr("transform", function (n) { return "translate(" + n.x + "," + n.y + ")"; });
      labelSel
        .attr("x", function (n) { return n.x; })
        .attr("y", function (n) { return n.y - nodeRadius(n) - 6; });
      if (typeof fitToView === "function") fitToView();
    }

    // Zoom / Pan
    var userMoved = false;
    var zoom = d3.zoom().scaleExtent([0.2, 5]).on("zoom", function (event) {
      if (event.sourceEvent) userMoved = true;   // echte Geste, kein Auto-Fit
      root.attr("transform", event.transform);
      state.zoomScale = event.transform.k;
      paint();
    });
    svg.call(zoom);

    // Einpassen, solange der Nutzer die Kamera nicht selbst angefasst hat: der
    // Graph soll die Flaeche nutzen, egal ob er aus 5 oder 200 Knoten besteht.
    // Auf jedem Tick statt einmalig - sonst passt die Kamera auf Positionen,
    // die die noch laufende Simulation gleich wieder verschiebt.
    function fitToView() {
      if (userMoved || !state.nodes.length) return;
      var xs = [], ys = [];
      state.nodes.forEach(function (n) {
        if (!nodeVisible(n) || !isFinite(n.x) || !isFinite(n.y)) return;
        xs.push(n.x); ys.push(n.y);
      });
      if (!xs.length) return;
      var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
      var y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
      var d = size();
      var pad = 80;
      var bw = Math.max(1, x1 - x0), bh = Math.max(1, y1 - y0);
      var k = Math.max(0.3, Math.min((d.w - 2 * pad) / bw, (d.h - 2 * pad) / bh, 1.8));
      var tx = d.w / 2 - k * (x0 + x1) / 2;
      var ty = d.h / 2 - k * (y0 + y1) / 2;
      // Direkt setzen (kein transition): das laeuft auf jedem Tick.
      zoom.transform(svg, d3.zoomIdentity.translate(tx, ty).scale(k));
    }

    // Drag
    var moved = false;
    nodeSel.call(d3.drag()
      .on("start", function (event, n) {
        moved = false;
        userMoved = true;   // ab jetzt gehoert die Kamera dem Nutzer
        if (!event.active) simulation.alphaTarget(0.25).restart();
        n.fx = n.x; n.fy = n.y;
      })
      .on("drag", function (event, n) {
        moved = true;
        n.fx = event.x; n.fy = event.y;
      })
      .on("end", function (event, n) {
        if (!event.active) simulation.alphaTarget(0);
        n.fx = null; n.fy = null;
      }));

    nodeSel
      .on("mouseenter", function (event, n) {
        state.hovered = n.id;
        tooltip(n, event);
        paint();
      })
      .on("mousemove", function (event, n) { tooltip(n, event); })
      .on("mouseleave", function () {
        state.hovered = null;
        tooltip(null);
        paint();
      })
      .on("click", function (event, n) {
        if (moved) return;           // Ziehen ist kein Klick
        if (n.url) window.location.href = n.url;
      });

    paint();

    window.addEventListener("resize", function () {
      var d = size();
      svg.attr("viewBox", "0 0 " + d.w + " " + d.h);
      simulation.force("center", d3.forceCenter(d.w / 2, d.h / 2));
      simulation.alpha(0.2).restart();
    });
  }

  function bindControls() {
    var search = document.getElementById("graph-search");
    if (search) {
      search.addEventListener("input", function () {
        state.query = search.value.trim().toLowerCase();
        paint();
      });
    }
    [["toggle-domain", "showDomain"], ["toggle-role", "showRole"], ["toggle-similar", "showSimilar"]]
      .forEach(function (pair) {
        var el = document.getElementById(pair[0]);
        if (!el) return;
        el.addEventListener("change", function () {
          state[pair[1]] = el.checked;
          if (simulation) applyFilters();
        });
      });
  }

  bindControls();

  fetch("/api/graph", { credentials: "same-origin" })
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(render)
    .catch(function (err) {
      showMessage("Der Graph konnte nicht geladen werden (" + err.message + "). Bitte Seite neu laden.");
    });
})();
