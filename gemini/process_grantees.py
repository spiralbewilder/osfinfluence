import json
import time
import csv
import sys
import os
from geopy.geocoders import Photon
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Initialize geolocator
geolocator = Photon(user_agent="grantee_locator")

CACHE_FILE = 'geocode_cache.json'

# Constants from HTML
countryNameMap = {
    'US': 'United States', 'USA': 'United States',
    'GB': 'United Kingdom', 'UK': 'United Kingdom', 'GBR': 'United Kingdom',
    'FR': 'France', 'FRA': 'France', 'DE': 'Germany', 'DEU': 'Germany', 'IT': 'Italy', 'ITA': 'Italy',
    'ES': 'Spain', 'ESP': 'Spain', 'NL': 'Netherlands', 'NLD': 'Netherlands', 'BE': 'Belgium', 'BEL': 'Belgium',
    'SE': 'Sweden', 'SW': 'Sweden', 'SWE': 'Sweden', 'NO': 'Norway', 'NOR': 'Norway',
    'CA': 'Canada', 'CAN': 'Canada', 'AU': 'Australia', 'AUS': 'Australia', 'NZ': 'New Zealand', 'NZL': 'New Zealand',
    'BR': 'Brazil', 'BRA': 'Brazil', 'AR': 'Argentina', 'ARG': 'Argentina', 'CL': 'Chile', 'CHL': 'Chile',
    'PE': 'Peru', 'PER': 'Peru', 'CO': 'Colombia', 'COL': 'Colombia', 'MX': 'Mexico', 'MEX': 'Mexico',
    'EG': 'Egypt', 'EGY': 'Egypt', 'ZA': 'South Africa', 'ZAF': 'South Africa', 'KE': 'Kenya', 'KEN': 'Kenya',
    'ID': 'Indonesia', 'IDN': 'Indonesia', 'TH': 'Thailand', 'THA': 'Thailand', 'IN': 'India', 'IND': 'India',
    'PK': 'Pakistan', 'PAK': 'Pakistan', 'BD': 'Bangladesh', 'BGD': 'Bangladesh', 'TR': 'Turkey', 'TUR': 'Turkey',
    'UA': 'Ukraine', 'UKR': 'Ukraine', 'PL': 'Poland', 'POL': 'Poland', 'KR': 'South Korea', 'KOR': 'South Korea',
    'JP': 'Japan', 'JPN': 'Japan', 'PH': 'Philippines', 'PHL': 'Philippines', 'MY': 'Malaysia', 'MYS': 'Malaysia',
    'TW': 'Taiwan', 'TWN': 'Taiwan', 'RQ': 'Puerto Rico',
    'CB': 'Cambodia', 'KHM': 'Cambodia', 'ET': 'Ethiopia', 'ETH': 'Ethiopia', 'HA': 'Haiti', 'HTI': 'Haiti',
    'LT': 'Lithuania', 'LTU': 'Lithuania', 'GV': 'Guinea', 'GIN': 'Guinea', 'TS': 'Tunisia', 'TUN': 'Tunisia',
    'EZ': 'Czech Republic', 'CZE': 'Czech Republic', 'PO': 'Portugal', 'PRT': 'Portugal', 'SP': 'Spain',
    'SU': 'Sudan', 'SDN': 'Sudan', 'KG': 'Kyrgyzstan', 'KGZ': 'Kyrgyzstan',
    'SZ': 'Switzerland', 'SF': 'South Africa', 'OC': 'United Kingdom'
}

cityCountryOverrides = {
    'London': 'United Kingdom',
    'Geneva': 'Switzerland',
    'Zurich': 'Switzerland',
    'Johannesburg': 'South Africa',
    'Vienna': 'Austria',
    'Rio De Janeiro': 'Brazil',
    'Rio De Janeiro ': 'Brazil'
}

import re

def titleCase(s):
    return re.sub(r'\b([a-z])', lambda m: m.group(1).upper(), s.lower())

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def geocode_address(address):
    for attempt in range(2):  # Retry once
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except (GeocoderTimedOut, GeocoderUnavailable):
            time.sleep(1)  # Longer sleep on retry
            continue
    return None, None

# Load persistent cache
cache = load_cache()

# Collect all data first
all_rows = []
queries = set()
for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('recipient_name', '').strip()
            if not name:
                continue
            address = (row.get('recipient_address1', '') + ' ' + row.get('recipient_address2', '')).strip()
            cityRaw = row.get('recipient_city', '').strip()
            city = titleCase(cityRaw) if cityRaw else ''
            stateRaw = row.get('recipient_state', '').strip()
            state = titleCase(stateRaw) if stateRaw else ''
            countryRaw = (row.get('recipient_country', '').strip() or 'US').upper()
            overrideCountry = cityCountryOverrides.get(city, None) if city else None
            countryFull = overrideCountry or countryNameMap.get(countryRaw, countryRaw)
            geocodeQueries = []
            if city and state:
                geocodeQueries.append(f"{city}, {state}, {countryFull}")
            if city and not state:
                geocodeQueries.append(f"{city}, {countryFull}")
            if not city and state:
                geocodeQueries.append(f"{state}, {countryFull}")
            if city:
                geocodeQueries.append(city)
            if overrideCountry and overrideCountry != countryFull:
                geocodeQueries.append(f"{city}, {overrideCountry}")
            geocodeQueries.append(countryFull)
            uniqueQueries = list(set(filter(None, geocodeQueries)))
            all_rows.append((name, address, uniqueQueries, filename))
            for q in uniqueQueries:
                queries.add(q)
            if address:
                queries.add(address)

print(f"Found {len(all_rows)} rows, {len(queries)} unique queries", file=sys.stderr)

# Geocode uniques only
geocoded_new = 0
for query in queries:
    if query in cache and cache[query] is not None:
        continue
    print(f"Geocoding new query: {query[:50]}...", file=sys.stderr)
    time.sleep(0.2)  # Rate limit
    lat, lng = geocode_address(query)
    cache[query] = (lat, lng) if lat is not None else None
    geocoded_new += 1
    if geocoded_new % 100 == 0:  # Save every 100
        save_cache(cache)
        print(f"Saved cache at {geocoded_new} geocodes", file=sys.stderr)

print(f"Geocoded {geocoded_new} new queries", file=sys.stderr)

# Save updated cache (final)
save_cache(cache)

# Output geocodes JSON (location -> coords)
geocodes_output = {k: {"lat": v[0], "lng": v[1]} for k, v in cache.items() if v is not None}
print(json.dumps(geocodes_output, indent=2))