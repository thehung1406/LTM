"""JWT token creation and validation utilities."""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from jose import jwt, JWTError

from core.config import settings


def create_access_token(subject: str) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: Subject (usually user_id) to encode in the token
        
    Returns:
        Encoded JWT access token string
    """
    expire_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.now(tz=timezone.utc)
    
    to_encode = {
        "sub": str(subject),
        "type": "access",
        "exp": now + expire_delta,
        "iat": now,
    }
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: str) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        subject: Subject (usually user_id) to encode in the token
        
    Returns:
        Encoded JWT refresh token string
    """
    expire_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    now = datetime.now(tz=timezone.utc)
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "type": "refresh",
        "exp": now + expire_delta,
        "iat": now,
    }
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Decoded token payload as dictionary
        
    Raises:
        ValueError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as exc:
        raise ValueError("Invalid token") from exc