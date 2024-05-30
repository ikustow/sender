import json
import aiohttp
import asyncio

async def get_data():
    main_address = 'UQCwpZzbHVqKBtGgUEkMn0IziI1WBDMIOVXZxW2lLg2wwCiW'
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://tonapi.io/v2/accounts/{main_address}/nfts?offset=0&indirect_ownership=true') as response:
            if response.status == 200:
                json_response = await response.json()
                nft_items = json_response.get('nft_items', [])

                filtered_items = [item for item in nft_items if item.get('collection', {}).get('address') == '0:6bb3fa2b2ec7536c7b26c74636c07486ee446ce508e99fb6a89f4f9320590ba5']

                parsed_items = []
                for item in filtered_items:
                    metadata = item.get('metadata')
                    if metadata:
                        parsed_item = {
                            'address': item['address'],
                            'name': metadata['description'],
                            'image': metadata['image']
                        }
                        parsed_items.append(parsed_item)

                return parsed_items
            else:
                print(f'Error: {response.status}')
                return []

if __name__ == '__main__':
    parsed_data = asyncio.run(get_data())
    print(parsed_data)
