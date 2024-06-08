from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet, generate_faucet_wallet

ripple_network = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(ripple_network)


def generate_wallet():
    _wallet = generate_faucet_wallet(client, debug=True)
    print(_wallet)
    return _wallet


w = generate_wallet()
print(w.address, w.public_key, w.private_key)
