import logging
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_db
from app.repositories.commodity_coin_repository import CommodityCoinRepository
from app.schemas.common.object_created import ObjectCreatedSchema
from app.schemas.flat_coin_schema import CommodityCoinSchema
from app.services.xrpl_client_wrapper import XrplClientWrapper


class CommodityCoinService:
    def __init__(
        self,
        commodity_coin_repository: CommodityCoinRepository,
        xrpl_client_wrapper: XrplClientWrapper,
    ) -> None:
        self.__commodity_coin_repository = commodity_coin_repository
        self.__xrpl_client_wrapper = xrpl_client_wrapper

    async def get_commodity_coins(
        self, name: str | None
    ) -> Sequence[CommodityCoinSchema]:
        commodity_coin_models = await self.__commodity_coin_repository.find_all(
            name=name
        )
        return [
            CommodityCoinSchema(
                id=commodity_coin_model.id,
                name=commodity_coin_model.name,
                address=commodity_coin_model.address,
                description=commodity_coin_model.description,
            )
            for commodity_coin_model in commodity_coin_models
        ]

    async def create_commodity_coin(
        self, name: str, description: str, amount_of_tokens: int, amount_to_issue: int
    ) -> ObjectCreatedSchema:
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
        commodity_coin_model = await self.__commodity_coin_repository.create(
            name=name,
            # TODO: Replace with real coin address
            address=stablecoin_address,
            description=description,
            issuer_wallet_public_key=issuer_wallet.public_key,
            issuer_wallet_private_key=issuer_wallet.private_key,
            holder_wallet_public_key=holder_wallet.public_key,
            holder_wallet_private_key=holder_wallet.private_key,
        )
        print("commodity_coin_model.id", commodity_coin_model.id)
        return ObjectCreatedSchema(id=str(commodity_coin_model.id))


async def build_commodity_coin_service(
    session: Annotated[AsyncSession, Depends(get_async_db)]
) -> CommodityCoinService:
    commodity_coin_repository = CommodityCoinRepository(session=session)
    xrpl_client_wrapper = XrplClientWrapper()
    return CommodityCoinService(
        commodity_coin_repository=commodity_coin_repository,
        xrpl_client_wrapper=xrpl_client_wrapper,
    )
