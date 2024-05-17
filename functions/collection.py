import asyncio
from TonTools import TonCenterClient

COLLECTION = 'EQBrs_orLsdTbHsmx0Y2wHSG7kRs5Qjpn7aon0-TIFkLpcoc'

async def get_collection1():
    client = TonCenterClient(orbs_access=True)
    
    data = await client.get_collection(collection_address=COLLECTION)
    items = await client.get_collection_items(collection=data, limit_per_one_request=20)
  
    items_data = []
    parsed_items = []
    

    for item in items:

        nft_value = await client.get_nft_items(nft_addresses=[item.address])

        if nft_value:
            items_data.append([item.address, nft_value[0].metadata, nft_value[0].owner])
        else:
            print(f"Error: No data returned for item {item}")
    
    for item_data_value in items_data:
       
        if item_data_value[2] == 'EQCwpZzbHVqKBtGgUEkMn0IziI1WBDMIOVXZxW2lLg2wwHVT':
            parsed_items.append({
                "address": item_data_value[0],
                "owner": item_data_value[2],
                **item_data_value[1]
            })
    
    return {"message": "Success", "response": parsed_items}

# Асинхронный запуск функции и вывод результата
async def main():
    res = await get_collection1()
    print(res)

# Запуск основного асинхронного метода
asyncio.run(main())
