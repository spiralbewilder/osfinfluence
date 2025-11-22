# Agents Guide – OSF Grants Globe

## Objective
- Build and maintain a professional, easy-to-use visualization of OSF/Soros-funded grantees worldwide on an interactive 3D globe (`osf_globe.html`).
- Show locations at exact locations where possible, and roll-up to city/region/country level, whatever is most specific—never display specific street addresses.
- Prioritize clarity: simple controls, quick load times, and intuitive filtering.

## Tech & Data Pipeline (preserve this architecture)
- Data prep happens **offline**, in Python:
  - `process_grantees.py`:
    - Reads yearly CSVs (e.g. `2020.csv`–`2023.csv`).
    - Geocodes unique location queries via Photon, using a persistent `geocode_cache.json`.
    - Emits `geocodes.json` (unique locations with lat/lng).
  - `extract_grantees.py`:
    - Groups CSV rows by recipient and emits `grantees.json` (recipient info, location strings, purposes, etc.).
- Browser/runtime:
  - Does **not** read CSVs directly in the normal path; it consumes `geocodes.json` and `grantees.json`.
  - May use PapaParse as a **fallback** if `grantees.json` is missing.
  - Must **not** call external geocoding APIs at runtime; geocodes come from `geocodes.json` and local cache.

## Privacy & Redaction Rules (non-negotiable)
- Never display street-level addresses or building-level specificity.
- City/region + country granularity is acceptable.
- If raw data includes street-level detail, aggregate or strip it before writing to `geocodes.json` / `grantees.json`.
- Do not introduce new external data sources or tracking without explicit approval.

## Visualization Requirements
- Use a 3D globe built with Globe.gl + Three.js:
  - Local JS bundles: `globe.gl.min.js`, `three.min.js` (no runtime CDN dependency).
- Points/bubbles represent grants or aggregated grant locations:
  - Color by primary sector; use a small, distinct palette.
  - Bubble size must be switchable between:
    - total grant amount, and
    - count of grants at that location (when amount data is available).
  - Tooltip or side panel should show:
    - recipient or aggregated location info,
    - year (or year range),
    - sector,
    - amount (or clearly marked as “not available” if amounts are not wired through),
    - location (city/region + country only),
    - purpose/notes (if available and non-identifying).
- Performance:
  - No runtime geocoding in the browser.
  - Page should load and render the globe within a few seconds on typical hardware.

## Interaction & UX
- Controls live in a sidebar (toggled from the viewport):
  - Year slider: filters grants to **up to** the selected year.
  - Size radio: bubble size mode (amount vs. count) – degrade gracefully if amounts are not yet present.
  - Sector filters: checkboxes with color swatches; allow multi-select.
- The globe must remain visible; controls should not permanently cover it.
- Responsive behavior:
  - Desktop: sidebar on the side.
  - Mobile: sidebar can slide in or become a bottom sheet.
- Accessibility:
  - Keyboard-focusable controls in a sensible order.
  - High-contrast text and controls.
  - Legible typography (no tiny fonts).

## Existing Implementation Expectations
- `osf_globe.html`:
  - Owns the globe instantiation (Globe.gl + Three.js).
  - Loads `geocodes.json` and `grantees.json` and uses them to build in-memory grant/location structures.
  - Contains:
    - a manual-rotation globe,
    - a slide-out controls panel (year slider, size mode, sector filters),
    - a detail panel for clicked points.
- Current data flow (to be refined, not replaced):
  - CSVs → `process_grantees.py` / `extract_grantees.py` → `geocodes.json` + `grantees.json` → `osf_globe.html` → Globe.gl.
- Photon + `geocode_cache.json` are acceptable in the **offline** Python step; do not move these calls into the browser.

## Known Pitfalls & Invariants (do not regress)
- Shared state:
  - Variables like `allPoints`, `sizeMode`, and `activeSectors` are shared state for aggregation and filtering.
  - They must be declared in a scope accessible to both the initial data load and the aggregation/filtering functions (no undefined-reference errors).
- Globe click handling:
  - Use Globe.gl’s recommended click signature (`onPointClick(point, event)`).
  - Do not rely on undefined `event.points[0].customdata`; instead, use the bound point object to populate the detail panel.
- Sizing:
  - Amount-based sizing is meaningless if amounts are all zero.
  - Do **not** invent numeric amounts. If you need amount-based sizing, wire real amounts from the data pipeline; otherwise, make count-based sizing the default and handle the “amount” mode gracefully.
- Geocoding in the browser:
  - Do not introduce per-grant async geocoding loops at runtime.
  - Resolve locations using `geocodes.json` synchronously at load and jitter once if needed.

## Improvement Priorities
When modifying this repo, follow this order of operations:

1. **Fix correctness issues first**:
   - Eliminate runtime errors (undefined variables like `allPoints`, `sizeMode`, `activeSectors`).
   - Fix click handlers and detail panel wiring so that clicking points reliably shows the right information.
2. **Improve manual rotation and camera behavior**:
   - Make drag rotation smooth and predictable.
   - Apply sensible zoom limits and damping.
   - Any auto-rotate should be gentle and never fight user input; it can be off by default.
3. **Improve labelling**:
   - Reduce label clutter.
   - Prefer “City, Country” labels and/or aggregated labels (location · grant count / amount band).
   - Only surface more detail in tooltips or the side panel.
4. **Optimize performance**:
   - Avoid redundant work on initial load.
   - Make filter changes (year, sector, size mode) update the globe efficiently.

## Setup & Run
- Serve files locally over HTTP from the project root (avoid `file://`):
  - Example: `python -m http.server 8000`
- Required files in the same directory for a working demo:
  - `osf_globe.html`
  - `three.min.js`
  - `globe.gl.min.js`
  - `papaparse.min.js`
  - `geocodes.json`
  - `grantees.json` (or CSVs if using the fallback path).
- Open: `http://localhost:8000/osf_globe.html` to validate changes.

## Working with Existing Code (important)
- Prefer **incremental changes** over rewrites. Preserve the current architecture unless there is a clear, documented reason to change it.
- Do **not** delete or replace major files (for example: `osf_globe.html`, `process_grantees.py`, `extract_grantees.py`, or core JS modules) unless explicitly requested.
- When improving code, aim to:
  - keep existing data formats and public interfaces stable, and
  - focus on clarity, performance, and UX polish.
- Reuse existing data structures and helper functions when possible instead of inventing new ones.
- If a larger redesign is truly necessary, propose it separately and keep the implementation patch small and localized.

## Change Notes
- Keep visuals simple and purposeful; avoid visual clutter.
- Document any new controls, data assumptions, or non-obvious logic in comments inside `osf_globe.html`.
- Do not add new external dependencies (CDNs, APIs, analytics) without explicit approval.

