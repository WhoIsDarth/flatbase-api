# Custom app imports
from tempx import genereate_wallet
# XRPL imports
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import TrustSet, Payment
from xrpl.models.requests import AccountInfo
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, TrustSet, AccountSet, AccountSetFlag
from xrpl.models.requests import AccountInfo
from xrpl.transaction import submit_and_wait
from xrpl.models.transactions.account_set import AccountSetAsfFlag
import xrpl
from xrpl.account import get_balance

ripple_network = "https://s.altnet.rippletest.net:51234/"

class CreateStableCoin:

    """
    
    """
    
    def __init__(self, 
                 issuer_wallet:Wallet, 
                 holder_wallet:Wallet,
                 amount_of_tokens:int, # The amount of coins
                 stable_coin_name:str, # The name of the stable coin
                 amount_to_issue:int, # Amount to issue
                 ):
        self.client = JsonRpcClient(ripple_network)
        self.issuer_wallet = issuer_wallet
        self.holder_wallet = holder_wallet
        self.amount_of_tokens = amount_of_tokens
        self.stable_coin_name = stable_coin_name
        self.amount_to_issue = amount_to_issue

    def __set_ripple(self) -> AccountSet:
        account_set_tx = AccountSet(
            account=self.issuer_wallet.classic_address,
            set_flag=AccountSetAsfFlag.ASF_DEFAULT_RIPPLE
        )
        return account_set_tx

    def __create_trustline(self) -> TrustSet:
        trust_set_tx = TrustSet(
            account=self.holder_wallet.classic_address,
            limit_amount={
                "currency": self.stable_coin_name,
                "value": str(self.amount_of_tokens),  # 1,000,000 units of GOLD
                "issuer": self.issuer_wallet.classic_address
            }
        )
        return trust_set_tx

    def __issue_stable_coin(self) -> Payment:
        payment_tx = Payment(
            account=self.issuer_wallet.classic_address,
            destination=self.holder_wallet.classic_address,
            amount={
                "currency":self.stable_coin_name,
                "value": str(self.amount_to_issue),  # 1,000,000 units of GOLD
                "issuer": issuer_wallet.classic_address
            }
        )
        return payment_tx
    
    def __validate(self) -> AccountInfo:
        account_info = AccountInfo(
            account=self.holder_wallet.classic_address,
            ledger_index="validated"
        )
        response = self.client.request(account_info)
        print(4, response)

    def create_stable_coin(self):

        # Set default Ripple flag to allow token issuing
        account_set_tx = self.__set_ripple()
        response = submit_and_wait(account_set_tx, self.client, self.issuer_wallet)
        print(1, response)

        # Create a trust line from the holder to the issuer for the stablecoin 
        trust_set_tx = self.__create_trustline()
        response = submit_and_wait(trust_set_tx, self.client, self.holder_wallet)
        print(2, response)

        # Issue some amount of the stable coin from the issuer to the holder
        payment_tx = self.__issue_stable_coin()
        response = submit_and_wait(payment_tx, self.client, self.issuer_wallet)
        print(3, response)

        self.__validate()

class CreateFlatCoin:

    """
    
    """

    def __init__(self, issuer_wallet, holder_wallet):
        pass
        self.client

    def __create_trustline(holder_wallet, issuer_wallet, currency, limit):
        trust_set_tx = TrustSet(
            account=holder_wallet.classic_address,
            limit_amount=xrpl.utils.amount_to_dict(currency, limit, issuer_wallet.classic_address)
        )
        signed_tx = safe_sign_and_autofill_transaction(trust_set_tx, holder_wallet, client)
        response = send_reliable_submission(signed_tx, client)
        return response

    def __issue_token(issuer_wallet, holder_wallet, currency, amount):
        payment_tx = Payment(
            account=issuer_wallet.classic_address,
            destination=holder_wallet.classic_address,
            amount=xrpl.utils.amount_to_dict(currency, amount, issuer_wallet.classic_address)
        )
        signed_tx = safe_sign_and_autofill_transaction(payment_tx, issuer_wallet, client)
        response = send_reliable_submission(signed_tx, client)
        return response
    
    def __issue_composite_token(issuer_wallet, holder_wallet, comp_amount, utk1_amount, utk2_amount):
        # Check balances of underlying tokens
        account_info = client.request(AccountInfo(
            account=holder_wallet.classic_address,
            ledger_index="validated"
        ))
        balances = {balance['currency']: balance['value'] for balance in account_info.result['account_data']['balance'] if balance['issuer'] == holder_wallet.classic_address}

        if float(balances[UNDERLYING_TOKEN1]) >= utk1_amount and float(balances[UNDERLYING_TOKEN2]) >= utk2_amount:
            # Burn underlying tokens (not supported natively, so we simulate by sending to issuer)
            issue_token(holder_wallet, underlying_issuer1_wallet, UNDERLYING_TOKEN1, str(utk1_amount))
            issue_token(holder_wallet, underlying_issuer2_wallet, UNDERLYING_TOKEN2, str(utk2_amount))
            # Issue composite token
            issue_token(issuer_wallet, holder_wallet, COMPOSITE_TOKEN, str(comp_amount))
            return True
        else:
            return False
    
    def create_flat_coin(self, name: str, underlying_assets: list):

        """
        A underlying asset is a dictionary object containing the following information:
        {
            The underlying token, which can be any asset hold by an issuer
        }
        """
        for underlying_asset in underlying_assets:
            self.__create_trustline(underlying_asset["holder_wallet"],\
                                    underlying_asset["underlying_issuer_wallet"],\
                                        underlying_asset["underlying_token"],\
                                            underlying_asset[""]
                                    )


if __name__ == "__main__":
   
    
    # Generate a wallet for a holder and issuer
    issuer_wallet = genereate_wallet()
    holder_wallet = genereate_wallet()

    stable_coin_creator = CreateStableCoin(
        issuer_wallet=issuer_wallet,
        holder_wallet=holder_wallet,
        amount_of_tokens=1000,
        stable_coin_name="CNX",
        amount_to_issue=10
    )
    stable_coin_creator.create_stable_coin()
