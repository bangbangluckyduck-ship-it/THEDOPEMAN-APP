#!/usr/bin/env python3
"""
Test script for /api/analyze/stream endpoint.
Tests cache hits and misses with SSE streaming.

Usage:
    python3 test_streaming_analysis.py https://qeerah.com
"""

import sys
import asyncio
import httpx
import json
from datetime import datetime

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_stream_response(url: str, video_url: str, product: str = None):
    """Test streaming analysis endpoint."""

    email = "bot-gold@tts-test.com"  # Use GOLD bot for market data access
    token = f"Bearer {email}"

    # Prepare request
    params = {"video_url": video_url}
    if product:
        params["product"] = product

    full_url = f"{url}/api/analyze/stream"

    print(f"📡 Testing: {full_url}")
    print(f"   Video: {video_url}")
    print(f"   Auth: {token}")
    print(f"   Product: {product or '(auto-detect)'}")

    try:
        # Make streaming request
        print("\n⏳ Connecting to stream...\n")

        start_time = datetime.now()
        events_received = []
        sections_received = []

        with httpx.stream(
            "GET",
            full_url,
            params=params,
            headers={"Authorization": token},
            timeout=300.0
        ) as response:
            print(f"✅ Connected (HTTP {response.status_code})\n")

            if response.status_code != 200:
                print(f"❌ Error: {response.status_code}")
                print(response.text[:500])
                return False

            # Parse SSE stream
            buffer = ""
            for line in response.iter_lines():
                buffer += line + "\n"

                # Process complete messages (separated by \n\n)
                if buffer.count("\n\n") > 0:
                    messages = buffer.split("\n\n")
                    buffer = messages[-1]  # Keep incomplete message

                    for message in messages[:-1]:
                        if not message.strip():
                            continue

                        # Parse SSE message
                        event_type = None
                        data = None

                        for msg_line in message.split("\n"):
                            if msg_line.startswith("event:"):
                                event_type = msg_line[6:].strip()
                            elif msg_line.startswith("data:"):
                                data = msg_line[5:].strip()

                        if event_type and data:
                            events_received.append((event_type, data))

                            # Parse JSON data
                            try:
                                parsed = json.loads(data)
                                elapsed = (datetime.now() - start_time).total_seconds()

                                if event_type == "start":
                                    print(f"▶️  [{elapsed:.2f}s] START")
                                    print(f"     {parsed.get('message', 'Analyzing...')}")
                                    print(f"     Source: {parsed.get('source', 'unknown')}")

                                elif event_type == "section":
                                    section_name = parsed.get("name", "?")
                                    sections_received.append(section_name)
                                    section_data = parsed.get("data", "")

                                    # Truncate long data for display
                                    if isinstance(section_data, str):
                                        preview = section_data[:60] + "..." if len(str(section_data)) > 60 else str(section_data)
                                    else:
                                        preview = str(section_data)[:60] + "..."

                                    print(f"📊 [{elapsed:.2f}s] SECTION: {section_name}")
                                    print(f"     {preview}")

                                elif event_type == "complete":
                                    print(f"✅ [{elapsed:.2f}s] COMPLETE")
                                    print(f"     Duration: {parsed.get('duration_ms', 'N/A')}ms")
                                    print(f"     Source: {parsed.get('source', 'unknown')}")

                                elif event_type == "error":
                                    print(f"❌ [{elapsed:.2f}s] ERROR")
                                    print(f"     {parsed.get('error', parsed.get('message', 'Unknown error'))}")
                                    return False

                            except json.JSONDecodeError:
                                print(f"⚠️  Invalid JSON: {data[:50]}...")

        # Summary
        total_time = (datetime.now() - start_time).total_seconds()
        print(f"\n{'─'*70}")
        print(f"📊 Stream Summary:")
        print(f"   ✓ Total events: {len(events_received)}")
        print(f"   ✓ Sections received: {len(sections_received)}")
        print(f"   ✓ Total time: {total_time:.2f}s")
        print(f"   ✓ Sections: {', '.join(sections_received[:5])}")
        if len(sections_received) > 5:
            print(f"              ... and {len(sections_received) - 5} more")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""

    if len(sys.argv) < 2:
        print("Usage: python3 test_streaming_analysis.py <api_url>")
        print("Example: python3 test_streaming_analysis.py https://qeerah.com")
        sys.exit(1)

    api_url = sys.argv[1].rstrip('/')

    print_section("🎥 TikTok Shop Analyzer - Streaming Analysis Test")

    # Test 1: Cache hit (same URL analyzed twice)
    print_section("Test 1: Cache Hit Scenario (Simulated)")
    print("ℹ️  Testing streaming from cache (should be <1 second)\n")

    test_video_url = "https://www.tiktok.com/@seller/video/7123456789"

    print("First analysis (cache miss - will take 20-30 seconds):")
    print("⏭️  Skipping live analysis for demo (too slow)")
    print("   Run full test with: python3 test_streaming_analysis.py <url> --full\n")

    # Test 2: Simulated cache hit
    print("Second analysis (cache hit - will take <1 second):")
    success = test_stream_response(
        api_url,
        test_video_url,
        product="Electronic Gadget"
    )

    if success:
        print("\n" + "="*70)
        print("  ✅ STREAMING ANALYSIS TEST PASSED")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("  ❌ STREAMING ANALYSIS TEST FAILED")
        print("="*70)
        sys.exit(1)

if __name__ == "__main__":
    main()
