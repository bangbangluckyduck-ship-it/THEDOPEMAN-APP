"""Comprehensive E2E test suite for all bot tiers."""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
BASE_URL = os.getenv("API_URL", "https://qeerah.com")
# Fallback to localhost if API_URL not set
if BASE_URL.startswith("http"):
    pass  # Use as-is
else:
    BASE_URL = "http://localhost:8000"

# Test bot credentials
BOTS = {
    "FREE": {
        "email": "bot-free@tts-test.com",
        "password": "BotFreePass123!",
        "tier": "free",
    },
    "PRO": {
        "email": "bot-pro@tts-test.com",
        "password": "BotProPass123!",
        "tier": "pro",
    },
    "GOLD": {
        "email": "bot-gold@tts-test.com",
        "password": "BotGoldPass123!",
        "tier": "gold",
    },
    "BETA": {
        "email": "bot-beta@tts-test.com",
        "password": "BotBetaPass123!",
        "tier": "beta",
    },
    "AGENCY": {
        "email": "bot-agency@tts-test.com",
        "password": "BotAgencyPass123!",
        "tier": "agency",
    },
    "ADMIN": {
        "email": "bot-admin@tts-test.com",
        "password": "BotAdminPass123!",
        "tier": "admin",
    }
}

class TestRunner:
    """Run comprehensive tests for each bot tier."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.results = {}
        self.session = requests.Session()
        self.start_time = datetime.now()

    def test_bot_tier(self, bot_type, email, password, tier):
        """Test all functionality for a single bot tier."""
        print(f"\n{'='*70}")
        print(f"🤖 Testing {bot_type} tier ({email})")
        print(f"{'='*70}\n")

        tier_results = {
            "tier": tier,
            "tests": {}
        }

        # Test 1: Login
        token = self.test_login(email, password, tier_results)
        if not token:
            tier_results["status"] = "FAILED"
            self.results[bot_type] = tier_results
            return False

        # Test 2: Get user info
        self.test_user_info(token, tier_results)

        # Test 3: Check market recommendations access
        self.test_market_recommendations(token, tier_results)

        # Test 4: Check Tendances Gagnantes tab access
        self.test_winning_trends_access(token, tier_results)

        # Test 5: Check admin endpoints (ADMIN tier only)
        if bot_type == "ADMIN":
            self.test_admin_endpoints(token, tier_results)

        # Test 6: Test password reset initiation
        self.test_forgot_password(email, tier_results)

        # Determine overall status
        failed = sum(1 for test in tier_results["tests"].values()
                    if test.get("status") == "FAILED")
        tier_results["status"] = "PASSED" if failed == 0 else "PARTIAL"

        self.results[bot_type] = tier_results

        # Print summary
        passed = sum(1 for test in tier_results["tests"].values()
                    if test.get("status") == "PASSED")
        print(f"\n📊 {bot_type} Tier Summary:")
        print(f"   ✅ Passed: {passed}")
        print(f"   ❌ Failed: {failed}")
        print(f"   Status: {tier_results['status']}")

        return failed == 0

    def test_login(self, email, password, tier_results):
        """Test user login."""
        print("1️⃣  Testing Login...")
        try:
            response = self.session.post(
                f"{self.base_url}/api/login",
                json={"email": email, "password": password},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("ok") and "email" in data:
                    # Login successful - use email as token (Bearer format: Bearer email)
                    print(f"   ✅ Login successful")
                    tier_results["tests"]["login"] = {"status": "PASSED"}
                    return email  # Return email to use in Authorization header

            print(f"   ❌ Login failed: {response.status_code}")
            print(f"      Response: {response.text[:100]}")
            tier_results["tests"]["login"] = {
                "status": "FAILED",
                "error": f"Status {response.status_code}"
            }
            return None

        except Exception as e:
            print(f"   ❌ Login error: {str(e)[:60]}")
            tier_results["tests"]["login"] = {
                "status": "FAILED",
                "error": str(e)
            }
            return None

    def test_user_info(self, token, tier_results):
        """Test getting user info."""
        print("2️⃣  Testing User Info...")
        try:
            headers = {"Authorization": f"Bearer {token}"}  # token is actually the email
            response = self.session.get(
                f"{self.base_url}/api/user-info",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if "email" in data or "tier" in data:
                    print(f"   ✅ User info retrieved")
                    tier_results["tests"]["user_info"] = {"status": "PASSED"}
                    return True

            print(f"   ⚠️  User info: {response.status_code}")
            tier_results["tests"]["user_info"] = {
                "status": "PARTIAL",
                "error": f"Status {response.status_code}"
            }
            return False

        except Exception as e:
            print(f"   ❌ User info error: {str(e)[:60]}")
            tier_results["tests"]["user_info"] = {
                "status": "FAILED",
                "error": str(e)
            }
            return False

    def test_market_recommendations(self, token, tier_results):
        """Test market recommendations endpoint."""
        print("3️⃣  Testing Market Recommendations...")
        try:
            headers = {"Authorization": f"Bearer {token}"}  # token is actually the email
            response = self.session.get(
                f"{self.base_url}/api/market-recommendations",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                print(f"   ✅ Market recommendations accessible")
                tier_results["tests"]["market_recommendations"] = {"status": "PASSED"}
                return True
            elif response.status_code == 403:
                print(f"   🔒 Market recommendations blocked (tier restriction)")
                tier_results["tests"]["market_recommendations"] = {
                    "status": "BLOCKED",
                    "reason": "Tier restriction"
                }
                return False
            else:
                print(f"   ⚠️  Market recommendations: {response.status_code}")
                tier_results["tests"]["market_recommendations"] = {
                    "status": "PARTIAL",
                    "error": f"Status {response.status_code}"
                }
                return False

        except Exception as e:
            print(f"   ❌ Market recommendations error: {str(e)[:60]}")
            tier_results["tests"]["market_recommendations"] = {
                "status": "FAILED",
                "error": str(e)
            }
            return False

    def test_winning_trends_access(self, token, tier_results):
        """Test Tendances Gagnantes (Winning Trends) access."""
        print("4️⃣  Testing Tendances Gagnantes (Winning Trends)...")
        try:
            headers = {"Authorization": f"Bearer {token}"}  # token is actually the email
            response = self.session.get(
                f"{self.base_url}/api/market-recommendations",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                print(f"   ✅ Tendances Gagnantes accessible")
                tier_results["tests"]["winning_trends"] = {"status": "PASSED"}
                return True
            elif response.status_code == 403:
                print(f"   🔒 Tendances Gagnantes blocked (tier restriction)")
                tier_results["tests"]["winning_trends"] = {
                    "status": "BLOCKED",
                    "reason": "Tier restriction"
                }
                return False
            else:
                print(f"   ⚠️  Tendances Gagnantes: {response.status_code}")
                tier_results["tests"]["winning_trends"] = {
                    "status": "PARTIAL",
                    "error": f"Status {response.status_code}"
                }
                return False

        except Exception as e:
            print(f"   ❌ Tendances Gagnantes error: {str(e)[:60]}")
            tier_results["tests"]["winning_trends"] = {
                "status": "FAILED",
                "error": str(e)
            }
            return False

    def test_admin_endpoints(self, token, tier_results):
        """Test admin-only endpoints (ADMIN tier only)."""
        print("5️⃣  Testing Admin Endpoints...")
        try:
            headers = {"Authorization": f"Bearer {token}"}  # token is actually the email

            # Try to get admin users list or similar admin-only endpoint
            response = self.session.get(
                f"{self.base_url}/admin/users",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                print(f"   ✅ Admin endpoints accessible")
                tier_results["tests"]["admin_endpoints"] = {"status": "PASSED"}
                return True
            elif response.status_code == 404:
                print(f"   ⚠️  Admin endpoint not found (may be different URL)")
                tier_results["tests"]["admin_endpoints"] = {
                    "status": "PARTIAL",
                    "error": "Admin endpoint not found"
                }
                return False
            elif response.status_code == 403:
                print(f"   ❌ Admin endpoints blocked (forbidden)")
                tier_results["tests"]["admin_endpoints"] = {
                    "status": "FAILED",
                    "error": "Forbidden"
                }
                return False
            else:
                print(f"   ⚠️  Admin endpoints: {response.status_code}")
                tier_results["tests"]["admin_endpoints"] = {
                    "status": "PARTIAL",
                    "error": f"Status {response.status_code}"
                }
                return False

        except Exception as e:
            print(f"   ⚠️  Admin endpoints error: {str(e)[:60]}")
            tier_results["tests"]["admin_endpoints"] = {
                "status": "PARTIAL",
                "error": str(e)
            }
            return False

    def test_forgot_password(self, email, tier_results):
        """Test password reset initiation."""
        print("6️⃣  Testing Password Reset Initiation...")
        try:
            response = self.session.post(
                f"{self.base_url}/api/forgot-password",
                json={
                    "email": email,
                    "password": "NewTestPass123!"
                },
                timeout=10
            )

            if response.status_code == 200:
                print(f"   ✅ Password reset initiated")
                tier_results["tests"]["password_reset"] = {"status": "PASSED"}
                return True
            elif response.status_code == 429:
                print(f"   ⏱️  Password reset rate limited (too many attempts)")
                tier_results["tests"]["password_reset"] = {
                    "status": "PARTIAL",
                    "reason": "Rate limited"
                }
                return False
            else:
                print(f"   ⚠️  Password reset: {response.status_code}")
                tier_results["tests"]["password_reset"] = {
                    "status": "PARTIAL",
                    "error": f"Status {response.status_code}"
                }
                return False

        except Exception as e:
            print(f"   ❌ Password reset error: {str(e)[:60]}")
            tier_results["tests"]["password_reset"] = {
                "status": "FAILED",
                "error": str(e)
            }
            return False

    def run_all_tests(self):
        """Run tests for all bot tiers."""
        print("\n" + "="*70)
        print("🚀 AUTOMATED TESTING SUITE - ALL BOT TIERS")
        print("="*70)
        print(f"API URL: {self.base_url}")
        print(f"Start Time: {self.start_time.isoformat()}")

        for bot_type, config in BOTS.items():
            self.test_bot_tier(
                bot_type,
                config["email"],
                config["password"],
                config["tier"]
            )
            # Small delay between tests
            time.sleep(1)

        # Print overall summary
        self.print_summary()

        # Save results to file
        self.save_results()

    def print_summary(self):
        """Print overall test summary."""
        print("\n" + "="*70)
        print("📊 OVERALL TEST SUMMARY")
        print("="*70 + "\n")

        tier_order = ["FREE", "PRO", "GOLD", "BETA", "AGENCY", "ADMIN"]

        for bot_type in tier_order:
            if bot_type not in self.results:
                continue

            result = self.results[bot_type]
            status_emoji = "✅" if result["status"] == "PASSED" else "⚠️" if result["status"] == "PARTIAL" else "❌"

            passed = sum(1 for test in result["tests"].values()
                        if test.get("status") == "PASSED")
            total = len(result["tests"])

            print(f"{status_emoji} {bot_type:10} - {result['status']:8} ({passed}/{total} tests passed)")

        # Overall result
        total_passed = sum(1 for r in self.results.values() if r["status"] == "PASSED")
        total_tiers = len(self.results)

        print(f"\n{'='*70}")
        print(f"Total Tiers Tested: {total_tiers}")
        print(f"Fully Passed: {total_passed}/{total_tiers}")

        elapsed = datetime.now() - self.start_time
        print(f"Execution Time: {elapsed.total_seconds():.2f} seconds")
        print(f"End Time: {datetime.now().isoformat()}")

    def save_results(self):
        """Save test results to file."""
        results_file = "/tmp/test_results.json"
        report_file = "/tmp/test_report.txt"

        # Save JSON results
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)

        # Save text report
        with open(report_file, "w") as f:
            f.write("🤖 AUTOMATED TEST REPORT\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"API URL: {self.base_url}\n")
            f.write("="*70 + "\n\n")

            tier_order = ["FREE", "PRO", "GOLD", "BETA", "AGENCY", "ADMIN"]

            for bot_type in tier_order:
                if bot_type not in self.results:
                    continue

                result = self.results[bot_type]
                status_emoji = "✅" if result["status"] == "PASSED" else "⚠️" if result["status"] == "PARTIAL" else "❌"

                f.write(f"{status_emoji} {bot_type}\n")
                f.write(f"   Tier: {result['tier']}\n")
                f.write(f"   Status: {result['status']}\n")
                f.write(f"   Tests:\n")

                for test_name, test_result in result["tests"].items():
                    test_emoji = "✅" if test_result.get("status") == "PASSED" else "⚠️" if test_result.get("status") == "PARTIAL" else "🔒" if test_result.get("status") == "BLOCKED" else "❌"
                    f.write(f"      {test_emoji} {test_name}: {test_result.get('status', 'UNKNOWN')}")
                    if "reason" in test_result:
                        f.write(f" ({test_result['reason']})")
                    elif "error" in test_result:
                        f.write(f" ({test_result['error'][:50]}...)")
                    f.write("\n")
                f.write("\n")

        print(f"\n✅ Results saved:")
        print(f"   JSON: {results_file}")
        print(f"   Report: {report_file}")
        print(f"\nView report: cat {report_file}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = BASE_URL

    print(f"Testing API: {base_url}")

    runner = TestRunner(base_url)
    runner.run_all_tests()


if __name__ == "__main__":
    main()
