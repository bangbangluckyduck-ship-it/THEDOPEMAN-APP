"""Password reset utilities for secure token generation and validation."""

import os
import secrets
import string
import bcrypt
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Tuple
from supabase_client import supabase

PASSWORD_RESET_TOKEN_EXPIRE_HOURS = int(os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_HOURS", "24"))
TEMPORARY_PASSWORD_LENGTH = int(os.getenv("TEMPORARY_PASSWORD_LENGTH", "12"))


def generate_reset_token() -> str:
    """Generate a secure reset token (~32 characters, URL-safe)."""
    return secrets.token_urlsafe(24)


def generate_temporary_password(length: int = TEMPORARY_PASSWORD_LENGTH) -> str:
    """Generate a random temporary password with mix of upper/lower/digits/symbols."""
    # Use mix of characters for security
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    # Ensure at least one of each type
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*"),
    ]
    # Fill the rest randomly
    for _ in range(length - 4):
        password.append(secrets.choice(chars))
    # Shuffle to avoid predictable pattern
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def hash_token(token: str) -> str:
    """Hash a token using bcrypt (never store plaintext tokens)."""
    return bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()


def verify_token(token: str, token_hash: str) -> bool:
    """Verify if a token matches its hash."""
    try:
        return bcrypt.checkpw(token.encode(), token_hash.encode())
    except Exception:
        return False


def create_password_reset_token(
    email: str,
    token_type: str,  # 'temporary_password' or 'magic_link'
    new_password_hash: Optional[str] = None,
) -> Tuple[bool, str, Optional[str]]:
    """
    Create a password reset token in Supabase.

    Returns:
        (success, token_plaintext, token_hash)
    """
    if not supabase:
        return False, "", None

    try:
        reset_token = generate_reset_token()
        token_hash = hash_token(reset_token)
        expires_at = (
            datetime.now(timezone.utc) + timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
        ).isoformat()

        reset_data = {
            "email": email,
            "reset_token": token_hash,
            "token_type": token_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": expires_at,
            "used": False,
        }

        if token_type == "temporary_password" and new_password_hash:
            reset_data["new_password"] = new_password_hash

        # Insert token into Supabase
        response = supabase.table("password_reset_tokens").insert(reset_data).execute()

        if response and response.data:
            return True, reset_token, token_hash
        else:
            return False, "", None

    except Exception as e:
        print(f"Error creating password reset token: {str(e)}")
        return False, "", None


def validate_reset_token(token: str, email: str) -> Tuple[bool, Optional[Dict]]:
    """
    Validate a reset token: check existence, expiration, and validity.

    Returns:
        (is_valid, token_data)
    """
    if not supabase or not token or not email:
        return False, None

    try:
        # Get all tokens for this email (not used, ordered by creation)
        response = supabase.table("password_reset_tokens").select("*").eq("email", email).eq("used", False).order("created_at", desc=True).limit(1).execute()

        if not response or not response.data:
            return False, None

        token_data = response.data[0]
        stored_hash = token_data.get("reset_token", "")

        # Verify token matches hash
        if not verify_token(token, stored_hash):
            return False, None

        # Check expiration
        expires_at = token_data.get("expires_at")
        if expires_at:
            expiry_time = datetime.fromisoformat(expires_at)
            if datetime.now(timezone.utc) > expiry_time:
                return False, token_data  # Expired but token exists

        return True, token_data

    except Exception as e:
        print(f"Error validating reset token: {str(e)}")
        return False, None


def mark_token_as_used(email: str, token: str) -> bool:
    """Mark a reset token as used after successful password change."""
    if not supabase:
        return False

    try:
        # Get the token record
        response = supabase.table("password_reset_tokens").select("*").eq("email", email).eq("used", False).order("created_at", desc=True).limit(1).execute()

        if response and response.data:
            token_id = response.data[0].get("id")
            # Mark as used
            supabase.table("password_reset_tokens").update({"used": True}).eq("id", token_id).execute()
            return True

    except Exception as e:
        print(f"Error marking token as used: {str(e)}")

    return False


def get_reset_token_info(email: str) -> Optional[Dict]:
    """Get info about latest reset token for an email."""
    if not supabase:
        return None

    try:
        response = (
            supabase.table("password_reset_tokens")
            .select("*")
            .eq("email", email)
            .eq("used", False)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        if response and response.data:
            return response.data[0]

    except Exception as e:
        print(f"Error getting reset token info: {str(e)}")

    return None


def check_rate_limit(email: str, max_attempts: int = 5, window_hours: int = 1) -> bool:
    """
    Check if user has exceeded rate limit for password reset requests.

    Returns:
        True if within limit (request allowed), False if limit exceeded
    """
    if not supabase:
        return True  # Allow if DB not available

    try:
        cutoff_time = (datetime.now(timezone.utc) - timedelta(hours=window_hours)).isoformat()

        response = (
            supabase.table("password_reset_tokens")
            .select("id", count="exact")
            .eq("email", email)
            .gt("created_at", cutoff_time)
            .execute()
        )

        if response and hasattr(response, "count"):
            return response.count < max_attempts

    except Exception as e:
        print(f"Error checking rate limit: {str(e)}")
        return True  # Allow if check fails

    return True
