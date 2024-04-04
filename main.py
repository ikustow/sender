from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tonsdk.contract.token.nft import NFTItem
from tonsdk.utils import to_nano, bytes_to_b64str, Address
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from cryptography.fernet import Fernet


def decrypt_strings(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    strings = decrypted_message.split("\n")  # Разделяем строку обратно на массив строк
    return strings

app = FastAPI()

class CreateMessgeRequest(BaseModel):
    mnemonic: str
    key: str

@app.post("/send_message")
def send_message(request: CreateMessgeRequest):
    key= request.key
    mnemonic = request.mnemonic
 
    decrypted_mnemonic = decrypt_strings(mnemonic, key)
 
    if mnemonic == '':
        raise HTTPException(status_code=400, detail="Mnemonic cannot be empty")

    try:
        mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=decrypted_mnemonic, version=WalletVersionEnum.v4r2, workchain=0)

        # Transfer logic
        body = NFTItem().create_transfer_body(new_owner_address=Address('UQD4452NIi3YSL4t7ECbPfzH5f3BsHXWltPkF19nNshL9bkB'))
        query = wallet.create_transfer_message(to_addr='EQBoHNzacteIGIeLVn7Fy4BO-RIQeQeMEvAN5UAlrxYDTH35',
                                               amount=to_nano(0.001, 'ton'),
                                               seqno=int(0x4),
                                               payload=body)

        # Convert the message to BOC and print (or return) it
        boc = bytes_to_b64str(query["message"].to_boc(False))
        

        return {"message": boc}

    except Exception as e:
        # Handle other exceptions or errors
        raise HTTPException(status_code=500, detail=str(e))