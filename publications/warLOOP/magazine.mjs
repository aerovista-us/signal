/**
 * Vespera × AeroVista — PNG magazine (page-flip / StPageFlip).
 * Loads JS via fetch → Blob URL (same-origin execution; avoids Tracking Prevention on CDN <script>).
 *
 * Default source order: CDN first, then ./vendor/page-flip.browser.min.js — avoids a 404 when vendor
 * is not deployed. Set pages-manifest.json `"preferLocalPageFlip": true` to try vendor first
 * (e.g. air-gapped LAN after running scripts/pull-page-flip.ps1).
 */

const PAGE_FLIP_VENDOR = new URL("./vendor/page-flip.browser.min.js", import.meta.url).href;
const PAGE_FLIP_CDN =
  "https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.min.js";

const CONFIG = {
  /** Library uses this vs vertical drift for quick horizontal swipe-to-flip (default in lib is 30). */
  swipeDistance: 26,
  flippingTime: 1100,
  flippingTimeReducedMotion: 240,
  maxShadowOpacity: 0.58,
  manifest: "pages-manifest.json",
};

function injectScriptSrc(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.async = false;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error(`Failed to load script: ${src}`));
    document.head.appendChild(s);
  });
}

/** Fetch JS text and run it from a blob: URL (same document origin → no third-party script semantics). */
async function injectScriptFromUrl(sourceUrl) {
  const res = await fetch(sourceUrl, { cache: "force-cache", credentials: "omit" });
  if (!res.ok) throw new Error(`${sourceUrl} → HTTP ${res.status}`);
  const text = await res.text();
  const blob = new Blob([text], { type: "application/javascript" });
  const blobUrl = URL.createObjectURL(blob);
  try {
    await injectScriptSrc(blobUrl);
  } finally {
    URL.revokeObjectURL(blobUrl);
  }
}

async function ensurePageFlip(preferLocalVendor) {
  if (globalThis.St?.PageFlip) return;
  const sources = preferLocalVendor ? [PAGE_FLIP_VENDOR, PAGE_FLIP_CDN] : [PAGE_FLIP_CDN, PAGE_FLIP_VENDOR];
  let lastErr = null;
  for (const url of sources) {
    try {
      await injectScriptFromUrl(url);
      if (globalThis.St?.PageFlip) return;
    } catch (e) {
      lastErr = e;
    }
  }
  throw lastErr || new Error("page-flip library did not register global St.PageFlip");
}

function measureBook(bookEl) {
  const r = bookEl.getBoundingClientRect();
  const vv = window.visualViewport;
  const w = Math.round(r.width > 2 ? r.width : vv?.width ?? window.innerWidth);
  const h = Math.round(r.height > 2 ? r.height : vv?.height ?? window.innerHeight);
  return {
    w: Math.max(280, w),
    h: Math.max(400, h),
  };
}

function resolvePageUrl(relative) {
  return new URL(relative, window.location.href).href;
}

function safeHref(href) {
  if (typeof href !== "string") return null;
  const t = href.trim();
  if (!t || /^\s*javascript:/i.test(t) || /^\s*data:/i.test(t)) return null;
  try {
    const u = new URL(t, window.location.href);
    if (u.protocol === "javascript:" || u.protocol === "data:") return null;
    return u.href;
  } catch {
    return null;
  }
}

function parseLinks(links) {
  if (!Array.isArray(links)) return [];
  const out = [];
  for (const l of links) {
    if (!l || typeof l !== "object") continue;
    const label = typeof l.label === "string" ? l.label.trim() : "";
    const href = safeHref(typeof l.href === "string" ? l.href : "");
    if (!label || !href) continue;
    out.push({ label, href });
  }
  return out;
}

function titleFromSrc(src) {
  const file = src.split("/").pop() || src;
  const base = file.replace(/\.[^.]+$/, "");
  return base
    .replace(/^[0-9]+\./, "")
    .replace(/_/g, " ")
    .replace(/-/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function linkOpensSameTab(href) {
  try {
    return new URL(href, window.location.href).origin === window.location.origin;
  } catch {
    return true;
  }
}

function collectChromeRefs() {
  return {
    kicker: document.getElementById("mag-header-kicker"),
    title: document.getElementById("mag-header-title"),
    meta: document.getElementById("mag-header-meta"),
    spread: document.getElementById("mag-header-spread"),
    footer: document.getElementById("mag-footer"),
    chinToggle: document.getElementById("mag-chin-toggle"),
    chinPanel: document.getElementById("mag-chin-panel"),
    chinSummary: document.getElementById("mag-chin-summary"),
    chinHint: document.getElementById("mag-chin-hint"),
    chinNote: document.getElementById("mag-chin-note"),
    chinLinks: document.getElementById("mag-chin-links"),
    flipHint: document.getElementById("flip-hint"),
    issue: "VXP-MR-01",
  };
}

function applyShellLabels(manifest, chrome) {
  if (!chrome) return;
  if (typeof manifest.issue === "string" && manifest.issue.trim()) {
    chrome.issue = manifest.issue.trim();
  }
  if (chrome.kicker && typeof manifest.partner === "string" && manifest.partner.trim()) {
    chrome.kicker.textContent = manifest.partner.trim();
  }
  if (chrome.title) {
    const t = typeof manifest.title === "string" ? manifest.title.trim() : "";
    if (t) chrome.title.textContent = t;
    else if (chrome.issue) chrome.title.textContent = chrome.issue;
  }
}

function setChinOpen(chrome, open) {
  if (!chrome?.footer || !chrome?.chinToggle) return;
  chrome.footer.classList.toggle("chin-open", open);
  chrome.chinToggle.setAttribute("aria-expanded", open ? "true" : "false");
}

function makeSyncChrome(pageSpecs, chrome) {
  let lastIdx = -1;
  return (idx, opts = {}) => {
    const collapseOnPageChange = opts.collapseOnPageChange !== false;
    if (collapseOnPageChange && lastIdx >= 0 && idx !== lastIdx) {
      setChinOpen(chrome, false);
    }
    lastIdx = idx;

    const spec = pageSpecs[idx];
    const n = pageSpecs.length;
    const issue = chrome.issue || "VXP-MR-01";

    const spreadTitle =
      spec.kind === "placeholder" ? spec.title || spec.label : spec.title || `Spread ${idx + 1}`;

    if (chrome.meta) chrome.meta.textContent = `${issue} · ${idx + 1} / ${n}`;
    if (chrome.spread) chrome.spread.textContent = spreadTitle;
    if (chrome.chinSummary) chrome.chinSummary.textContent = spreadTitle;

    const open = chrome.footer?.classList.contains("chin-open");
    if (chrome.chinHint) {
      chrome.chinHint.textContent = open ? "Tap to collapse notes" : `Notes & links · ${idx + 1} of ${n}`;
    }

    const note =
      spec.kind === "placeholder"
        ? spec.note || "This spread is not published yet."
        : spec.note || "";

    if (chrome.flipHint) chrome.flipHint.hidden = n > 1;

    if (chrome.chinNote) {
      const showNote = Boolean(note) && (n > 1 || spec.kind === "placeholder");
      chrome.chinNote.textContent = showNote ? note : "";
      chrome.chinNote.hidden = !showNote;
    }

    if (chrome.chinLinks) {
      chrome.chinLinks.replaceChildren();
      const links = Array.isArray(spec.links) ? spec.links : [];
      for (const l of links) {
        const a = document.createElement("a");
        a.href = l.href;
        a.textContent = l.label;
        a.rel = "noopener noreferrer";
        a.target = linkOpensSameTab(l.href) ? "_self" : "_blank";
        chrome.chinLinks.appendChild(a);
      }
    }
  };
}

/**
 * Each manifest entry is either a string (image path), `{ "src": "…", "title", "note", "links" }`,
 * or `{ "placeholder": true, "label": "…" }`.
 */
function normalizePageSpecs(manifest) {
  const raw = Array.isArray(manifest.pages) ? manifest.pages : [];
  return raw.map((entry, i) => {
    if (typeof entry === "string") {
      return {
        kind: "image",
        src: entry,
        resolved: resolvePageUrl(entry),
        title: titleFromSrc(entry),
        note: "",
        links: [],
      };
    }
    if (entry && typeof entry === "object") {
      if (entry.placeholder === true) {
        const label =
          typeof entry.label === "string" && entry.label.trim()
            ? entry.label.trim()
            : `Page ${i + 1}`;
        return {
          kind: "placeholder",
          label,
          title: typeof entry.title === "string" && entry.title.trim() ? entry.title.trim() : label,
          note: typeof entry.note === "string" ? entry.note.trim() : "",
          links: parseLinks(entry.links),
        };
      }
      if (typeof entry.src === "string") {
        const src = entry.src;
        return {
          kind: "image",
          src,
          resolved: resolvePageUrl(src),
          title:
            typeof entry.title === "string" && entry.title.trim()
              ? entry.title.trim()
              : titleFromSrc(src),
          note: typeof entry.note === "string" ? entry.note.trim() : "",
          links: parseLinks(entry.links),
        };
      }
    }
    throw new Error(`pages-manifest.json: invalid page entry at index ${i}`);
  });
}

function preloadAround(pageSpecs, index) {
  const neighbors = [pageSpecs[index - 1], pageSpecs[index + 1]].filter(Boolean);
  const seen = new Set();
  for (const spec of neighbors) {
    if (spec.kind !== "image") continue;
    if (seen.has(spec.resolved)) continue;
    seen.add(spec.resolved);
    const img = new Image();
    img.decoding = "async";
    img.src = spec.resolved;
  }
}

function showEmpty(bookEl, message) {
  bookEl.innerHTML = "";
  const wrap = document.createElement("div");
  wrap.className = "empty-state";
  wrap.innerHTML = message;
  bookEl.appendChild(wrap);
}

function buildPageElements(pageSpecs) {
  const frag = document.createDocumentFragment();
  const pages = [];
  let firstImagePlaced = false;
  for (let i = 0; i < pageSpecs.length; i++) {
    const spec = pageSpecs[i];
    const page = document.createElement("div");
    page.className = "page";
    page.dataset.density = "soft";

    if (spec.kind === "placeholder") {
      page.classList.add("page--placeholder");
      const inner = document.createElement("div");
      inner.className = "page__placeholder-inner";
      const kicker = document.createElement("p");
      kicker.className = "page__placeholder-kicker";
      kicker.textContent = "Coming soon";
      const labelEl = document.createElement("p");
      labelEl.className = "page__placeholder-label";
      labelEl.textContent = spec.title || spec.label;
      inner.appendChild(kicker);
      inner.appendChild(labelEl);
      page.appendChild(inner);
    } else {
      const img = document.createElement("img");
      img.className = "page__img";
      img.alt = spec.title || "";
      img.decoding = "async";
      /* Eager: avoids Edge “lazy placeholder” intervention on flip pages; list is small. */
      img.loading = "eager";
      if (!firstImagePlaced) {
        img.fetchPriority = "high";
        firstImagePlaced = true;
      }
      img.src = spec.resolved;
      page.appendChild(img);
    }

    frag.appendChild(page);
    pages.push(page);
  }
  return { frag, pages };
}

function syncNav(pf, prevBtn, nextBtn) {
  if (!pf) return;
  const i = pf.getCurrentPageIndex();
  const n = pf.getPageCount();
  prevBtn.hidden = i <= 0;
  nextBtn.hidden = i >= n - 1;
}

function waitLayout(bookEl, cb) {
  requestAnimationFrame(() => {
    requestAnimationFrame(cb);
  });
}

function initMagazine(PageFlip, bookEl, prevBtn, nextBtn, pageSpecs, chrome) {
  const syncChrome = chrome ? makeSyncChrome(pageSpecs, chrome) : null;

  waitLayout(bookEl, () => {
    const { w, h } = measureBook(bookEl);
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const flippingTime = reduceMotion ? CONFIG.flippingTimeReducedMotion : CONFIG.flippingTime;

    const { frag, pages } = buildPageElements(pageSpecs);
    bookEl.appendChild(frag);

    const pf = new PageFlip(bookEl, {
      width: w,
      height: h,
      size: "fixed",
      minWidth: w,
      maxWidth: w,
      minHeight: h,
      maxHeight: h,
      drawShadow: true,
      flippingTime,
      maxShadowOpacity: CONFIG.maxShadowOpacity,
      usePortrait: true,
      autoSize: false,
      /* true: touch listeners use passive mode where possible — helps iOS/WebKit deliver gestures over overflow:hidden shells */
      mobileScrollSupport: true,
      swipeDistance: CONFIG.swipeDistance,
      showCover: false,
      showPageCorners: true,
      clickEventForward: false,
      useMouseEvents: true,
      startPage: 0,
      startZIndex: 0,
    });

    pf.loadFromHTML(pages);

    preloadAround(pageSpecs, 0);
    syncNav(pf, prevBtn, nextBtn);
    if (syncChrome) syncChrome(0, { collapseOnPageChange: false });

    pf.on("flip", () => {
      const idx = pf.getCurrentPageIndex();
      preloadAround(pageSpecs, idx);
      syncNav(pf, prevBtn, nextBtn);
      if (syncChrome) syncChrome(idx);
    });

    if (chrome?.chinToggle) {
      chrome.chinToggle.addEventListener("click", () => {
        const open = !chrome.footer.classList.contains("chin-open");
        setChinOpen(chrome, open);
        if (syncChrome) syncChrome(pf.getCurrentPageIndex(), { collapseOnPageChange: false });
      });
    }

    const scheduleReflow = () => {
      const ui = pf.getUI?.();
      if (ui && typeof ui.update === "function") ui.update();
    };

    bookEl.querySelectorAll(".page__img").forEach((img) => {
      img.addEventListener("load", () => scheduleReflow(), { passive: true });
    });

    let resizeT = 0;
    const onResize = () => {
      window.clearTimeout(resizeT);
      resizeT = window.setTimeout(scheduleReflow, 80);
    };

    window.addEventListener("resize", onResize, { passive: true });
    window.addEventListener("orientationchange", onResize, { passive: true });
    const vv = window.visualViewport;
    if (vv) {
      vv.addEventListener("resize", onResize, { passive: true });
      vv.addEventListener("scroll", onResize, { passive: true });
    }

    let ro;
    if (typeof ResizeObserver !== "undefined") {
      ro = new ResizeObserver(() => scheduleReflow());
      ro.observe(bookEl);
    }

    prevBtn.addEventListener("click", () => pf.flipPrev("top"));
    nextBtn.addEventListener("click", () => pf.flipNext("top"));

    scheduleReflow();
  });
}

async function main() {
  const bookEl = document.getElementById("book");
  const prevBtn = document.getElementById("nav-prev");
  const nextBtn = document.getElementById("nav-next");

  let manifest;
  try {
    const r = await fetch(new URL(CONFIG.manifest, window.location.href), { cache: "no-store" });
    if (!r.ok) throw new Error(`Manifest HTTP ${r.status}`);
    manifest = await r.json();
  } catch (err) {
    showEmpty(bookEl, `<strong>Could not load manifest.</strong><br />${String(err.message || err)}`);
    return;
  }

  const preferLocalVendor = manifest.preferLocalPageFlip === true;

  try {
    await ensurePageFlip(preferLocalVendor);
  } catch (err) {
    showEmpty(
      bookEl,
      `<strong>Page flip library failed to load.</strong><br />${String(err.message || err)}`,
    );
    return;
  }

  const PageFlip = globalThis.St.PageFlip;

  let pageSpecs;
  try {
    pageSpecs = normalizePageSpecs(manifest);
  } catch (err) {
    showEmpty(bookEl, `<strong>Invalid manifest.</strong><br />${String(err.message || err)}`);
    return;
  }

  if (pageSpecs.length === 0) {
    showEmpty(
      bookEl,
      "<strong>No pages in manifest.</strong><br />Add PNG paths to <code>pages-manifest.json</code> (see <code>pages/README.txt</code>).",
    );
    return;
  }

  const chrome = collectChromeRefs();
  applyShellLabels(manifest, chrome);
  initMagazine(PageFlip, bookEl, prevBtn, nextBtn, pageSpecs, chrome);
}

main();
