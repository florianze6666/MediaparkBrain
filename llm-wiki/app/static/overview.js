/* Wissensübersicht (/dashboard): Tabellensortierung und Dialoge.
 *
 * Reines Vanilla-JS, keine Bibliothek. Nichts hier trifft eine
 * Rechteentscheidung - die Tabelle enthaelt bereits nur Zeilen, die der
 * Server freigegeben hat (app/overview.py), und das Teilen wird beim POST
 * noch einmal geprueft (main.share_page: nur der Ersteller).
 */
(function () {
  "use strict";

  // --- Sortierbare Tabellen -------------------------------------------------

  function zellwert(row, index, typ) {
    var cell = row.cells[index];
    if (!cell) return typ === "num" ? 0 : "";
    var raw = cell.hasAttribute("data-value")
      ? cell.getAttribute("data-value")
      : cell.textContent;
    raw = String(raw).trim();
    if (typ === "num") {
      var n = parseFloat(raw.replace(",", "."));
      return isNaN(n) ? -1 : n;
    }
    return raw.toLowerCase();
  }

  function initSortable(table) {
    var thead = table.tHead;
    var tbody = table.tBodies[0];
    if (!thead || !tbody) return;
    var headers = thead.rows[0].cells;

    Array.prototype.forEach.call(headers, function (th, index) {
      var typ = th.getAttribute("data-sort");
      if (!typ) return;
      th.classList.add("sortierbar");
      th.tabIndex = 0;
      th.setAttribute("role", "button");

      function sortiere() {
        var aufsteigend = th.getAttribute("data-richtung") !== "auf";
        // Leere Platzhalterzeile ("Noch kein Wissen") nie mitsortieren.
        var rows = Array.prototype.filter.call(tbody.rows, function (r) {
          return !r.querySelector("td.empty");
        });
        rows.sort(function (a, b) {
          var va = zellwert(a, index, typ);
          var vb = zellwert(b, index, typ);
          if (va < vb) return aufsteigend ? -1 : 1;
          if (va > vb) return aufsteigend ? 1 : -1;
          return 0;
        });
        rows.forEach(function (r) { tbody.appendChild(r); });

        Array.prototype.forEach.call(headers, function (other) {
          other.removeAttribute("data-richtung");
          other.classList.remove("sortiert-auf", "sortiert-ab");
          if (other.getAttribute("data-sort")) other.setAttribute("aria-sort", "none");
        });
        th.setAttribute("data-richtung", aufsteigend ? "auf" : "ab");
        th.classList.add(aufsteigend ? "sortiert-auf" : "sortiert-ab");
        th.setAttribute("aria-sort", aufsteigend ? "ascending" : "descending");
      }

      th.addEventListener("click", sortiere);
      th.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          sortiere();
        }
      });
    });
  }

  Array.prototype.forEach.call(
    document.querySelectorAll("table[data-sortable]"), initSortable
  );

  // --- Dialoge --------------------------------------------------------------

  function oeffne(id) {
    var dlg = document.getElementById(id);
    if (!dlg) return null;
    if (typeof dlg.showModal === "function") dlg.showModal();
    else dlg.setAttribute("open", "open");   // sehr alte Browser
    return dlg;
  }

  function schliesse(dlg) {
    if (!dlg) return;
    if (typeof dlg.close === "function") dlg.close();
    else dlg.removeAttribute("open");
  }

  document.addEventListener("click", function (event) {
    var opener = event.target.closest("[data-open-dialog]");
    if (opener) {
      oeffne(opener.getAttribute("data-open-dialog"));
      return;
    }
    var closer = event.target.closest("[data-close-dialog]");
    if (closer) {
      schliesse(closer.closest("dialog"));
      return;
    }
    var teilen = event.target.closest("[data-teilen-slug]");
    if (teilen) {
      oeffneTeilen(teilen);
    }
  });

  // --- Teilen-Dialog --------------------------------------------------------

  var VERTRAULICH = "vertraulich";

  function oeffneTeilen(button) {
    var dlg = document.getElementById("dialog-teilen");
    if (!dlg) return;
    var slug = button.getAttribute("data-teilen-slug");
    var titel = button.getAttribute("data-teilen-titel") || slug;
    var stufe = button.getAttribute("data-teilen-vertraulichkeit") || "intern";
    var istErsteller = button.getAttribute("data-teilen-ersteller") === "1";

    // Eine offene Auswahl darf nicht ueber dem Teilen-Dialog liegen bleiben.
    var auswahl = document.getElementById("dialog-teilen-auswahl");
    if (auswahl && auswahl.open) schliesse(auswahl);

    var form = document.getElementById("teilen-form");
    form.action = "/wiki/" + encodeURIComponent(slug) + "/share";
    document.getElementById("teilen-titel").textContent = titel;

    var link = document.getElementById("teilen-link");
    link.value = window.location.origin + "/wiki/" + slug;

    var hinweis = document.getElementById("teilen-hinweis");
    var zeile = document.getElementById("teilen-vertraulich-zeile");
    if (stufe !== VERTRAULICH) {
      hinweis.textContent =
        "Diese Seite ist " + stufe + ": alle Leser der Domäne sehen sie bereits. " +
        "Empfänger wirken nur bei vertraulich.";
      hinweis.hidden = false;
      zeile.hidden = false;
    } else {
      hinweis.hidden = true;
      zeile.hidden = true;
      var box = document.getElementById("teilen-vertraulich");
      if (box) box.checked = false;
    }

    var fremd = document.getElementById("teilen-fremd");
    var absenden = document.getElementById("teilen-absenden");
    fremd.hidden = istErsteller;
    absenden.disabled = !istErsteller;

    oeffne("dialog-teilen");
  }

  var kopieren = document.getElementById("teilen-kopieren");
  if (kopieren) {
    kopieren.addEventListener("click", function () {
      var feld = document.getElementById("teilen-link");
      feld.select();
      var ok = false;
      try {
        ok = document.execCommand("copy");
      } catch (e) { /* faellt auf die Auswahl zurueck */ }
      if (!ok && navigator.clipboard) navigator.clipboard.writeText(feld.value);
      kopieren.textContent = "Kopiert";
      window.setTimeout(function () { kopieren.textContent = "Kopieren"; }, 1500);
    });
  }

  // --- Suchfeld im Bearbeiten-Dialog ----------------------------------------

  var suche = document.getElementById("bearbeiten-suche");
  if (suche) {
    suche.addEventListener("input", function () {
      var q = suche.value.trim().toLowerCase();
      var liste = document.getElementById("bearbeiten-liste");
      Array.prototype.forEach.call(liste.children, function (li) {
        var titel = li.getAttribute("data-titel") || "";
        li.hidden = !!q && titel.indexOf(q) === -1;
      });
    });
  }
})();
