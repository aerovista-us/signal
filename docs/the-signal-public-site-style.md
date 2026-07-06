# The SIGNAL public site — visual system

## Source of truth

The public hub and dispatch pages use the **shareholder newsletter** palette and atmosphere defined in:

- [`the_signal_aerovista_shareholder_newsletter.html`](../the_signal_aerovista_shareholder_newsletter.html)

Key traits: cool ink (`#f5fbff`), cyan/blue accents, dark blue gradient background, 44px grid overlay, Inter sans-serif, gradient brand mark.

## Shared stylesheet

| File | Role |
|------|------|
| [`signal-public-theme.css`](../signal-public-theme.css) | Canonical file for GitHub Pages (repo root) |
| [`css/signal-public-theme.css`](../css/signal-public-theme.css) | Mirror copy; keep in sync with root file |

### Pages that load it

| Page | How theme is applied |
|------|----------------------|
| [`index.html`](../index.html) | Shared rules **inlined** in `<style>` (no external CSS required on Pages) |
| [`dispatches/*.html`](../dispatches/) | `<link href="../signal-public-theme.css" />` |

`index.html` also keeps page-specific inline styles (hero grid, dispatch cards, audio player).

See [github-pages-deploy.md](./github-pages-deploy.md) for pushing to [aerovista-us/signal](https://github.com/aerovista-us/signal).

### Hub links to macro publications

[`index.html`](../index.html) lists these in the **Macro Publications** section (`#publications`) and footer:

| Label | Path |
|-------|------|
| Macro Signals Briefing (standalone) | [`signal.html`](../signal.html) |
| Signals Briefing · issue wrap | [`publications/VXP-MR-01-macro-rails-intelligence/signals_briefing.html`](../publications/VXP-MR-01-macro-rails-intelligence/signals_briefing.html) |
| Macro Rails Intelligence Magazine | [`publications/VXP-MR-01-macro-rails-intelligence/magazine.html`](../publications/VXP-MR-01-macro-rails-intelligence/magazine.html) |

Those pages keep their own Vespera styling; only the hub cards use the newsletter public theme. The magazine card on [`index.html`](../index.html) previews [`cover.png`](../publications/VXP-MR-01-macro-rails-intelligence/cover.png). [`signal.html`](../signal.html) links to the issue briefing and magazine in an **Also in this issue** block. Each publication page includes a **← The SIGNAL** link back to [`index.html`](../index.html) (dispatch-style hub navigation).

## Exclusions (not part of this theme)

These files keep their own styling and were **not** updated in the newsletter alignment pass:

| File | Notes |
|------|-------|
| [`signal.html`](../signal.html) | Standalone Vespera macro briefing (purple palette) |
| [`publications/VXP-MR-01-macro-rails-intelligence/signals_briefing.html`](../publications/VXP-MR-01-macro-rails-intelligence/signals_briefing.html) | Issue-wrapped briefing; tied to `signal.html` |
| [`publications/VXP-MR-01-macro-rails-intelligence/magazine.html`](../publications/VXP-MR-01-macro-rails-intelligence/magazine.html) | PNG magazine shell |
| [`player                 .html`](../player%20%20%20%20%20%20%20%20%20%20%20%20%20%20.html) | SwampHop audio player (separate green/gold aesthetic) |

## Browser chrome

- `theme-color` on hub and dispatches: `#04070d`
- Root [`favicon.svg`](../favicon.svg) accent: `#67e8f9` (newsletter cyan)

Publication routes may reference their own favicon under `publications/`.

## Internal Signals (EOD / EOW)

Shareholder, employee, and operator editions live under [**Internal Signals**](../dispatches/internal-signals.html) (formerly internal news). All daily and weekly internal reports route through this hub.

| Route | Role |
|-------|------|
| [`dispatches/internal-signals.html`](../dispatches/internal-signals.html) | Canonical hub — sections: Right Now, Daily EOD, Weekly EOW, ByteCast, Milestones, Archive |
| [`dispatches/current-updates.html`](../dispatches/current-updates.html) | Redirect to Internal Signals (legacy EOD/EOW hub URL) |
| [`newsletter-current.html`](../newsletter-current.html) | Redirect to Internal Signals (legacy newsletter URL) |
| [`dispatches/eod-current-operating-note.html`](../dispatches/eod-current-operating-note.html) | Current daily operating note |
| [`dispatches/eow-current-stakeholder-update.html`](../dispatches/eow-current-stakeholder-update.html) | Current weekly stakeholder summary |
| [`dispatches/eow-2026-06-28-weekend-report.html`](../dispatches/eow-2026-06-28-weekend-report.html) | Dated EOW weekend report (June 28, 2026) |
| [`newsletters/aerovista_bytecast_status_player.html`](../newsletters/aerovista_bytecast_status_player.html) | Current overall company status ByteCast (July 5 — audio, AVCC roadmap, transcript) |
| [`newsletters/aerovista_weekend_report_6.28.26.html`](../newsletters/aerovista_weekend_report_6.28.26.html) | Weekend ByteCast edition (June 28 — audio + transcript) |
| [`newsletters/aerovista_signal_weekly_2026-06-21.html`](../newsletters/aerovista_signal_weekly_2026-06-21.html) | Weekly ByteCast archive (June 21) |
| [`newsletters/aerovista_signal_echoverse_bytecast_2026-06-16.html`](../newsletters/aerovista_signal_echoverse_bytecast_2026-06-16.html) | Platform ByteCast example (EchoVerse) |

The homepage features one **Internal Signals** card; separate newsletter and EOD/EOW cards were removed.

## Adding a new dispatch

1. Copy an existing dispatch HTML shell.
2. Include `<link rel="stylesheet" href="../css/signal-public-theme.css" />`.
3. Set `<meta name="theme-color" content="#04070d" />`.
4. Do **not** duplicate the old inline gold-theme `<style>` block.
