import asyncio
from TonTools import *
import base64
import json
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tonsdk.contract.token.nft import NFTItem
from tonsdk.utils import to_nano, bytes_to_b64str, Address
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from cryptography.fernet import Fernet
from model.CreateMessageRequestClass import CreateMessageRequest

COLLECTION = 'EQBrs_orLsdTbHsmx0Y2wHSG7kRs5Qjpn7aon0-TIFkLpcoc'



def decrypt_strings(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message.split("\n")


app = FastAPI()

@app.post("/send_message")
def send_message(request: CreateMessageRequest):
    key= request.key.encode() 
    mnemonic =  request.mnemonic.encode() 

    if not mnemonic:
        raise HTTPException(status_code=400, detail="Mnemonic cannot be empty")

    try:
        decrypted_mnemonic = decrypt_strings(mnemonic, key)
        mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(
            mnemonics=decrypted_mnemonic, 
            version=WalletVersionEnum.v4r2, 
            workchain=0
        )
        body = NFTItem().create_transfer_body(new_owner_address=Address(request.new_owner_address))
        query = wallet.create_transfer_message(
            to_addr=request.to_addr,
            amount=to_nano(0.01, 'ton'),
            seqno=int(0x26),
            payload=body
        )

        boc = bytes_to_b64str(query["message"].to_boc(False))
        response = requests.post('https://toncenter.com/api/v2/sendBoc', data= json.dumps({"boc":boc})).json()
        return {"message": "Success", "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collection")
async def get_collection():
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

                return {"message": "Success", "response": parsed_items}
            else:
                print(f'Error: {response.status}')
                return {"message": "Success", "response": parsed_items}
    
   
