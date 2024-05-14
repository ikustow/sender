
from pydantic import BaseModel


class CreateMessageRequest(BaseModel):
    mnemonic: str
    key: str
    new_owner_address: str
    to_addr: str