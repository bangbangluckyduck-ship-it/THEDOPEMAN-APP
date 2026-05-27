"""Setup test bots in Supabase for automated E2E testing."""

import os
import sys
from datetime import datetime
from pathlib import Path

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# THEN import Supabase client
from supabase import create_client
import bcrypt

# Initialize Supabase with env vars
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ SUPABASE_URL or SUPABASE_KEY not configured")
    print(f"   SUPABASE_URL: {bool(SUPABASE_URL)}")
    print(f"   SUPABASE_KEY: {bool(SUPABASE_KEY)}")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Bot definitions
BOTS = {
    "FREE": {
        "email": "bot-free@tts-test.com",
        "password": "BotFreePass123!",
        "tier": "free",
        "description": "Free tier - 3 analyses max"
    },
    "PRO": {
        "email": "bot-pro@tts-test.com",
        "password": "BotProPass123!",
        "tier": "pro",
        "description": "Pro tier - Analyses illimitées"
    },
    "GOLD": {
        "email": "bot-gold@tts-test.com",
        "password": "BotGoldPass123!",
        "tier": "gold",
        "description": "Gold tier - Premium complet"
    },
    "BETA": {
        "email": "bot-beta@tts-test.com",
        "password": "BotBetaPass123!",
        "tier": "beta",
        "description": "Beta tier - Features beta"
    },
    "AGENCY": {
        "email": "bot-agency@tts-test.com",
        "password": "BotAgencyPass123!",
        "tier": "agency",
        "description": "Agency tier - Max tier"
    },
    "ADMIN": {
        "email": "bot-admin@tts-test.com",
        "password": "BotAdminPass123!",
        "tier": "admin",
        "description": "Admin tier - All access"
    }
}

def setup_bots():
    """Create or update test bots in Supabase."""
    print("🤖 SETUP TEST BOTS")
    print("=" * 60)
    print()

    results = []

    for bot_type, config in BOTS.items():
        email = config["email"].lower()
        password = config["password"]
        tier = config["tier"]

        try:
            # Check if user exists
            response = supabase.table("users").select("id").eq("email", email).execute()
            
            if response.data:
                # User exists - just update tier
                user_id = response.data[0]["id"]
                supabase.table("users").update({"tier": tier}).eq("id", user_id).execute()
                print(f"✅ {bot_type:10} - Updated (already exists)")
                results.append((bot_type, "updated", email))
            else:
                # Create new user
                password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                new_user = {
                    "email": email,
                    "password": password_hash,
                    "tier": tier,
                }
                supabase.table("users").insert(new_user).execute()
                print(f"✅ {bot_type:10} - Created")
                results.append((bot_type, "created", email))

        except Exception as e:
            print(f"❌ {bot_type:10} - Error: {str(e)[:50]}")
            results.append((bot_type, "error", str(e)))

    print()
    print("=" * 60)
    print("📊 CREDENTIALS")
    print("=" * 60)
    print()
    
    # Print credentials
    for bot_type, config in BOTS.items():
        print(f"{bot_type:10}")
        print(f"  Email:    {config['email']}")
        print(f"  Password: {config['password']}")
        print(f"  Tier:     {config['tier']}")
        print()

    # Save credentials to file
    creds_file = "/tmp/test_bots_credentials.txt"
    with open(creds_file, "w") as f:
        f.write("🤖 TEST BOTS CREDENTIALS\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 70 + "\n\n")
        
        for bot_type, config in BOTS.items():
            f.write(f"{bot_type}\n")
            f.write(f"  Email:    {config['email']}\n")
            f.write(f"  Password: {config['password']}\n")
            f.write(f"  Tier:     {config['tier']}\n")
            f.write(f"  Desc:     {config['description']}\n\n")

    print(f"✅ Credentials saved: {creds_file}")
    print()
    print("=" * 60)
    print("🚀 Ready for testing!")
    return True

if __name__ == "__main__":
    success = setup_bots()
    sys.exit(0 if success else 1)
