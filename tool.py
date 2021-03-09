import json
import csv

#Network request related imports
import certifi
import requests
import urllib3

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

def write_csv_log(items, headers, name):
    try:

        with open(name + '.csv', 'w', encoding="utf-8-sig") as f:
            dw = csv.DictWriter(f, fieldnames=headers, delimiter=',', lineterminator='\n', extrasaction='ignore')
            dw.writeheader()
            dw.writerows(items)
        
    except Exception as e:
        print("Error writing" , name , "log:", e)

with open('source.csv', 'r', encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    cards = list(reader)

endpointBase = "http://yugiohprices.com/api/price_for_print_tag/"
output = []
x = 1

records = len(cards)

for card in cards:

    try:

        print("Processing",card,x,"of",records)
        x = x + 1

        url = endpointBase + card['Code']

        response = requests.get(url)
        jsonResponse = json.loads(response.content)

        content = jsonResponse['data']
        content['card_name'] = content['name']
        content.update(content['price_data'])
        content.update(content['price_data']['data']['prices'])
        output.append(content)

    except Exception as e:
        print(e)


headers = ["print_tag","card_name","card_type","family","type","name","rarity","high","low","average","shift","shift_3","shift_7","shift_21","shift_30","shift_90","shift_180","shift_365","updated_at"]
write_csv_log(output,headers,"output")
