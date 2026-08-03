# ⚡ Quick Reference - Streaming Analysis v3

**Use this for quick lookups while deploying**

---

## Database Migration (Copy-Paste SQL)

**Location**: Supabase SQL Editor

```sql
-- Run these in order
CREATE TABLE IF NOT EXISTS video_analyses_cache (
    id BIGSERIAL PRIMARY KEY,
    video_url TEXT UNIQUE NOT NULL,
    video_id TEXT NOT NULL,
    analysis_data JSONB NOT NULL,
    product_id TEXT,
    ai_model_used TEXT DEFAULT 'mistral',
    analysis_duration_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    view_count INTEGER DEFAULT 1
);

CREATE INDEX idx_video_url ON video_analyses_cache(video_url);
CREATE INDEX idx_video_id ON video_analyses_cache(video_id);
CREATE INDEX idx_expires_at ON video_analyses_cache(expires_at);

ALTER TABLE video_analyses_cache ENABLE ROW LEVEL SECURITY;

CREATE POLICY "cache_service_role" ON video_analyses_cache
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
```

---

## File Changes Checklist

### ✅ Verify These Files Exist

- [ ] `/cache_manager.py` (5.5 KB)
- [ ] `/static/app_v3.js` (13 KB)
- [ ] `/migration_create_cache_table.sql` (2.8 KB)

### ✅ Verify These Files Are Updated

- [ ] `main.py` - Check line 10: `from cache_manager import ...`
- [ ] `main.py` - Check ~line 450: New `/api/analyze/stream` endpoint
- [ ] `templates/index.html` - Check ~line 1470: `app_v3.js`
- [ ] `templates/index.html` - Check ~line 750: CSS animation styles

---

## Command Reference

### Restart Server
```bash
cd /Users/fr166991/tiktok-analyzer
pkill -f "python3.*main.py"
sleep 2
python3 main.py
```

### Test Endpoint
```bash
curl "http://localhost:8000/api/analyze/stream?video_url=https://www.tiktok.com/@test/video/123" \
  -H "Authorization: Bearer test@example.com"
```

### Clear Browser Cache
- Windows: `Ctrl+Shift+Del`
- Mac: `Cmd+Shift+Delete` or `Cmd+Shift+R` (hard refresh)

### Rollback to v2
```bash
sed -i '' 's/app_v3.js/app_v2.js/g' templates/index.html
pkill -f "python3.*main.py"
python3 main.py
```

---

## Key Functions

### Backend (Python)

```python
# cache_manager.py
from cache_manager import (
    normalize_tiktok_url(url),      # Returns (canonical_url, video_id)
    get_cached_analysis(url),        # Returns analysis_dict or None
    save_to_cache(url, data, ms),   # Saves and returns True/False
    get_cache_stats()                # Returns {total_cached, total_views, ...}
)
```

### Frontend (JavaScript)

```javascript
// app_v3.js
streamAnalysis(videoUrl, product)      // Main function
displayAnalysisSection(name, data)     // Render section
displayAnalysisComplete(ms, source)    // Show completion
switchTab(tabName)                     // Switch tabs
```

---

## Database Queries

### Check Cache Status
```sql
SELECT COUNT(*) FROM video_analyses_cache;
```

### View Cached Videos
```sql
SELECT video_url, view_count FROM video_analyses_cache ORDER BY view_count DESC;
```

### Find Expired Entries
```sql
SELECT video_url FROM video_analyses_cache WHERE expires_at < NOW();
```

### Cache Statistics
```sql
SELECT 
  COUNT(*) as total,
  SUM(view_count) as views,
  ROUND(AVG(view_count)::numeric, 2) as avg
FROM video_analyses_cache;
```

---

## API Endpoints

### Original Endpoint (POST)
```
POST /analyze
Input: frames (JSON), audio (File), product (string)
Output: {hook_type, retention_type, ...}
Time: ~30 seconds
```

### New Endpoint (GET)
```
GET /api/analyze/stream?video_url=<url>&product=<optional>
Output: Server-Sent Events (event: start, section, complete, error)
Time: <1s (cache) or 30s (fresh)
```

---

## Status Indicators

### ✅ Deployment Success
- Server starts without errors
- Browser loads app_v3.js
- Database table exists
- Second submission of same URL is <1s

### ⚠️ Potential Issues
- `module 'cache_manager' not found` → Restart server
- Database table not found → Run SQL migration
- SSE not streaming → Check browser console (F12)

---

## Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Cache lookup | <10ms | ⏳ |
| Cache save | <200ms | ⏳ |
| SSE streaming | 350ms/section | ⏳ |
| Cache hit response | <1s | ⏳ |
| First analysis | ~30s | ✅ |

---

## Backup/Restore

### Backup Cache Data
```sql
-- Export cache table
SELECT json_agg(row_to_json(t)) 
FROM video_analyses_cache t
INTO OUTFILE 'cache_backup.json';
```

### Restore Cache Data
```sql
-- Import cache table
-- (Use your database tool)
```

---

## Monitoring Commands

### Check Server Health
```bash
curl -s http://localhost:8000/ | head -20
```

### Monitor Logs
```bash
tail -f /var/log/tiktok-analyzer.log
```

### Check Database Size
```sql
SELECT 
  pg_size_pretty(pg_total_relation_size('video_analyses_cache'))
AS size;
```

---

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `ImportError: No module named cache_manager` | Restart server |
| `relation "video_analyses_cache" does not exist` | Run SQL migration |
| `SSE stream not showing` | Clear browser cache (Ctrl+Shift+Del) |
| `Cached result still takes 30s` | Check cache table has data |
| `502 Bad Gateway on /api/analyze/stream` | Check server logs |

---

## Test Workflow

1. **Start server**: `python3 main.py`
2. **Open browser**: Navigate to `/app`
3. **First analysis**: Submit video, wait ~30s
4. **Verify cache**: Check DB for new entry
5. **Second analysis**: Submit same URL, should be <1s
6. **Check SSE**: Open DevTools (F12), Network tab, look for stream
7. **Verify sections**: Should see `event: section` multiple times

---

## File Locations

```
/Users/fr166991/tiktok-analyzer/
├── cache_manager.py              ← NEW
├── migration_create_cache_table.sql   ← NEW
├── main.py                       ← MODIFIED
├── templates/index.html          ← MODIFIED
├── static/
│   ├── app_v3.js                ← NEW
│   └── app_v2.js                ← UNCHANGED
└── docs/
    ├── README_STREAMING_V3.md    ← NEW
    ├── DEPLOYMENT_CHECKLIST.md   ← NEW
    ├── MIGRATION_CACHE_SETUP.md  ← NEW
    ├── STREAMING_ANALYSIS_GUIDE.md  ← NEW
    └── QUICK_REFERENCE.md        ← THIS FILE
```

---

## Emergency Procedures

### If Server Crashes
```bash
pkill -f "python3"
sleep 2
python3 main.py
```

### If Cache Gets Corrupted
```sql
-- Delete all cache entries
DELETE FROM video_analyses_cache;

-- System will rebuild cache naturally
```

### If You Need to Rollback
```bash
sed -i '' 's/app_v3.js/app_v2.js/g' templates/index.html
pkill -f "python3.*main.py"
python3 main.py
# System reverts to v2
```

---

## Key Numbers to Remember

| Number | What |
|--------|------|
| 30 | Seconds for fresh analysis |
| 1 | Second for cache hit |
| 10 | Number of sections streamed |
| 350 | Milliseconds per section delay |
| 30/60/90 | Cache TTL days (default/popular/viral) |

---

## Next Steps

1. ✅ Read this file
2. → Open DEPLOYMENT_CHECKLIST.md
3. → Follow Phase 1-4
4. → Verify with tests
5. → Done! 🎉

---

*Quick reference complete. Ready to deploy!*
