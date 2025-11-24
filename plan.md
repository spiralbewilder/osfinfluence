Overall End Goal State
Based on the project history and the current implementation in osf_globe.html, the end goal is a fully functional, interactive 3D globe visualization of OSF (Open Society Foundations) grants that provides an intuitive, data-driven exploration of philanthropic funding worldwide. Here's the comprehensive vision:

Core Functionality
Globe Display: A rotating 3D globe (using Globe.gl) with a dark background, displaying bubbles (points) representing individual grants or aggregated grant clusters at their geographic locations.
Data Representation:
Bubbles are colored by primary sector (e.g., Education in blue, Media in magenta).
Bubble size reflects either total grant amount or number of grants (user-selectable).
Locations are pre-geocoded from CSV data (2020-2023) for instant loading, with fallbacks for unmapped areas.
Interactivity:
Clickable bubbles to show grant details (name, amount, year, sector, location, purpose) in a side panel.
Year slider to filter grants up to a selected year (e.g., 2020-2023).
Sector filters (grouped into "Primary Sectors" and "Other Sectors") to show/hide bubbles by category.
Size mode toggle (amount vs. count).
Performance: Loads in seconds with no runtime geocoding delays or API calls; handles thousands of grants efficiently.
User Interface & Experience
Layout: Full-screen globe with a toggleable sliding sidebar (320px wide) on the right for controls, ensuring the globe is never permanently obscured.
Controls:
Top-left button to show/hide the sidebar.
Sidebar includes: Year label/slider, size mode radios, collapsible sector filters with color swatches and checkboxes.
Filters are scrollable and grouped for usability.
Responsiveness: Works on desktop and mobile; sidebar adapts or becomes a bottom sheet if needed.
Accessibility: Keyboard navigation, high-contrast colors, tooltips for clarity.
Technical Implementation
Data Sources: CSVs (2020-2023) parsed via PapaParse; pre-geocoded geocodes.json for locations; optional grantees.json for aggregated data.
Libraries: Local copies of Three.js, Globe.gl, and PapaParse to avoid CDN issues.
Hosting: Runs behind a simple web server (e.g., python -m http.server 8000) to prevent CORS and file protocol blocks.
Error Handling: Graceful fallbacks for missing data, with user guidance for setup issues.
Security & Privacy: No external API calls; all data processed locally.
User Workflow
Serve the files over HTTP.
Open osf_globe.html in a browser.
Explore the globe: Rotate, zoom, filter by year/sector, click bubbles for details.
Use the sidebar toggle for advanced controls without cluttering the view.
Success Criteria
Usability: Legend and controls don't overlay the globe; everything is accessible via the sidebar.
Performance: Loads quickly, handles data volume without lag.
Accuracy: Locations are correctly mapped; sectors are categorized based on grant purposes.
Completeness: Covers all provided grant data with proper aggregation and visualization.
This creates an engaging, educational tool for understanding global grant distributions, highlighting OSF's impact across sectors and regions. If any aspect isn't aligned, provide feedback for refinement!

Ease-of-use ideas to consider next
- Add a short hint near the year slider explaining it shows grants up to the selected year.
- Provide a one-click “reset filters” control to restore year, size mode, and sector defaults.
- On mobile, offer a bottom-sheet version of the detail panel to keep the globe visible.
