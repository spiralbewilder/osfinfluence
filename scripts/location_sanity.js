// Heuristic scanner for location/name/purpose mismatches using grantees.json (object keyed by recipient).
// Flags locations whose recipient/purpose text hints at a different country than the location string.
const fs = require('fs');

const granteesPath = process.argv[2] || 'grantees.json';
const raw = JSON.parse(fs.readFileSync(granteesPath, 'utf8'));

const entries = Array.isArray(raw)
  ? raw
  : Object.entries(raw).map(([name, val]) => ({ name, ...val }));

const countryMap = {
  'United States': 'United States', USA: 'United States', US: 'United States',
  'United Kingdom': 'United Kingdom', UK: 'United Kingdom', 'U.K.': 'United Kingdom', England: 'United Kingdom', Scotland: 'United Kingdom', Wales: 'United Kingdom', 'Northern Ireland': 'United Kingdom',
  Canada: 'Canada', Mexico: 'Mexico', 'Puerto Rico': 'Puerto Rico',
  France: 'France', Germany: 'Germany', Italy: 'Italy', Spain: 'Spain', Portugal: 'Portugal', Netherlands: 'Netherlands',
  Belgium: 'Belgium', Switzerland: 'Switzerland', Austria: 'Austria', Ireland: 'Ireland', Denmark: 'Denmark', Sweden: 'Sweden', Norway: 'Norway', Finland: 'Finland',
  Poland: 'Poland', Ukraine: 'Ukraine', Russia: 'Russia', 'Czech Republic': 'Czech Republic', Hungary: 'Hungary',
  Turkey: 'Turkey', Tunisia: 'Tunisia', Egypt: 'Egypt', Kenya: 'Kenya', 'South Africa': 'South Africa', Zambia: 'Zambia', Zimbabwe: 'Zimbabwe', Uganda: 'Uganda', Ethiopia: 'Ethiopia', Nigeria: 'Nigeria', Ghana: 'Ghana', Senegal: 'Senegal', Gambia: 'Gambia', Sudan: 'Sudan', Morocco: 'Morocco', Algeria: 'Algeria',
  Israel: 'Israel', Jordan: 'Jordan', Lebanon: 'Lebanon', Palestine: 'Palestine', Syria: 'Syria', Iraq: 'Iraq', Iran: 'Iran',
  India: 'India', Pakistan: 'Pakistan', Bangladesh: 'Bangladesh', Indonesia: 'Indonesia', Philippines: 'Philippines', Malaysia: 'Malaysia', Thailand: 'Thailand', Vietnam: 'Vietnam', Cambodia: 'Cambodia', Myanmar: 'Myanmar', China: 'China', Mongolia: 'Mongolia', Japan: 'Japan', 'South Korea': 'South Korea', Taiwan: 'Taiwan',
  Australia: 'Australia', 'New Zealand': 'New Zealand',
  Colombia: 'Colombia', Brazil: 'Brazil', Argentina: 'Argentina', Chile: 'Chile', Peru: 'Peru', Bolivia: 'Bolivia', Paraguay: 'Paraguay', Uruguay: 'Uruguay',
  'Costa Rica': 'Costa Rica', Panama: 'Panama', Guatemala: 'Guatemala', Honduras: 'Honduras', 'El Salvador': 'El Salvador', Nicaragua: 'Nicaragua', Cuba: 'Cuba', Haiti: 'Haiti', 'Dominican Republic': 'Dominican Republic', Jamaica: 'Jamaica'
};
const countryNames = Object.keys(countryMap);
const normalizeCountry = (name) => (name && countryMap[name.trim()]) || null;
const countryFromLoc = (loc) => {
  if (!loc) return null;
  const parts = loc.split(',').map((s) => s.trim()).filter(Boolean);
  const last = parts[parts.length - 1];
  return normalizeCountry(last);
};
const countryHints = (text) => {
  const lower = (text || '').toLowerCase();
  const hits = new Set();
  for (const c of countryNames) {
    if (lower.includes(c.toLowerCase())) hits.add(countryMap[c]);
  }
  return hits;
};

const buckets = new Map();
for (const e of entries) {
  const locs = e.locations || (e.location ? [e.location] : []);
  const texts = [e.name || '', ...(e.purposes || []), ...(e.addresses || [])];
  const hintsCombined = new Set();
  for (const t of texts) {
    for (const h of countryHints(t)) hintsCombined.add(h);
  }
  for (const loc of locs) {
    const locCountry = countryFromLoc(loc);
    const bucket = buckets.get(loc) || { loc, count: 0, locCountry, hintCountries: new Set(), samples: [] };
    bucket.count += 1;
    for (const h of hintsCombined) bucket.hintCountries.add(h);
    if (bucket.samples.length < 2) bucket.samples.push(e.name || 'Recipient');
    buckets.set(loc, bucket);
  }
}

const candidates = Array.from(buckets.values())
  .filter((b) => b.count >= 2)
  .filter((b) => {
    if (!b.locCountry) return b.hintCountries.size > 0;
    return Array.from(b.hintCountries).some((h) => h && h !== b.locCountry);
  })
  .sort((a, b) => b.count - a.count)
  .slice(0, 40);

console.log('Possible country-context mismatches (top by count):');
for (const b of candidates) {
  const hints = Array.from(b.hintCountries).join('; ') || '—';
  const samples = b.samples.join(' | ');
  console.log(`${b.loc} | count ${b.count} | locCountry ${b.locCountry || 'unknown'} | hints ${hints} | samples: ${samples}`);
}
