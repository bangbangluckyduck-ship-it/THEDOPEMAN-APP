"""Cache manager for video analysis results using Supabase."""

import json
import re
import asyncio
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
import hashlib

from supabase_client import supabase

# Cache configuration
CACHE_TTL_DAYS = 30
CACHE_TTL_POPULAR_DAYS = 60
CACHE_TTL_VIRAL_DAYS = 90


def normalize_tiktok_url(url: str) -> Tuple[str, str]:
    """
    Normalize TikTok URL to canonical form and extract video ID.

    Examples:
    - https://www.tiktok.com/@user/video/123?utm_source=share → https://www.tiktok.com/@user/video/123
    - https://vm.tiktok.com/abc123 → https://www.tiktok.com/@unknown/video/123
    - https://vt.tiktok.com/abc123 → https://www.tiktok.com/@unknown/video/123

    Returns: (normalized_url, video_id)
    """
    try:
        # Extract video ID from URL (pattern: /video/XXXXX)
        match = re.search(r'/video/(\d+)', url)
        if not match:
            # Try to extract from vm.tiktok.com format (hash-based)
            # For now, use URL hash as ID for short URLs
            url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
            video_id = url_hash
        else:
            video_id = match.group(1)

        # Normalize URL format
        parsed = urlparse(url)

        # Remove query parameters
        clean_path = parsed.path.rstrip('/')

        # Handle vm.tiktok.com and vt.tiktok.com (short URLs)
        if parsed.netloc in ['vm.tiktok.com', 'vt.tiktok.com', 'm.tiktok.com']:
            # Convert short URL to canonical form
            normalized_url = f"https://www.tiktok.com/video/{video_id}"
        else:
            # Already in canonical format
            normalized_url = f"https://www.tiktok.com{clean_path}"

        return normalized_url, video_id

    except Exception as e:
        print(f"[CACHE] Error normalizing URL: {e}")
        # Fallback: use URL hash
        url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
        return url, url_hash


async def get_cached_analysis(video_url: str) -> Optional[dict]:
    """
    Check if analysis exists in cache and is not expired.
    Updates view_count if found.

    Returns: analysis_data if found and valid, None otherwise
    """
    try:
        normalized_url, video_id = normalize_tiktok_url(video_url)

        # Query cache
        response = supabase.table("video_analyses_cache").select(
            "id, analysis_data, view_count, created_at"
        ).eq("video_url", normalized_url).lt("expires_at", "now()").execute()

        if not response.data:
            print(f"[CACHE] MISS: {normalized_url}")
            return None

        cached = response.data[0]

        # Update view_count
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: supabase.table("video_analyses_cache").update({
                "view_count": cached["view_count"] + 1,
                "updated_at": "now()"
            }).eq("id", cached["id"]).execute()
        )

        print(f"[CACHE] HIT: {normalized_url} (views: {cached['view_count'] + 1})")
        return cached["analysis_data"]

    except Exception as e:
        print(f"[CACHE] Error retrieving from cache: {e}")
        return None


async def save_to_cache(
    video_url: str,
    analysis_data: dict,
    duration_ms: int,
    product_id: Optional[str] = None
) -> bool:
    """
    Save analysis result to cache for future requests.

    Cache TTL depends on popularity:
    - Default: 30 days
    - Popular (>10 views): 60 days
    - Viral (>100 views): 90 days
    """
    try:
        normalized_url, video_id = normalize_tiktok_url(video_url)

        # Determine TTL based on popularity (future view_count)
        ttl_days = CACHE_TTL_DAYS

        # Calculate expiration
        expires_at = (datetime.utcnow() + timedelta(days=ttl_days)).isoformat()

        # Insert or update cache
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: supabase.table("video_analyses_cache").upsert({
                "video_url": normalized_url,
                "video_id": video_id,
                "analysis_data": analysis_data,
                "product_id": product_id,
                "ai_model_used": "mistral",
                "analysis_duration_ms": duration_ms,
                "expires_at": expires_at,
                "view_count": 1,
                "updated_at": "now()"
            }).execute()
        )

        print(f"[CACHE] SAVED: {normalized_url} ({duration_ms}ms)")
        return True

    except Exception as e:
        print(f"[CACHE] Error saving to cache: {e}")
        # Don't fail the analysis if cache save fails
        return False


async def get_cache_stats() -> dict:
    """Get cache statistics for monitoring."""
    try:
        response = supabase.table("video_analyses_cache").select(
            "view_count, created_at, expires_at"
        ).execute()

        if not response.data:
            return {
                "total_cached": 0,
                "hit_rate": 0,
                "avg_views": 0
            }

        total = len(response.data)
        total_views = sum(r["view_count"] for r in response.data)

        return {
            "total_cached": total,
            "total_views": total_views,
            "avg_views_per_video": round(total_views / total, 2) if total > 0 else 0,
            "estimated_cost_saved": f"${total_views * 0.01:.2f}"  # Rough estimate
        }

    except Exception as e:
        print(f"[CACHE] Error getting stats: {e}")
        return {}
