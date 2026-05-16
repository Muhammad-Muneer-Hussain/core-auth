import jwt
from datetime import datetime, timezone
from typing import Annotated 
from fastapi.security import OAuth2PasswordRequestForm 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, oauth2_scheme
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, StandardResponse
from app.schemas.token import Token, TokenRefresh
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token
)
from app.core.config import settings
from app.redis.client import is_token_blacklisted, add_token_to_blacklist

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user_in.email)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user



@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: AsyncSession = Depends(get_db)
):
    
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id)
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(token_in: TokenRefresh, db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token"
    )
    
    try:
        payload = jwt.decode(token_in.refresh_token, settings.REFRESH_SECRET, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        exp = payload.get("exp")
        
        if user_id is None or token_type != "refresh":
            raise credentials_exception
            
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    if await is_token_blacklisted(token_in.refresh_token):
        raise credentials_exception
        
    stmt = select(User).where(User.id == int(user_id))
    result = await db.execute(stmt)
    if not result.scalar_one_or_none():
        raise credentials_exception
        
    # Rotate tokens: Blacklist old refresh token to prevent reuse (Optional but good practice)
    now = datetime.now(timezone.utc).timestamp()
    ttl = int(exp - now)
    if ttl > 0:
        await add_token_to_blacklist(token_in.refresh_token, ttl)
        
    return Token(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id)
    )

@router.post("/logout", response_model=StandardResponse)
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.ACCESS_SECRET, algorithms=[settings.ALGORITHM])
        exp = payload.get("exp")
        now = datetime.now(timezone.utc).timestamp()
        ttl = int(exp - now)
        if ttl > 0:
            await add_token_to_blacklist(token, ttl)
    except jwt.InvalidTokenError:
        pass # If token is already invalid, we just ignore
        
    return StandardResponse(detail="Revocation complete")
