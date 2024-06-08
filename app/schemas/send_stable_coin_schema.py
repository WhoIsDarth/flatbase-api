from pydantic import BaseModel


class SendStableCoinSchema(BaseModel):
    amount: float
    receiver_address: str
