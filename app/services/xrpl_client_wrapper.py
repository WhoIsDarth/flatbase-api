import logging
from typing import NamedTuple, Optional

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.transaction import submit_and_wait
from xrpl.asyncio.wallet import generate_faucet_wallet
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests import AccountInfo
from xrpl.models.transactions import AccountSet, Payment, TrustSet
from xrpl.wallet import Wallet

from app.config import settings


class StableCoinToCompose(NamedTuple):
    name: str
    issuer_wallet: Wallet
    holder_wallet: Wallet
    amount: float


class XrplClientWrapper:
    def __init__(
        self,
        network: str = settings.XRP_NETWORK,
        main_wallet_public_key: Optional[str] = settings.XRP_WALLET_PUBLIC_KEY,
        main_wallet_private_key: Optional[str] = settings.XRP_WALLET_PRIVATE_KEY,
    ):
        self.__client = AsyncJsonRpcClient(network)
        self.__main_wallet = Wallet(
            public_key=main_wallet_public_key, private_key=main_wallet_private_key
        )

    async def create_wallet(self) -> Wallet:
        # Create and fund a new wallet using the XRPL Testnet Faucet
        # TODO: When we move from development remove faucet_wallet generation
        wallet = await generate_faucet_wallet(self.__client)
        return wallet

    async def fund_wallet(self, destination_wallet: Wallet, amount: str) -> None:
        if not self.__main_wallet:
            raise ValueError("Main wallet is not set.")

        payment_tx = Payment(
            account=self.__main_wallet.classic_address,
            destination=destination_wallet.classic_address,
            amount=amount,  # Amount in drops (1 XRP = 1,000,000 drops)
        )
        response = await submit_and_wait(payment_tx, self.__client, self.__main_wallet)
        logging.info(
            f"Funding response for {destination_wallet.classic_address}: {response}"
        )

    async def create_stable_coin(
        self,
        issuer_wallet: Wallet,
        holder_wallet: Wallet,
        stable_coin_name: str,
        amount_of_tokens: float,
        amount_to_issue: float,
    ) -> str:
        # Fund issuer and holder wallets
        # TODO: Calculate funding amount later
        # await self.fund_wallet(issuer_wallet, "1000000")  # Fund with 10 XRP
        # await self.fund_wallet(holder_wallet, "1000000")  # Fund with 10 XRP

        # Set default Ripple flag to allow token issuing
        account_set_tx = self.__set_ripple(issuer_wallet)
        response = await submit_and_wait(account_set_tx, self.__client, issuer_wallet)
        logging.info(f"AccountSet response: {response}")

        # Create a trust line from the holder to the issuer for the stablecoin
        trust_set_tx = self.__create_trustline(
            holder_wallet, issuer_wallet, stable_coin_name, amount_of_tokens
        )
        response = await submit_and_wait(trust_set_tx, self.__client, holder_wallet)
        logging.info(f"TrustSet response: {response}")

        # Issue some amount of the stable coin from the issuer to the holder
        payment_tx = self.__issue_stable_coin(
            issuer_wallet,
            issuer_wallet,
            holder_wallet,
            stable_coin_name,
            amount_to_issue,
        )
        response = await submit_and_wait(payment_tx, self.__client, issuer_wallet)
        logging.info(f"Payment response: {response}")

        # Validate the account info
        # TODO: Check that coin really exists
        await self.__validate(holder_wallet)

        # Return the stablecoin address
        stablecoin_address = f"{issuer_wallet.classic_address}.{stable_coin_name}"
        return stablecoin_address

    async def collateralize_composite_token(
        self,
        issuer_wallet: Wallet,
        utks: list[StableCoinToCompose],
    ) -> str:
        for utk in utks:
            # Create trustline
            trust_set_tx = self.__create_trustline(
                issuer_wallet, utk.issuer_wallet, utk.name, utk.amount
            )
            response = await submit_and_wait(trust_set_tx, self.__client, issuer_wallet)
            logging.info(f"TrustSet response for {utk.name}: {response}")

            # Send underlying tokens back to issuer (burn)
            burn_tx = self.__issue_stable_coin(
                sender_wallet=utk.holder_wallet,
                issuer_wallet=utk.issuer_wallet,
                holder_wallet=issuer_wallet,
                stable_coin_name=utk.name,
                amount_to_issue=utk.amount,
            )
            logging.info(f"Collateralize transaction: {burn_tx}")
            try:
                response = await submit_and_wait(
                    burn_tx, self.__client, utk.holder_wallet
                )
                logging.info(
                    f"Burn response for {utk.issuer_wallet.classic_address}: {response}"
                )
            except Exception as e:
                logging.error(f"Error burning token {utk.name}: {e}")
                raise

        return True

    async def send_stable_coin(
        self,
        receiver_wallet_classic_address: str,
        issuer_wallet: Wallet,
        holder_wallet: Wallet,
        stable_coin_name: str,
        amount: float,
    ) -> None:
        payment_tx = Payment(
            account=holder_wallet.classic_address,
            destination=receiver_wallet_classic_address,
            amount=IssuedCurrencyAmount(
                currency=stable_coin_name,
                value=str(amount),
                issuer=issuer_wallet.classic_address,
            ),
        )
        logging.info(f"Payment transaction: {payment_tx}")
        await submit_and_wait(payment_tx, self.__client, holder_wallet)

    def __set_ripple(self, issuer_wallet: Wallet) -> AccountSet:
        return AccountSet(
            account=issuer_wallet.classic_address,
            set_flag=8,
        )

    def __create_trustline(
        self,
        holder_wallet: Wallet,
        issuer_wallet: Wallet,
        stable_coin_name: str,
        amount_of_tokens: float,
    ) -> TrustSet:
        return TrustSet(
            account=holder_wallet.classic_address,
            limit_amount={
                "currency": stable_coin_name,
                "value": str(amount_of_tokens),
                "issuer": issuer_wallet.classic_address,
            },
        )

    def __issue_stable_coin(
        self,
        sender_wallet: Wallet,
        issuer_wallet: Wallet,
        holder_wallet: Wallet,
        stable_coin_name: str,
        amount_to_issue: float,
    ) -> Payment:
        return Payment(
            account=sender_wallet.classic_address,
            destination=holder_wallet.classic_address,
            amount=IssuedCurrencyAmount(
                currency=stable_coin_name,
                value=str(amount_to_issue),
                issuer=issuer_wallet.classic_address,
            ),
        )

    async def __validate(self, wallet: Wallet) -> None:
        account_info = AccountInfo(
            account=wallet.classic_address, ledger_index="validated"
        )
        response = await self.__client.request(account_info)
        logging.info(f"Validation response: {response}")
