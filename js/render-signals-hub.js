/**
 * Internal Signals hub — render catalog from signals-catalog.json + search/filter.
 */
(function () {
  var CATALOG_URL = "/js/signals-catalog.json";

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/"/g, "&quot;");
  }

  function badgesHtml(badges) {
    return (badges || [])
      .map(function (b) {
        return '<span class="type-badge ' + esc(b.type) + '">' + esc(b.label) + "</span>";
      })
      .join("");
  }

  function catalogRow(item) {
    return (
      '<a class="catalog-row" href="' +
      esc(item.href) +
      '" data-types="' +
      esc((item.types || []).join(" ")) +
      '" data-tags="' +
      esc(item.tags || "") +
      '">' +
      '<div class="row-date"><em>' +
      esc(item.dateEm) +
      "</em>" +
      esc(item.dateYear) +
      "</div>" +
      '<div class="row-body"><strong>' +
      badgesHtml(item.badges) +
      esc(item.title) +
      "</strong><span>" +
      esc(item.summary) +
      "</span></div>" +
      '<span class="row-action">Open →</span></a>'
    );
  }

  function nowCard(item) {
    return (
      '<a class="now-card" href="' +
      esc(item.href) +
      '" data-types="' +
      esc((item.types || []).join(" ")) +
      '" data-tags="' +
      esc(item.tags || "") +
      '">' +
      '<span class="type">' +
      esc(item.typeLabel) +
      "</span><strong>" +
      esc(item.title) +
      "</strong><span>" +
      esc(item.summary) +
      '</span><span class="arrow">Open edition →</span></a>'
    );
  }

  function countByType(editions, type) {
    if (type === "all") return editions.length;
    return editions.filter(function (e) {
      return (e.types || []).indexOf(type) >= 0;
    }).length;
  }

  function initFilters(rows, nowCards, sections, empty, chips, input) {
    var activeFilter = "all";

    function matchesFilter(el) {
      var types = (el.dataset.types || "").split(/\s+/);
      return activeFilter === "all" || types.indexOf(activeFilter) >= 0;
    }

    function matchesSearch(el, q) {
      if (!q) return true;
      var text = (el.textContent + " " + (el.dataset.tags || "")).toLowerCase();
      return text.indexOf(q) >= 0;
    }

    function applyFilters() {
      var q = (input && input.value ? input.value : "").trim().toLowerCase();
      var visibleRows = 0;

      rows.forEach(function (row) {
        var ok = matchesFilter(row) && matchesSearch(row, q);
        row.classList.toggle("hidden", !ok);
        if (ok) visibleRows++;
      });

      nowCards.forEach(function (card) {
        var ok = matchesFilter(card) && matchesSearch(card, q);
        card.style.display = ok ? "" : "none";
      });

      sections.forEach(function (section) {
        var sectionRows = section.querySelectorAll(".catalog-row:not(.hidden)");
        var hasNow =
          section.id === "now" &&
          [].some.call(section.querySelectorAll(".now-card"), function (c) {
            return c.style.display !== "none";
          });
        var hasContent = section.id === "about" || sectionRows.length > 0 || hasNow;
        section.style.display = (q || activeFilter !== "all") && !hasContent && section.id !== "about" ? "none" : "";
      });

      if (empty) {
        var anyNow = nowCards.some(function (c) {
          return c.style.display !== "none";
        });
        empty.classList.toggle("visible", (q || activeFilter !== "all") && visibleRows === 0 && !anyNow);
      }
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        chips.forEach(function (c) {
          c.classList.remove("active");
        });
        chip.classList.add("active");
        activeFilter = chip.dataset.filter || "all";
        applyFilters();
      });
    });

    if (input) input.addEventListener("input", applyFilters);
    applyFilters();
  }

  function bindCopyButtons() {
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", async function () {
        var text = btn.getAttribute("data-copy");
        try {
          await navigator.clipboard.writeText(text);
          var old = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(function () {
            btn.textContent = old;
          }, 1400);
        } catch (e) {
          /* ignore */
        }
      });
    });
  }

  function renderFeatured(featured) {
    if (!featured) return;
    var article = document.querySelector(".featured");
    if (!article) return;
    var label = article.querySelector(".featured-label");
    if (label && featured.label) {
      label.innerHTML =
        '<span class="dot"></span> ' + esc(featured.label);
    }
    var h2 = article.querySelector("h2");
    if (h2 && featured.title) h2.textContent = featured.title;
    var p = article.querySelector(".featured-copy p, .featured > div > p");
    if (!p) p = article.querySelector(".featured p");
    if (p && featured.summary) p.textContent = featured.summary;
    var openBtn = article.querySelector('.featured-actions a.btn[href]');
    if (openBtn && featured.href) openBtn.href = featured.href;
    var copyBtn = article.querySelector(".featured-actions [data-copy]");
    if (copyBtn && featured.href) {
      copyBtn.setAttribute(
        "data-copy",
        featured.href.indexOf("http") === 0
          ? featured.href
          : "https://thesignal.aerovista.us" + featured.href
      );
    }
    var stats = article.querySelectorAll(".featured-side .pulse-stat");
    (featured.stats || []).forEach(function (stat, i) {
      if (!stats[i]) return;
      var strong = stats[i].querySelector("strong");
      var span = stats[i].querySelector("span");
      if (strong) strong.textContent = stat.value;
      if (span) span.textContent = stat.label;
    });
  }

  function render(data) {
    renderFeatured(data.featured);

    var editions = data.editions || [];
    var sections = {
      eod: document.getElementById("catalog-eod"),
      weekly: document.getElementById("catalog-weekly"),
      bytecast: document.getElementById("catalog-bytecast"),
      milestones: document.getElementById("catalog-milestones"),
      eom: document.getElementById("catalog-eom"),
      archive: document.getElementById("catalog-archive"),
    };

    Object.keys(sections).forEach(function (key) {
      var el = sections[key];
      if (!el) return;
      var html = editions
        .filter(function (e) {
          return e.section === key;
        })
        .map(catalogRow)
        .join("");
      el.innerHTML = html;
    });

    var nowGrid = document.querySelector("#now .now-grid");
    if (nowGrid && data.now) {
      nowGrid.innerHTML = data.now.map(nowCard).join("");
    }

    var meta = document.querySelector(".hub-meta strong");
    if (meta && data.updated) {
      var d = new Date(data.updated + "T12:00:00");
      meta.textContent =
        "Updated " +
        d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
    }
    var metaCount = document.querySelector(".hub-meta");
    if (metaCount) {
      var countNode = metaCount.childNodes[metaCount.childNodes.length - 1];
      if (countNode && countNode.nodeType === 3) {
        countNode.textContent = "\n          " + editions.length + " editions indexed\n        ";
      }
    }

    var chips = [].slice.call(document.querySelectorAll(".filter-chip"));
    chips.forEach(function (chip) {
      var type = chip.dataset.filter || "all";
      var countEl = chip.querySelector(".count");
      if (countEl) countEl.textContent = String(countByType(editions, type));
    });

    var rows = [].slice.call(document.querySelectorAll(".catalog-row"));
    var nowCards = [].slice.call(document.querySelectorAll(".now-card"));
    var hubSections = [].slice.call(document.querySelectorAll(".hub-section"));
    var empty = document.getElementById("emptyState");
    var input = document.getElementById("signalSearch");

    initFilters(rows, nowCards, hubSections, empty, chips, input);
    bindCopyButtons();

    var subnavLinks = [].slice.call(document.querySelectorAll(".subnav-link"));
    if (subnavLinks.length && hubSections.length && "IntersectionObserver" in window) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              var id = entry.target.id;
              subnavLinks.forEach(function (link) {
                link.classList.toggle("active", link.getAttribute("href") === "#" + id);
              });
            }
          });
        },
        { rootMargin: "-40% 0px -50% 0px", threshold: 0 }
      );
      hubSections.forEach(function (s) {
        observer.observe(s);
      });
    }
  }

  fetch(CATALOG_URL)
    .then(function (r) {
      return r.json();
    })
    .then(render)
    .catch(function (err) {
      console.warn("signals-catalog load failed", err);
      bindCopyButtons();
    });
})();
