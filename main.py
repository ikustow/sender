import base64
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tonsdk.contract.token.nft import NFTItem
from tonsdk.utils import to_nano, bytes_to_b64str, Address
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from cryptography.fernet import Fernet

app = FastAPI()

class CreateMessageRequest(BaseModel):
    mnemonic: str
    key: str
    new_owner_address: str
    to_addr: str

def decrypt_strings(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message.split("\n")

@app.post("/send_message")
def send_message(request: CreateMessageRequest):
    key= request.key.encode() 
    mnemonic =  request.mnemonic.encode() 

    if not mnemonic:
        raise HTTPException(status_code=400, detail="Mnemonic cannot be empty")

    try:
        decrypted_mnemonic = decrypt_strings(mnemonic, key)
        print(decrypted_mnemonic)
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
            seqno=int(0x4),
            payload=body
        )

        boc = bytes_to_b64str(query["message"].to_boc(False))
        url = 'https://toncenter.com/api/v2/sendBoc'
        data = {"boc": boc}
        response = requests.post(url, json=data)

        return {"message": "Success", "response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
