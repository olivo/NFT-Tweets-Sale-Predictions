import json
import requests
from urllib.request import urlopen, Request
import re


def get_collections(offset, limit):

    url = "https://api.opensea.io/api/v1/collections"

    #querystring = {"offset":"0","limit":"300"}
    print("Offset: " + str(offset))
    querystring = {"offset":offset,"limit":limit}

    response = requests.request("GET", url, params=querystring)

    #print(response.text)

    result = json.loads(response.text)

    collections = []
    print(result)
    for collection in result['collections']:
        collections.append(collection['slug'])

    #print(collections)
    return collections

def get_assets():
    # Example collection name: seikatsukun Collection
     
    url = "http://api.opensea.io/api/v1/assets"

    #querystring = {"order_direction":"desc","offset":"0","limit":"20"}
    #querystring = {"order_direction":"desc","offset":"0","limit":"50", "collection":"boredapeyachtclub"}
    querystring = {"order_direction":"asc","offset":"100","limit":"50", "collection":"the-sevens-official"}

    response = requests.request("GET", url, params=querystring)

    print(response.text)

    # Write down assets response
    f = open("assets_response.txt", "w")
    f.write(response.text)
    f.close()

    result = json.loads(response.text)

    #print(result['assets'])

    for asset in result['assets']:
        print(asset['id'])
        print(asset['permalink'])


    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    #asset_url = asset['permalink']
    asset_url = 'https://opensea.io/assets/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/1704'

    req = Request(url=asset_url, headers=headers) 

    html = urlopen(req).read()
    

    # Write down asset HTML.
    f = open("html_response.txt", "w")
    f.write(html.decode())
    f.close()

    #response = requests.request("GET", asset['permalink'])
    decoded_html = html.decode()
    buy_price_location_start = decoded_html.index("Price--amount\">") + len("Price--amount\">")
    buy_price_location_end = buy_price_location_start + decoded_html[buy_price_location_start:].index("<")
    # Price--raw-symbol
    listing_price = float(decoded_html[buy_price_location_start : buy_price_location_end])
    print("Listing price: " + str(listing_price))

    offers_start_index = decoded_html.index("<span>Offers")
    #print("Offers start index: " + str(offers_start_index))
    print(decoded_html[offers_start_index : offers_start_index + 100])
    offer_price_start = decoded_html[offers_start_index:].index("Price--amount\">") + len("Price--amount\">")
    #print("Offer price start: " + str(offer_price_start))
    print(decoded_html[offers_start_index + offer_price_start : offers_start_index + offer_price_start + 1000])

# zed-run-official
def get_floor(collectionName):
# https://opensea.io/collection/zed-run-official?collectionSlug=zed-run-official&search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    #asset_url = asset['permalink']
    asset_url = 'https://opensea.io/collection/{}?collectionSlug={}&search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW'\
        .format(collectionName, collectionName)
    print(asset_url)
    req = Request(url=asset_url, headers=headers) 

    html = urlopen(req).read()

    #f = open("html_sorted_response.txt", "r")
    #html = f.read()
    #print(html[:500])
    
    #print(html)

    # Write down asset HTML.
    #f = open("html_sorted_response.txt", "w")
    #f.write(html.decode())
    #f.write(str(html))
    #f.close()
    #exit()
    html = str(html)
    #regex_matches = re.findall(r"((?:(?<=email=)|(?<=secret=))[^;]+)", s)
    # Price--amount">0.038<!
    regex_matches = re.findall(r"Price--amount\">[^<]*<!-- --> <span class=\"Price--raw-symbol\"></span></div></div></div></div><div class=\"AssetCardFooter--annotations\">", html)
    prices = []
    #last_prices = []

    for i in range(len(regex_matches)):
        regex_match = regex_matches[i]
        print(regex_match)
        number = regex_match[regex_match.index(">") + 1:regex_match.index("<")]
        # Remove commas from values like 1,000,000
        number = number.replace(",", "")

        number = float(number)
        #if i % 2 == 0:
        prices.append(number)
        #else:
        #    last_prices.append(number)

    prices = sorted(list(set(prices)))
    #prices.sort()
    if len(prices) > 1:
        print("Prices:")
        for price in prices:
            print(price)

        if len(prices) > 1:
            print("The spread is :" + str(prices[1] - prices[0]))
            return (prices[0], prices[1])

    return (0,0)





#get_assets()
#collectionName = 'zed-run-official'
#collectionName = 'space-punks-club'
#collectionName = 'cryptokitties'
collectionName = 'thecryptodads'

#get_floor(collectionName)
#collections = []
#limit = 300
#offset = 0

#while True:
#    print("Hello")
#    new_collections = get_collections(str(offset), str(limit))
#    print(limit)
#    
#    for collection in new_collections:
#        collections.append(collection)
    
#    offset += limit

    #if offset >= 50000 or new_collections is None or new_collections == []:
#    if offset >= 10000 or new_collections is None or new_collections == []:
#        break
    #break

#print(len(collections))
#print(collections)
#exit(1)

#collections = get_collections()
collections = ['cryptopunks', 'sipheriansurge', 'boredapeyachtclub','zed-run-official', \
    'punks-comic', 'guardians-of-the-metaverse', 'theprojecturs', 'cool-cats-nft', \
    'cryptoadz-by-gremplin', 'cyberkongz', 'pudgypenguins', 'savage-droids', \
    'vgds', 'meebits', 'veefriends', '0n1-force', 'parallelalpha', 'moonpass', \
    'based-fish-mafia', 'fusionape', 'adam-bomb-squad', 'supducks', 'rumble-kong-league', \
    'space-punks-club', 'cryptokitties', 'thecryptodads', 'world-of-women-nft', 'blitmap', \
    'tie-dye-ninjas', 'wicked-ape-bone-club', 'octohedz', 'roguesocietybot', 'guttercatgang', \
    'cyberkongz-vx', 'koala-intelligence-agency', 'skvllpvnkz-hideout', 'gutter-species-mint-pass', \
    'fluf-world', 'acclimatedmooncats', 'cryptocannabisclub', 'cryptozoo-co', 'crypto-pills-by-michh-klein', \
    'space-dinos-club', 'tunesproject', 'rtfkt-capsule-space-drip-1-2', 'dotdotdots', 'marscatsvoyage', \
    'etherlambos', 'gutterrats', 'dogesoundclub-mates', 'the-doge-pound', 'defaced-n-friends', 'fatales', \
    'fvck-crystal', 'nyan-cat-official', 'uwucrew', 'bastard-gan-punks-v2', 'goonsofbalatroon', 'theo-nft', \
    'great-ape-society', 'royalsocietyofplayers', 'purrnelopes-country-club', 'stoner-cats-official', \
    'non-fungible-soup', 'sympathyforthedevils', 'dystopunks-v2', 'doge-pound-puppies-real', 'realms-of-ether-1', \
    'boring-bananas-company', 'illuvium', 'chibidinos', 'ape-gang', 'thewickedcraniums', 'bullsontheblock', 'collectvox', \
    'bored-mummy-waking-up', 'vogu', 'lonelyalienspaceclub', 'chunkychickens-v2', 'rtfkt-capsule-space-drip', 'animetas', \
    'voxies', 'sneaky-vampire-syndicate', 'omnimorphs', '0xvampire-project', 'uunicorns', 'impermanent-digital', \
    'evolved-apes-inc', 'crypto-hobos', 'dapperdinosnft', 'thewynlambo', 'onchainmonkey'
    ]

# Overriding collections for testing.
collections = ['boredapeyachtclub']

floors = dict()

for collection in collections:
    print("Gathering data for collection: " + collection)
    try:
        floor = get_floor(collection)
        lowest_price = floor[0]
        spread = floor[1] - floor[0]

        if spread >= 0.05:
            floors[collection] = (spread, lowest_price)

    except:
        print("Found exception")

#print("The spreads and lowest prices are:")
#for collection in floors:
#    print(collection + ": " + str(floors[collection]))

floor_tuples = []
for collection in floors:
    floor_tuples.append((collection, floors[collection][0], floors[collection][1]))

floor_tuples.sort(key=lambda x: x[1], reverse=True)

print("The spreads and lowest prices are:")
for floor_tuple in floor_tuples:
    print(floor_tuple[0] + ": " + str(floors[floor_tuple[0]]))

# Calling proper opensea API.
#opensea_collection = 'boredapeyachtclub'
opensea_collection = 'theyakuzacatssociety'

retrieve_assets_url = 'https://api.opensea.io/api/v1/assets?collection={}&limit=1'\
        .format(opensea_collection)
req = Request(url=retrieve_assets_url) 

html = urlopen(req).read()

html = str(html)

# Assets dump
f = open("opensea_assets_response.txt", "w")
f.write(html)
f.close()

# Getting events for asset with token id = 9974
token_id = 8924
asset_contract_address = '0x454cbc099079dc38b145e37e982e524af3279c44'
retrieve_events_url = 'https://api.opensea.io/api/v1/events?only_opensea=false&token_id={}&asset_contract_address={}&collection_slug={}&offset=100&limit=100'\
    .format(token_id, asset_contract_address, opensea_collection)
#'https://api.opensea.io/api/v1/events?only_opensea=false&token_id={}&limit=20&collection_slug={}'\
#        .format(token_id, opensea_collection)
headers = {'Accept': 'application/json'}
req = Request(url=retrieve_events_url, headers = headers) 

html = urlopen(req).read()

html = str(html)

# Events dump
f = open("opensea_events_response.txt", "w")
f.write(html)
f.close()

