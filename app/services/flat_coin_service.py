import logging
from typing import Annotated, Sequence
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from xrpl.wallet import Wallet

from app.core.db import get_async_db
from app.repositories.commodity_coin_repository import CommodityCoinRepository
from app.repositories.flat_coin_repository import FlatCoinRepository
from app.schemas.common.object_created import ObjectCreatedSchema
from app.schemas.flat_coin_schema import FlatCoinSchema
from app.services.xrpl_client_wrapper import StableCoinToCompose, XrplClientWrapper


class FlatCoinService:
    def __init__(
        self,
        flat_coin_repository: FlatCoinRepository,
        commodity_coin_repository: CommodityCoinRepository,
        xrpl_client_wrapper: XrplClientWrapper,
    ) -> None:
        self.__flat_coin_repository = flat_coin_repository
        self.__xrpl_client_wrapper = xrpl_client_wrapper
        self.__commodity_coin_repository = commodity_coin_repository

    async def get_flat_coins(self, name: str | None) -> Sequence[FlatCoinSchema]:
        flat_coin_models = await self.__flat_coin_repository.find_all(name=name)
        return [
            FlatCoinSchema(
                id=flat_coin_model.id,
                name=flat_coin_model.name,
                address=flat_coin_model.address,
                description=flat_coin_model.description,
                # TODO: replace with real commodity_coins
                commodity_coins=[],
            )
            for flat_coin_model in flat_coin_models
        ]

    async def create_flat_coin(
        self,
        name: str,
        description: str,
        amount_of_tokens: int,
        amount_to_issue: int,
        commodities_amount: list[float],
        commodities_ids: list[UUID],
    ) -> ObjectCreatedSchema:
        commodity_coin_models = await self.__commodity_coin_repository.find_by_ids(
            ids=commodities_ids
        )

        issuer_wallet = await self.__xrpl_client_wrapper.create_wallet()
        holder_wallet = await self.__xrpl_client_wrapper.create_wallet()

        logging.info(f"Issuer Wallet: {issuer_wallet.classic_address}")
        logging.info(f"Holder Wallet: {holder_wallet.classic_address}")

        # Create stablecoin
        stablecoin_address = await self.__xrpl_client_wrapper.create_stable_coin(
            issuer_wallet,
            holder_wallet,
            name,
            amount_of_tokens,
            amount_to_issue,
        )

        logging.info("Collateralizing flat coin")

        await self.__xrpl_client_wrapper.collateralize_composite_token(
            issuer_wallet=issuer_wallet,
            utks=[
                StableCoinToCompose(
                    issuer_wallet=Wallet(
                        public_key=commodity_coin_model.issuer_wallet_public_key,
                        private_key=commodity_coin_model.issuer_wallet_private_key,
                    ),
                    holder_wallet=Wallet(
                        public_key=commodity_coin_model.holder_wallet_public_key,
                        private_key=commodity_coin_model.holder_wallet_private_key,
                    ),
                    # TODO: Change later
                    amount=commodities_amount[0],
                    name=commodity_coin_model.name,
                )
                for commodity_coin_model in commodity_coin_models
            ],
        )

        # TODO: Encrypt Private Keys
        flat_coin_model = await self.__flat_coin_repository.create(
            name=name,
            # TODO: Replace with real coin address
            address=stablecoin_address,
            description=description,
            issuer_wallet_public_key=issuer_wallet.public_key,
            issuer_wallet_private_key=issuer_wallet.private_key,
            holder_wallet_public_key=holder_wallet.public_key,
            holder_wallet_private_key=holder_wallet.private_key,
        )
        logging.info(f"Created flat_coin_model with id:{flat_coin_model.id}")

        return ObjectCreatedSchema(id=str(flat_coin_model.id))

    async def flat_coin_faucet(
        self, flat_coin_id: UUID, flat_coin_amount: float, destination_address: str
    ) -> None:
        flat_coin_model = await self.__flat_coin_repository.find_by_id(id=flat_coin_id)

        if flat_coin_model is None:
            raise Exception("Flat coin not found")
        
        logging.info("Found flat_coin_model, sending...")

        await self.__xrpl_client_wrapper.send_stable_coin(
            issuer_wallet=Wallet(
                public_key=flat_coin_model.issuer_wallet_public_key,
                private_key=flat_coin_model.issuer_wallet_private_key,
            ),
            holder_wallet=Wallet(
                public_key=flat_coin_model.holder_wallet_public_key,
                private_key=flat_coin_model.holder_wallet_private_key,
            ),
            stable_coin_name=flat_coin_model.name,
            amount=flat_coin_amount,
            receiver_wallet_classic_address=destination_address,
        )


async def build_flat_coin_service(
    session: Annotated[AsyncSession, Depends(get_async_db)]
) -> FlatCoinService:
    flat_coin_repository = FlatCoinRepository(session=session)
    commodity_coin_repository = CommodityCoinRepository(session=session)
    xrpl_client_wrapper = XrplClientWrapper()
    return FlatCoinService(
        flat_coin_repository=flat_coin_repository,
        commodity_coin_repository=commodity_coin_repository,
        xrpl_client_wrapper=xrpl_client_wrapper,
    )
