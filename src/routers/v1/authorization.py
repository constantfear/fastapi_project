from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from icecream import ic
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.configurations.token import create_access_token, decode_token
from src.models.seller import Seller
from src.schemas import LoginSeller, Token, TokenData

token_router = APIRouter(tags=["token"], prefix="/token")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@token_router.post("/", response_model=Token)
async def login_for_access_token(form_data: LoginSeller, session: DBSession) -> Token:
    query = select(Seller).filter(Seller.email == form_data.email)
    res = await session.execute(query)
    seller = res.scalar()
    if not seller or seller.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=10)
    access_token = create_access_token(
        data={"seller_email": seller.email, "seller_id": seller.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: DBSession):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("seller_email")
        seller_id: int = payload.get("seller_id")
        ic(seller_id)
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username, id=seller_id)
    except JWTError:
        raise credentials_exception
    query = select(Seller).filter(Seller.email == token_data.email)
    res = await session.execute(query)
    seller = res.scalar()
    if seller is None:
        raise credentials_exception
    return seller
