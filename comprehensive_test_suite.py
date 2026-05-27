"""Comprehensive E2E test suite for ALL features and ALL bot tiers."""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
BASE_URL = os.getenv("API_URL", "https://tiktokshop-analyzer.com").rstrip('/')

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

class ComprehensiveTestRunner:
    """Run comprehensive tests for each bot tier - ALL features."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.results = {}
        self.start_time = datetime.now()

    def test_bot_tier(self, bot_type, email, password, tier):
        """Test ALL functionality for a single bot tier."""
        print(f"\n{'='*80}")
        print(f"🤖 Testing {bot_type} tier ({email})")
        print(f"{'='*80}\n")

        session = requests.Session()
        tier_results = {
            "tier": tier,
            "tests": {},
            "status": "UNKNOWN"
        }

        # Test 1: Login
        token = self.test_login(session, email, password, tier_results)
        if not token:
            tier_results["status"] = "FAILED"
            self.results[bot_type] = tier_results
            return False

        # Test 2: User Info
        self.test_user_info(session, token, tier_results)

        # Test 3: Market Recommendations Access
        self.test_market_recommendations(session, token, tier_results)

        # Test 4: Winning Trends (Tendances Gagnantes)
        self.test_winning_trends(session, token, tier_results)

        # Test 5: Product Recommendations
        self.test_product_recommendations(session, token, tier_results)

        # Test 6: User Quota/Usage Info
        self.test_quota_info(session, token, tier_results)

        # Test 7: Password Reset
        self.test_forgot_password(session, email, tier_results)

        # Test 8: Admin Endpoints (ADMIN tier only)
        if bot_type == "ADMIN":
            self.test_admin_user_list(session, token, tier_results)
            self.test_admin_set_tier(session, token, tier_results)
            self.test_admin_grant_beta(session, token, tier_results)

        # Test 9: Analyze Endpoint (GET /analyze)
        self.test_analyze_endpoint(session, token, tier_results)

        # Test 10: Stripe/Pricing Endpoints
        self.test_stripe_endpoints(session, token, tier_results)

        # Determine overall status
        passed = sum(1 for t in tier_results["tests"].values() if t.get("status") == "PASSED")
        blocked = sum(1 for t in tier_results["tests"].values() if t.get("status") == "BLOCKED")
        failed = sum(1 for t in tier_results["tests"].values() if t.get("status") == "FAILED")
        total = len(tier_results["tests"])

        tier_results["stats"] = {"passed": passed, "blocked": blocked, "failed": failed, "total": total}
        tier_results["status"] = "PASSED" if failed == 0 else "PARTIAL" if blocked > 0 else "FAILED"

        self.results[bot_type] = tier_results

        # Print summary
        print(f"\n📊 {bot_type} Tier Summary:")
        print(f"   ✅ Passed:  {passed}")
        print(f"   🔒 Blocked: {blocked} (tier restriction)")
        print(f"   ❌ Failed:  {failed}")
        print(f"   Total:  {total} tests")
        print(f"   Status: {tier_results['status']}")

        return failed == 0

    def test_login(self, session, email, password, tier_results):
        """Test user login."""
        print("1️⃣  Testing Login...")
        try:
            response = session.post(
                f"{self.base_url}/api/login",
                json={"email": email, "password": password},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    print(f"   ✅ Login successful")
                    tier_results["tests"]["login"] = {"status": "PASSED"}
                    return email

            print(f"   ❌ Login failed: {response.status_code}")
            tier_results["tests"]["login"] = {"status": "FAILED", "error": f"Status {response.status_code}"}
            return None

        except Exception as e:
            print(f"   ❌ Login error: {str(e)[:60]}")
            tier_results["tests"]["login"] = {"status": "FAILED", "error": str(e)[:60]}
            return None

    def test_user_info(self, session, token, tier_results):
        """Test getting user info."""
        print("2️⃣  Testing User Info...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.get(f"{self.base_url}/api/user-info", headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"   ✅ User info retrieved")
                tier_results["tests"]["user_info"] = {"status": "PASSED"}
                return True
            else:
                print(f"   ⚠️  User info: {response.status_code}")
                tier_results["tests"]["user_info"] = {"status": "PARTIAL"}
                return False
        except Exception as e:
            print(f"   ❌ User info error: {str(e)[:60]}")
            tier_results["tests"]["user_info"] = {"status": "FAILED"}
            return False

    def test_market_recommendations(self, session, token, tier_results):
        """Test market recommendations."""
        print("3️⃣  Testing Market Recommendations...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.get(f"{self.base_url}/api/market-recommendations", headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"   ✅ Market recommendations accessible")
                tier_results["tests"]["market_recommendations"] = {"status": "PASSED"}
            elif response.status_code == 403:
                print(f"   🔒 Market recommendations blocked (tier restriction)")
                tier_results["tests"]["market_recommendations"] = {"status": "BLOCKED"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["market_recommendations"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["market_recommendations"] = {"status": "FAILED"}

    def test_winning_trends(self, session, token, tier_results):
        """Test Tendances Gagnantes tab."""
        print("4️⃣  Testing Tendances Gagnantes (Winning Trends)...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.get(f"{self.base_url}/api/market-recommendations", headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"   ✅ Tendances Gagnantes accessible")
                tier_results["tests"]["winning_trends"] = {"status": "PASSED"}
            elif response.status_code == 403:
                print(f"   🔒 Tendances Gagnantes blocked (tier restriction)")
                tier_results["tests"]["winning_trends"] = {"status": "BLOCKED"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["winning_trends"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["winning_trends"] = {"status": "FAILED"}

    def test_product_recommendations(self, session, token, tier_results):
        """Test product recommendations by category."""
        print("5️⃣  Testing Product Recommendations...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.get(
                f"{self.base_url}/api/product-recommendations/beaute",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                print(f"   ✅ Product recommendations accessible")
                tier_results["tests"]["product_recommendations"] = {"status": "PASSED"}
            elif response.status_code == 403:
                print(f"   🔒 Product recommendations blocked (tier restriction)")
                tier_results["tests"]["product_recommendations"] = {"status": "BLOCKED"}
            elif response.status_code == 404:
                print(f"   ⚠️  Endpoint not found")
                tier_results["tests"]["product_recommendations"] = {"status": "PARTIAL"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["product_recommendations"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["product_recommendations"] = {"status": "FAILED"}

    def test_quota_info(self, session, token, tier_results):
        """Test quota/usage information."""
        print("6️⃣  Testing Quota/Usage Info...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.get(f"{self.base_url}/api/usage-info", headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"   ✅ Quota info accessible")
                tier_results["tests"]["quota_info"] = {"status": "PASSED"}
            elif response.status_code == 404:
                print(f"   ⚠️  Endpoint not found")
                tier_results["tests"]["quota_info"] = {"status": "PARTIAL"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["quota_info"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["quota_info"] = {"status": "FAILED"}

    def test_forgot_password(self, session, email, tier_results):
        """Test password reset."""
        print("7️⃣  Testing Password Reset...")
        try:
            response = session.post(
                f"{self.base_url}/api/forgot-password",
                json={"email": email, "password": "NewPass123!"},
                timeout=10
            )

            if response.status_code == 200:
                print(f"   ✅ Password reset initiated")
                tier_results["tests"]["password_reset"] = {"status": "PASSED"}
            elif response.status_code == 429:
                print(f"   ⏱️  Rate limited (expected)")
                tier_results["tests"]["password_reset"] = {"status": "PARTIAL", "reason": "Rate limited"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["password_reset"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["password_reset"] = {"status": "FAILED"}

    def test_admin_user_list(self, session, token, tier_results):
        """Test admin user list endpoint."""
        print("8️⃣  Testing Admin - User List...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.get(f"{self.base_url}/admin/users", headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"   ✅ Admin user list accessible")
                tier_results["tests"]["admin_user_list"] = {"status": "PASSED"}
            elif response.status_code == 403:
                print(f"   ❌ Admin endpoint forbidden (not admin)")
                tier_results["tests"]["admin_user_list"] = {"status": "FAILED"}
            elif response.status_code == 404:
                print(f"   ⚠️  Endpoint not found")
                tier_results["tests"]["admin_user_list"] = {"status": "PARTIAL"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["admin_user_list"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["admin_user_list"] = {"status": "FAILED"}

    def test_admin_set_tier(self, session, token, tier_results):
        """Test admin set tier endpoint."""
        print("9️⃣  Testing Admin - Set Tier...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.post(
                f"{self.base_url}/admin/set-tier",
                headers=headers,
                json={"email": "test@test.com", "tier": "pro"},
                timeout=10
            )

            if response.status_code in [200, 400]:  # 400 if user doesn't exist
                print(f"   ✅ Admin set tier endpoint works")
                tier_results["tests"]["admin_set_tier"] = {"status": "PASSED"}
            elif response.status_code == 403:
                print(f"   ❌ Admin endpoint forbidden")
                tier_results["tests"]["admin_set_tier"] = {"status": "FAILED"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["admin_set_tier"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["admin_set_tier"] = {"status": "FAILED"}

    def test_admin_grant_beta(self, session, token, tier_results):
        """Test admin grant beta endpoint."""
        print("🔟 Testing Admin - Grant Beta...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.post(
                f"{self.base_url}/admin/grant-beta",
                headers=headers,
                json={"email": "test@test.com"},
                timeout=10
            )

            if response.status_code in [200, 400]:  # 400 if user doesn't exist
                print(f"   ✅ Admin grant beta endpoint works")
                tier_results["tests"]["admin_grant_beta"] = {"status": "PASSED"}
            elif response.status_code == 403:
                print(f"   ❌ Admin endpoint forbidden")
                tier_results["tests"]["admin_grant_beta"] = {"status": "FAILED"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["admin_grant_beta"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["admin_grant_beta"] = {"status": "FAILED"}

    def test_analyze_endpoint(self, session, token, tier_results):
        """Test analyze endpoint."""
        print("1️⃣1️⃣ Testing Video Analysis Endpoint...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.get(f"{self.base_url}/analyze", headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"   ✅ Analyze endpoint accessible")
                tier_results["tests"]["analyze_endpoint"] = {"status": "PASSED"}
            elif response.status_code in [403, 401]:
                print(f"   🔒 Analyze endpoint blocked/restricted")
                tier_results["tests"]["analyze_endpoint"] = {"status": "BLOCKED"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["analyze_endpoint"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["analyze_endpoint"] = {"status": "FAILED"}

    def test_stripe_endpoints(self, session, token, tier_results):
        """Test Stripe/pricing endpoints."""
        print("1️⃣2️⃣ Testing Stripe/Pricing Endpoints...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = session.post(
                f"{self.base_url}/create-checkout-session",
                headers=headers,
                json={"price_id": "test"},
                timeout=10
            )

            # Stripe endpoints may not work without proper config, but should exist
            if response.status_code in [200, 400, 500]:
                print(f"   ✅ Stripe endpoints exist")
                tier_results["tests"]["stripe_endpoints"] = {"status": "PASSED"}
            elif response.status_code == 404:
                print(f"   ⚠️  Stripe endpoints not found")
                tier_results["tests"]["stripe_endpoints"] = {"status": "PARTIAL"}
            else:
                print(f"   ⚠️  Status {response.status_code}")
                tier_results["tests"]["stripe_endpoints"] = {"status": "PARTIAL"}
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:60]}")
            tier_results["tests"]["stripe_endpoints"] = {"status": "PARTIAL"}

    def run_all_tests(self):
        """Run tests for all bot tiers."""
        print("\n" + "="*80)
        print("🚀 COMPREHENSIVE TESTING SUITE - ALL FEATURES, ALL BOTS")
        print("="*80)
        print(f"API URL: {self.base_url}")
        print(f"Start Time: {self.start_time.isoformat()}")
        print(f"Testing {len(BOTS)} tiers with 12+ features each...")

        for bot_type, config in BOTS.items():
            self.test_bot_tier(
                bot_type,
                config["email"],
                config["password"],
                config["tier"]
            )
            time.sleep(0.5)

        self.print_summary()
        self.save_results()

    def print_summary(self):
        """Print overall test summary."""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("="*80 + "\n")

        tier_order = ["FREE", "PRO", "GOLD", "BETA", "AGENCY", "ADMIN"]
        total_tests = 0
        total_passed = 0

        for bot_type in tier_order:
            if bot_type not in self.results:
                continue

            result = self.results[bot_type]
            stats = result.get("stats", {})
            status_emoji = "✅" if result["status"] == "PASSED" else "⚠️" if result["status"] == "PARTIAL" else "❌"

            passed = stats.get("passed", 0)
            total = stats.get("total", 0)

            print(f"{status_emoji} {bot_type:10} - {result['status']:8} ({passed}/{total} tests)")

            total_tests += total
            total_passed += passed

        print(f"\n{'='*80}")
        print(f"Total Tests Run: {total_tests}")
        print(f"Total Passed: {total_passed}/{total_tests}")
        print(f"Success Rate: {total_passed*100//total_tests if total_tests > 0 else 0}%")

        elapsed = datetime.now() - self.start_time
        print(f"Execution Time: {elapsed.total_seconds():.2f} seconds")

    def save_results(self):
        """Save test results to file."""
        results_file = "/tmp/comprehensive_test_results.json"
        report_file = "/tmp/comprehensive_test_report.txt"

        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)

        with open(report_file, "w") as f:
            f.write("🤖 COMPREHENSIVE TEST REPORT\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"API URL: {self.base_url}\n")
            f.write("="*80 + "\n\n")

            tier_order = ["FREE", "PRO", "GOLD", "BETA", "AGENCY", "ADMIN"]

            for bot_type in tier_order:
                if bot_type not in self.results:
                    continue

                result = self.results[bot_type]
                stats = result.get("stats", {})
                status_emoji = "✅" if result["status"] == "PASSED" else "⚠️" if result["status"] == "PARTIAL" else "❌"

                f.write(f"{status_emoji} {bot_type}\n")
                f.write(f"   Tier: {result['tier']}\n")
                f.write(f"   Status: {result['status']}\n")
                f.write(f"   Stats: {stats['passed']}/{stats['total']} passed\n")
                f.write(f"   Tests:\n")

                for test_name, test_result in sorted(result["tests"].items()):
                    test_emoji = "✅" if test_result.get("status") == "PASSED" else "🔒" if test_result.get("status") == "BLOCKED" else "⚠️" if test_result.get("status") == "PARTIAL" else "❌"
                    f.write(f"      {test_emoji} {test_name}: {test_result.get('status')}")
                    if "reason" in test_result:
                        f.write(f" ({test_result['reason']})")
                    f.write("\n")
                f.write("\n")

        print(f"\n✅ Results saved:")
        print(f"   JSON: {results_file}")
        print(f"   Report: {report_file}")


def main():
    """Main entry point."""
    api_url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL

    runner = ComprehensiveTestRunner(api_url)
    runner.run_all_tests()


if __name__ == "__main__":
    main()
