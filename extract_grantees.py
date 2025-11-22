import csv
import os
import json

grantees = {}
for year in range(2020, 2024):
    filename = f'{year}.csv'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['recipient_name'].strip()
                if name:
                    city = row['recipient_city'].strip()
                    state = row['recipient_state'].strip()
                    country = row['recipient_country'].strip()
                    address1 = row['recipient_address1'].strip()
                    address2 = row['recipient_address2'].strip()
                    postal = row['recipient_postal'].strip()
                    purpose = row['purpose'].strip()
                    loc = f'{city}, {state}, {country}'.strip(', ')
                    if name not in grantees:
                        grantees[name] = {
                            'locations': [loc],
                            'addresses': [f'{address1} {address2}'.strip()],
                            'purposes': [purpose]
                        }
                    else:
                        if loc not in grantees[name]['locations']:
                            grantees[name]['locations'].append(loc)
                        if f'{address1} {address2}'.strip() not in grantees[name]['addresses']:
                            grantees[name]['addresses'].append(f'{address1} {address2}'.strip())
                        if purpose not in grantees[name]['purposes']:
                            grantees[name]['purposes'].append(purpose)

with open('grantees.json', 'w') as f:
    json.dump(grantees, f, indent=2)
print('Extracted', len(grantees), 'unique grantees')