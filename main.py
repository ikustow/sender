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
from functions.collection import parse_response
from model.CreateMessageRequestClass import CreateMessageRequest

COLLECTION = 'EQBs85otZAYdYQNSUEUWg_C7DnKERAFvPaJtKcKlI9Po8S0e'



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
            seqno=int(0x9),
            payload=body
        )

        boc = bytes_to_b64str(query["message"].to_boc(False))
        response = requests.post('https://toncenter.com/api/v2/sendBoc', data= json.dumps({"boc":boc})).json()
        return {"message": "Success", "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collection")
async def get_collection():
   
    client = TonCenterClient(orbs_access=True)
    
    #data = await client.get_collection(collection_address=COLLECTION)
    #items = await client.get_collection_items(collection=data, limit_per_one_request=20)
    items = ['EQDkT6tXU784fXSjShCmu1-eMuiDQ0LkRewz4Ae8r-Z8eOjK','EQB4NG0xJXMgqfhkpc_vtgefPN9A6dtFBIyE3GjHMpyezLce',
             'EQBod5p-wtHwvsyn3zcqrlSzGffLEnIYCgY14ujNtYpv5QJu', 'EQB5XTy4fA-YFO4VxGIWCenajOnxi4I2-vcXHMxRDHUV52Un', 'EQBFBxa5M8FqaE_hHHj4d6-anzosUGPIy2d1ArZuwAyQFsnz']
    items_data = []
    parsed_items = []
    
    for item in items:
        nft_value = await client.get_nft_items(nft_addresses=[item.address])
        items_data.append([item.address, nft_value[0].metadata,nft_value[0].owner])
    
    for item_data_value in items_data:
        if item_data_value[2] == 'EQCwpZzbHVqKBtGgUEkMn0IziI1WBDMIOVXZxW2lLg2wwHVT':
            parsed_items.append({
                "address": item_data_value[0],
                "owner": item_data_value[2],
                **item_data_value[1]
            })
    
    return {"message": "Success", "response": parsed_items}