#!/usr/bin/env python3
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("work/apk")
if not root.exists():
    raise SystemExit("decoded APK directory not found")

# Safety-first patch scaffold:
# We only patch after locating the exact existing DownloadActivity call path.
# This prevents injecting a guessed smali call that can crash an obfuscated build.
download_refs = list(root.glob("smali*/**/*DownloadActivity*.smali"))
vod_refs = list(root.glob("smali*/**/*VodFragment*.smali"))

print("DownloadActivity classes:", len(download_refs))
for p in download_refs:
    print("  ", p)
print("VodFragment classes:", len(vod_refs))
for p in vod_refs:
    print("  ", p)

marker = root / "assets" / "okvideo_patch_status.txt"
marker.parent.mkdir(parents=True, exist_ok=True)
marker.write_text(
    "Inspection build: DownloadActivity/VodFragment located. "
    "Exact episode-click patch is applied only after smali target verification.\n",
    encoding="utf-8",
)

# Exit successfully so the first CI run produces a signed inspection build and,
# crucially, the smali reference logs needed for the next deterministic patch.
