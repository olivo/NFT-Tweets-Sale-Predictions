import datetime
import json
import requests
from urllib.request import urlopen, Request
import re

class Asset:
    def __init__(self, properties):
        self.id = properties['id']
        self.token_id = properties['token_id']
        self.num_sales = properties['num_sales']
        self.background_color = properties['background_color']
        self.image_url = properties['image_url']
        self.name = properties['name']
        self.permalink = properties['permalink']
        self.asset_contract = properties['asset_contract']
        self.collection = properties['collection']
        self.collection_slug = self.collection['slug']

        # Process traits, which are of the form:
        # {'trait_type': 'body', 'value': 'blue cat skin', 'display_type': None, 'max_value': None, 'trait_count': 9933, 'order': None}
        self.trait_dict = dict()
        for trait_bag in properties['traits']:
            trait_type = trait_bag['trait_type']
            trait_value = trait_bag['value']
            trait_count = trait_bag['trait_count']
            self.trait_dict[trait_type + "_value"] = trait_value
            self.trait_dict[trait_type + "_count"] = trait_count

        self.traits = properties['traits']

        #print("traits type", type(self.traits))
        #print("traits: " + str(self.traits))

class Event:
    def __init__(self, asset, properties):
        self.asset = asset
        self.auction_type = properties['auction_type']
        self.bid_amount = properties['bid_amount']
        self.ending_price = properties['ending_price']
        self.event_type = properties['event_type']
        self.created_date = properties['created_date']
        self.total_price = properties['total_price']
        self.quantity = properties['quantity']
 
"""
"asset_bundle": null,
      "auction_type": null,
      "bid_amount": "20750000000000000000",
      "collection_slug": "boredapeyachtclub",
      "contract_address": "0x7be8076f4ea4a4ad08075c2508e481d6c946d12b",
      "created_date": "2021-10-21T06:50:20.737876",
      "custom_event_name": null,
      "dev_fee_payment_event": null,
      "duration": null,
      "ending_price": null,
      "event_type": "offer_entered",
      "total_price": null,
      "quantity": 1,
"""

def get_assets(collection, offset = 0, limit = 1):
    assets = []
    retrieve_assets_url = 'https://api.opensea.io/api/v1/assets?collection={}&offset={}&limit={}'\
        .format(opensea_collection, offset, limit)
    req = Request(url=retrieve_assets_url) 

    html = urlopen(req).read()

    assets_response = json.loads(html)


    f1 = open("opensea_assets_response.txt", "w")
    f1.write(html.decode())
    f1.close()


    f = open("assets.txt", "a")
    
    
    #f.write(html)
    #f.write('id,token_id,image_url,permalink,asset_contract,collection,traits\n')

    collection_traits = set()

    for asset in assets_response['assets']:
        asset_instance = Asset(asset)
        assets.append(asset_instance)

        # Download image
        #img_data = requests.get(asset_instance.image_url).content
        #with open('images/{}.jpg'.format(asset_instance.token_id), 'wb') as handler:
        #    handler.write(img_data)

        # Add traits from the NFT to the global list.
        for trait in asset_instance.traits:
            # Sample.
            # "trait_type":"face","value":"mononoke","display_type":null,"max_value":null,"trait_count":237,"order":null
            collection_traits.add(trait['trait_type'])

        #f.write(str(asset_instance.id) + "," + str(asset_instance.token_id) + "," +  str(asset_instance.image_url) + "," + str(asset_instance.permalink) + "," + str(asset_instance.asset_contract) + "," + str(asset_instance.collection) + "," + str(asset_instance.traits) + "\n")

    #f.close()
    f.write('id,token_id,image_url,permalink,collection')
    #print(collection_traits)
    for trait in collection_traits:
        f.write("," + trait+"_value"+","+trait+"_count")
        #print("Hello")
    f.write("\n")

    for asset in assets:
        f.write(str(asset.id) + "," + str(asset.token_id) + "," +  str(asset.image_url) + "," + str(asset.permalink) + "," + str(asset.collection_slug))
        for trait in collection_traits:
            #print("TRAIT:", trait)
            #print("traits:", asset.traits)
            if trait+"_value" in asset.trait_dict:
                f.write("," + str(asset.trait_dict[trait+"_value"]) + "," + str(asset.trait_dict[trait+"_count"]))
            else:
                f.write("," + str(0))
        f.write("\n")

    return assets

def get_events(assets, offset = 0, limit = 1, epoch = datetime.datetime(2022,3,1,0,0).timestamp()):
    events = []

    f1 = open("events.txt", "a")

    f1.write('token_id,collection,event_type,auction_type,bid_amount,ending_price,created_date,total_price,quantity\n')
    num_asset = 0

    for asset in assets:
        
        print("Processing events of asset", str(num_asset))
        num_asset += 1
        
        current_offset = 0
        while True:
            # Retrieving sale events.
            retrieve_events_url = 'https://api.opensea.io/api/v1/events?only_opensea=false&token_id={}&asset_contract_address={}&collection_slug={}&offset={}&limit={}&occurred_after={}&event_type'\
            .format(asset.token_id, asset.asset_contract['address'], asset.collection['slug'], current_offset, limit, epoch, 'successful')

            #print(retrieve_events_url)
    
            headers = {'Accept': 'application/json'}
            req = Request(url=retrieve_events_url, headers = headers) 

            html = urlopen(req).read()

            events_response = json.loads(html)

            f = open("opensea_events_response.txt", "w")
            f.write(html.decode())
            f.close()

            if len(events_response['asset_events']) == 0:
                break

            for event in events_response['asset_events']:
                event_instance = Event(asset, event)
                events.append(event_instance)

                f1.write('{},{},{},{},{},{},{},{},{}\n'\
                    .format(event_instance.asset.token_id, event_instance.asset.collection_slug, event_instance.event_type,\
                        event_instance.auction_type, event_instance.bid_amount, event_instance.ending_price, event_instance.created_date,\
                            event_instance.total_price, event_instance.quantity))
            #self.asset = asset
            #self.auction_type = properties['auction_type']
            #self.bid_amount = properties['bid_amount']
            #self.ending_price = properties['ending_price']
            #self.event_type = properties['event_type']
            #self.created_date = properties['created_date']
            #self.total_price = properties['total_price']
            #self.quantity = properties['quantity']
            current_offset += limit

    return events

# Calling proper opensea API.
#opensea_collection = 'boredapeyachtclub'
#opensea_collection = 'theyakuzacatssociety'
opensea_collection = 'cool-cats-nft'

num_assets= 10000
assets = []
for offset in range(0, num_assets, 50):
    print("Processing asset offset", str(offset))
#for offset in range(0, 2, 50):
    current_assets = get_assets(opensea_collection, offset, limit=50)
    #current_assets = get_assets(opensea_collection, offset, limit=2)
    for asset in current_assets:
        assets.append(asset)

print("LEN ASSETS", len(assets))
# Assets dump
#f = open("opensea_assets_response.txt", "w")
#f.write(html)
#f.close()

exit()

# Getting events for asset with token id of the last asset
token_id = assets[-1].token_id
asset_contract_address = assets[-1].asset_contract['address']

events = get_events(assets, offset=0, limit=300, epoch = datetime.datetime(2021,10,1,0,0).timestamp())

print(events[-1].event_type)
print(events[-1].bid_amount)
print(events[-1].auction_type)
print(events[-1].ending_price)

#for event in events:
#    if event.event_type != "offer_entered":
#        print(event.event_type)
#        print(event.bid_amount)
#        print(event.auction_type)
#        print(event.ending_price)

# Events dump
#f = open("opensea_events_response.txt", "w")
#f.write(html)
#f.close()

