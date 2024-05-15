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
from functions.sending import send_message
from model.CreateMessageRequestClass import CreateMessageRequest

app = FastAPI()

@app.post("/send_message")
async def handle_send_message(request: CreateMessageRequest):
    return send_message(request)

@app.get("/collection")
async def get_collection():
    COLLECTION = 'EQBs85otZAYdYQNSUEUWg_C7DnKERAFvPaJtKcKlI9Po8S0e'
    client = TonCenterClient(orbs_access=True)

    data = await client.get_collection(collection_address=COLLECTION)
    items = await client.get_collection_items(collection=data, limit_per_one_request=20)
    items_data = []
    for item in items:
        #print(item.address)
        
        nft_value = await client.get_nft_items(nft_addresses=[item.address])
        items_data.append([item.address, nft_value[0].metadata])
        #print(data1[0]) 
    return {"message": "Success", "response": items_data}