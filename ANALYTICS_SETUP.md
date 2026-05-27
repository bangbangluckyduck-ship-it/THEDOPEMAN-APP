# 📊 Analytics Setup Guide

## Quick Start

The analytics system tracks visitor count per day in real-time.

### Step 1: Create Supabase Tables (5 minutes)

1. Go to your Supabase dashboard
2. Open **SQL Editor**
3. Click **New Query**
4. Copy the content from `analytics_setup.sql`
5. Click **RUN**

You should see 3 tables created:
- `daily_visitor_stats` - Daily visitor count
- `visitor_logs` - Individual visit logs
- `analytics_config` - Configuration settings

### Step 2: Set Environment Variable

Add this to your `.env` file:

```bash
ANALYTICS_PASSWORD=your_admin_password_here
```

(Default is `admin123` if not set)

### Step 3: Deploy Code

The analytics code is already integrated in `main.py`:
- Routes: `/api/analytics`, `/api/analytics/today`
- Visitor tracking on homepage and app page
- Analysis counting in `/analyze` endpoint

### Step 4: Access Dashboard

Once deployed to Render:
1. Go to `https://your-domain.com/analytics`
2. Enter your admin password
3. View real-time visitor stats!

---

## How It Works

### Automatic Tracking
- Every visit to `/` (homepage) is logged
- Every visit to `/app` is logged
- Every analysis in `/analyze` increments counter

### API Endpoints

**Get 30-day stats:**
```bash
curl "https://your-domain.com/api/analytics?password=admin123"
```

**Get today's count:**
```bash
curl "https://your-domain.com/api/analytics/today?password=admin123"
```

### Dashboard Features
- ✅ Total visitors (last 30 days)
- ✅ Visitors today (real-time)
- ✅ Average per day
- ✅ Line chart visualization
- ✅ Daily breakdown table
- ✅ Auto-refresh every 5 minutes

---

## Customization

### Change Password
Update `ANALYTICS_PASSWORD` in `.env`

### Change Tracking
Edit `track_visitor()` function in `main.py` to track more/fewer pages

### Change Retention
Update `daily_visitor_stats` table RLS policies to retain longer

---

## Troubleshooting

**Q: Dashboard shows "Analytics not available"**
A: Make sure Supabase tables are created (run analytics_setup.sql)

**Q: Password is incorrect but I'm sure it's right**
A: Check your `.env` file - it must have `ANALYTICS_PASSWORD=`

**Q: Visitor count isn't updating**
A: Check Supabase network tab - make sure the insert is working

---

## Footer Fix

The footer is now sticky on all pages!

**What changed:**
- `#app-footer` now has `position: fixed`
- `main` has `padding-bottom: 140px` to avoid overlap
- Footer stays visible on mobile too

---

**That's it! Analytics + sticky footer are ready to go.** 🎉
