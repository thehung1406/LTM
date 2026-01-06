"""Password hashing and user authentication utilities."""
from passlib.context import CryptContext
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str) -> User | None:
    """
    Authenticate a user by username and password.
    
    Args:
        username: Username to authenticate
        password: Password to verify
        
    Returns:
        User object if authentication successful, None otherwise
    """
    user = await User.find_one({"username": username})
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user
