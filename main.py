import base64
import json
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tonsdk.contract.token.nft import NFTItem
from tonsdk.utils import to_nano, bytes_to_b64str, Address
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from cryptography.fernet import Fernet

from functions.collection import get_collection
from functions.sending import send_message
from model.CreateMessageRequestClass import CreateMessageRequest

app = FastAPI()

@app.post("/send_message")
async def handle_send_message(request: CreateMessageRequest):
    return send_message(request)

@app.get("/collection")
async def handle_get_collection():
    return get_collection()