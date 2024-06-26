
import json
from fastapi import HTTPException
import requests
from model.CreateMessageRequestClass import CreateMessageRequest
from pydantic import BaseModel
from tonsdk.contract.token.nft import NFTItem
from tonsdk.utils import to_nano, bytes_to_b64str, Address
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from cryptography.fernet import Fernet


def decrypt_strings(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message.split("\n")


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

        # Transfer logic
        body = NFTItem().create_transfer_body(new_owner_address=Address(request.new_owner_address))
        query = wallet.create_transfer_message(
            to_addr=request.to_addr,
            amount=to_nano(0.01, 'ton'),
            seqno=int(0x9),
            payload=body
        )

        boc = bytes_to_b64str(query["message"].to_boc(False))
        #url = 'https://toncenter.com/api/v2/sendBoc'
        #data = {"boc": boc}
        #response = requests.post(url, json=data)
        response = requests.post('https://toncenter.com/api/v2/sendBoc', data= json.dumps({"boc":boc})).json()
        return {"message": "Success", "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))