"""Authentication and authorization endpoints."""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from schemas.token import Token
from schemas.user import UserCreate, UserRead, PasswordChange
from services.user_service import create_user, change_user_password
from utils.dependencies import get_current_user
from utils.jwt import create_access_token, create_refresh_token
from utils.security import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate):
    """Register a new user account."""
    user = await create_user(payload)
    return UserRead(**user.model_dump())


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with username and password to receive access and refresh tokens."""
    user = await User.find_one(User.username == form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username hoặc password không đúng",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Update user status to online
    user.status = "online"
    user.last_online = datetime.now()
    await user.save()
    
    # Generate tokens
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserRead(**user.model_dump())
    )


@router.post("/logout", response_model=UserRead)
async def logout(current_user: User = Depends(get_current_user)):
    """Logout current user and update status to offline."""
    current_user.status = "offline"
    current_user.last_online = datetime.now()
    await current_user.save()
    return UserRead(**current_user.model_dump())


@router.patch("/change-password", response_model=UserRead)
async def change_password(
    payload: PasswordChange,
    current_user: User = Depends(get_current_user)
):
    """Change the current user's password."""
    user = await change_user_password(current_user, payload.old_password, payload.new_password)
    return UserRead(**user.model_dump())
