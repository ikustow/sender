import asyncio

from TonTools import *

COLLECTION = 'EQBs85otZAYdYQNSUEUWg_C7DnKERAFvPaJtKcKlI9Po8S0e'

async def main():
    client = TonCenterClient(orbs_access=True)

    data = await client.get_collection(collection_address=COLLECTION)
    items = await client.get_collection_items(collection=data, limit_per_one_request=20)

    for item in items:
        print(item.address)
        
        data1 = await client.get_nft_items(nft_addresses=[item.address])

        print(data1[0]) 
  

asyncio.run(main())