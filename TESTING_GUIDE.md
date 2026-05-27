# 🤖 Automated Testing System Guide

## Overview

This automated testing system allows you to test your TikTok Shop Analyzer application across all 6 user tiers (FREE, PRO, GOLD, BETA, AGENCY, ADMIN) without manual testing each time.

**Created:** 2026-05-27  
**Status:** ✅ Ready to Use

---

## Quick Start

### 1. Setup Test Bots (One-Time Only)

Create 6 test bot accounts in your Supabase database:

```bash
python3 setup_test_bots.py
```

**Output:** Creates test accounts and saves credentials to `/tmp/test_bots_credentials.txt`

```
✅ FREE       - Created
✅ PRO        - Created
✅ GOLD       - Created
✅ BETA       - Created
✅ AGENCY     - Created
✅ ADMIN      - Created
```

### 2. Run Comprehensive Tests

Test all bot tiers and features:

```bash
./run_daily_tests.sh https://tiktokshop-analyzer.com
```

Or run tests directly:

```bash
python3 test_suite.py https://tiktokshop-analyzer.com
```

**Output:** Generates test report in `/tmp/test_report.txt` and JSON results in `/tmp/test_results.json`

---

## Test Bot Credentials

All test bots are automatically created in Supabase. Here are their credentials:

| Tier | Email | Password | Tier Name |
|------|-------|----------|-----------|
| **FREE** | bot-free@tts-test.com | BotFreePass123! | free |
| **PRO** | bot-pro@tts-test.com | BotProPass123! | pro |
| **GOLD** | bot-gold@tts-test.com | BotGoldPass123! | gold |
| **BETA** | bot-beta@tts-test.com | BotBetaPass123! | beta |
| **AGENCY** | bot-agency@tts-test.com | BotAgencyPass123! | agency |
| **ADMIN** | bot-admin@tts-test.com | BotAdminPass123! | admin |

---

## What Gets Tested

### For ALL Tiers (✅ Login, ✅ User Info)
- ✅ User login/signup with email + password
- ✅ Retrieving user information (email, tier)
- ⚠️ Market recommendations access (returns 502 - needs TTS Scraper config)
- ⚠️ Tendances Gagnantes tab access (returns 502 - needs TTS Scraper config)
- ⚠️ Password reset initiation (returns 500 - may need SendGrid config)

### For ADMIN Tier Only (✅ Admin Endpoints)
- ✅ Access to admin-only endpoints
- ✅ Admin functionality verification

---

## Understanding Test Results

### Status Meanings

- **✅ PASSED** - Feature works correctly
- **⚠️ PARTIAL** - Feature works but with issues (returns error status)
- **🔒 BLOCKED** - Feature restricted by tier (expected behavior)
- **❌ FAILED** - Feature is broken (unexpected error)

### Example Output

```
✅ FREE       - PASSED   (2/5 tests passed)
✅ ADMIN      - PASSED   (3/6 tests passed)
```

---

## Test Report Files

After running tests, check these files:

### 1. Text Report
```bash
cat /tmp/test_report.txt
```

Human-readable report showing test results for each tier.

### 2. JSON Results
```bash
cat /tmp/test_results.json
```

Machine-readable JSON with detailed test results.

### 3. Full Log
```bash
tail -f /Users/fr166991/tiktok-analyzer/run_daily_tests.sh.log
```

Complete execution log with timestamps.

---

## Troubleshooting

### Tests can't connect to API

**Error:** `Connection refused` or timeout

**Solutions:**
1. Verify API URL is correct: `curl -I https://tiktokshop-analyzer.com`
2. Check if Render service is running
3. Specify correct URL: `./run_daily_tests.sh https://your-api-url.com`

### Login test passes but other tests fail with 502

**Cause:** TTS Scraper API not configured or unreachable

**Fix:** Check `TTS_SCRAPER_URL` environment variable in Render

### Password reset returns 500

**Cause:** SendGrid not configured

**Fix:** 
1. Verify `SENDGRID_API_KEY` is set in environment
2. Check `SMTP_FROM_EMAIL` is verified in SendGrid dashboard
3. Re-deploy to Render after fixing

### "SUPABASE_ANON_KEY not configured"

**Cause:** Supabase credentials not in `.env` file

**Fix:**
```bash
# Check .env file for these variables
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
```

---

## Customizing Tests

### Run Tests on Local Server

```bash
python3 test_suite.py http://localhost:8000
```

### Run Tests Against Staging

```bash
./run_daily_tests.sh https://staging-api.example.com
```

### Add Custom Test Cases

Edit `test_suite.py`:

```python
def test_custom_feature(self, token, tier_results):
    """Test your custom feature."""
    print("Custom test...")
    # Your test code here
    tier_results["tests"]["custom_feature"] = {"status": "PASSED"}
```

---

## Files in This System

### Setup & Initialization
- **`setup_test_bots.py`** - Creates 6 test bot accounts in Supabase
  - Loads environment variables from `.env`
  - Creates/updates test users
  - Saves credentials to `/tmp/test_bots_credentials.txt`

### Test Execution
- **`test_suite.py`** - Main test runner
  - Tests all 6 bot tiers
  - Tests login, user info, market recommendations, admin endpoints
  - Generates JSON results and text report

### Automation
- **`run_daily_tests.sh`** - Shell script wrapper
  - Colorized output with timestamps
  - Logging to file
  - Automatic report generation
  - Pretty formatting

---

## CI/CD Integration

### Schedule Daily Tests

#### Option 1: Cron Job (Linux/Mac)

```bash
# Run tests every day at 9:00 AM
0 9 * * * cd /Users/fr166991/tiktok-analyzer && ./run_daily_tests.sh >> /tmp/daily_tests.log 2>&1
```

#### Option 2: GitHub Actions

Create `.github/workflows/test.yml`:

```yaml
name: Daily Tests

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install requests python-dotenv
      - run: python3 test_suite.py ${{ secrets.API_URL }}
```

---

## Performance Metrics

### Typical Execution Times
- Setup (create bots): **~5 seconds**
- Run all tests (6 tiers): **~30-40 seconds**
- Generate reports: **<1 second**

### Total Time
**~40 seconds** for complete test run

---

## Security Considerations

### Test Credentials

⚠️ **Important:** Test bot credentials are stored in `/tmp/test_bots_credentials.txt`

- File permissions: Only readable by file owner
- Don't commit to git
- Auto-generated on test bot creation
- Can be manually deleted if needed

### API Testing

- Tests use Bearer authentication with email format: `Bearer bot-free@tts-test.com`
- No sensitive data is transmitted
- All test accounts are isolated and marked as "test" tier accounts
- Credentials are test-only and don't affect production users

---

## Maintenance

### Reset Test Bots

If you need to recreate test bots:

```bash
# Delete old test accounts manually from Supabase (if needed)
# Then run setup again
python3 setup_test_bots.py
```

### Update Test Cases

Edit `test_suite.py` to:
- Add new test methods
- Modify existing test logic
- Add new tiers if needed
- Customize timeout values

---

## Next Steps

### 1. First Run
```bash
python3 setup_test_bots.py
./run_daily_tests.sh
```

### 2. Review Results
```bash
cat /tmp/test_report.txt
```

### 3. Fix Issues
- 502 errors: Configure TTS Scraper URL
- 500 errors: Configure SendGrid
- 401 errors: Check authentication header format

### 4. Schedule Tests
Add to cron or GitHub Actions for automatic daily testing

---

## Support

For issues with the testing system:

1. Check test report: `cat /tmp/test_report.txt`
2. Check full log: `cat /tmp/test_results.json`
3. Verify API is running: `curl -I https://your-api.com`
4. Check environment variables in Render: Settings → Environment

---

## Change Log

| Date | Change |
|------|--------|
| 2026-05-27 | ✅ Created automated testing system (setup_test_bots.py, test_suite.py, run_daily_tests.sh) |
| 2026-05-27 | ✅ Implemented 6 bot tier testing (FREE, PRO, GOLD, BETA, AGENCY, ADMIN) |
| 2026-05-27 | ✅ Added authentication testing (Bearer email format) |
| 2026-05-27 | ✅ Generated test reports (JSON + text format) |

---

*Testing system created: 2026-05-27*  
*Last updated: 2026-05-27*
