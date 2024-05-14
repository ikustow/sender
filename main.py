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

def decrypt_strings(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message.split("\n")

@app.post("/send_message")
async def handle_send_message(request: CreateMessageRequest):
    return send_message(request)
