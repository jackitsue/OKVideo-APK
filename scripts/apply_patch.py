#!/usr/bin/env python3
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("work/apk")
if not root.exists():
    raise SystemExit("decoded APK directory not found")

smali = root / "smali_classes3"
base = smali / "com/fongmi/android/tv"
iface = base / "ui/adapter/EpisodeAdapter$oOoOoOoOoOoOoO0o.smali"
episode_fragment = base / "ui/fragment/EpisodeFragment.smali"
video_activity = base / "ui/activity/VideoActivity.smali"
side_dialog = smali / "oOoO0Oo0oOoO0OoO/OoOo0o0oOo0O0O0o.smali"
holders = [
    base / "ui/holder/EpisodeGridHolder.smali",
    base / "ui/holder/EpisodeHoriHolder.smali",
    base / "ui/holder/EpisodeVertHolder.smali",
]
listener = base / "ui/holder/EpisodeLongClickListener.smali"

required = [iface, episode_fragment, video_activity, side_dialog, *holders]
missing = [str(p) for p in required if not p.exists()]
if missing:
    raise SystemExit("Missing expected smali files:\n" + "\n".join(missing))

def read(path):
    return path.read_text(encoding="utf-8")

def write(path, value):
    path.write_text(value, encoding="utf-8")

# Extend the existing episode callback with a dedicated long-press download action.
s = read(iface)
sig = ".method public abstract onDownload(Lcom/fongmi/android/tv/bean/Episode;)V"
if sig not in s:
    s = s.rstrip() + "\n\n" + sig + "\n.end method\n"
    write(iface, s)

# EpisodeFragment already owns SiteViewModel. Its existing normal click switches
# between play/download based on a Bundle flag; long press should always download.
s = read(episode_fragment)
if ".method public onDownload(Lcom/fongmi/android/tv/bean/Episode;)V" not in s:
    s = s.rstrip() + r"""

.method public onDownload(Lcom/fongmi/android/tv/bean/Episode;)V
    .locals 1

    iget-object v0, p0, Lcom/fongmi/android/tv/ui/fragment/EpisodeFragment;->oOoOo0O0Oo0o0OoO:Lcom/fongmi/android/tv/model/SiteViewModel;

    invoke-virtual {v0, p1}, Lcom/fongmi/android/tv/model/SiteViewModel;->OoO0oOoO0o0OoOo0(Lcom/fongmi/android/tv/bean/Episode;)V

    return-void
.end method
""" + "\n"
    write(episode_fragment, s)

# Side episode list: download the selected episode and close the sheet.
s = read(side_dialog)
if ".method public onDownload(Lcom/fongmi/android/tv/bean/Episode;)V" not in s:
    s = s.rstrip() + r"""

.method public onDownload(Lcom/fongmi/android/tv/bean/Episode;)V
    .locals 1

    iget-object v0, p0, LoOoO0Oo0oOoO0OoO/OoOo0o0oOo0O0O0o;->OoOoO0O0o0oOoO0O:Lcom/fongmi/android/tv/model/SiteViewModel;

    invoke-virtual {v0, p1}, Lcom/fongmi/android/tv/model/SiteViewModel;->OoO0oOoO0o0OoOo0(Lcom/fongmi/android/tv/bean/Episode;)V

    iget-object p1, p0, LoOoO0Oo0oOoO0OoO/OoOo0o0oOo0O0O0o;->oOo0oO0o0O0O0Oo0:Lcom/google/android/material/sidesheet/SideSheetDialog;

    invoke-virtual {p1}, Landroidx/appcompat/app/AppCompatDialog;->dismiss()V

    return-void
.end method
""" + "\n"
    write(side_dialog, s)

# Player episode list: use the same built-in SiteViewModel download event.
s = read(video_activity)
if ".method public onDownload(Lcom/fongmi/android/tv/bean/Episode;)V" not in s:
    s = s.rstrip() + r"""

.method public onDownload(Lcom/fongmi/android/tv/bean/Episode;)V
    .locals 1

    iget-object v0, p0, Lcom/fongmi/android/tv/ui/activity/VideoActivity;->oOoOoO0Oo0oO0o0O:Lcom/fongmi/android/tv/model/SiteViewModel;

    invoke-virtual {v0, p1}, Lcom/fongmi/android/tv/model/SiteViewModel;->OoO0oOoO0o0OoOo0(Lcom/fongmi/android/tv/bean/Episode;)V

    return-void
.end method
""" + "\n"
    write(video_activity, s)

# Reusable long-click listener for all three episode holder layouts.
listener.parent.mkdir(parents=True, exist_ok=True)
listener_text = r""".class public final Lcom/fongmi/android/tv/ui/holder/EpisodeLongClickListener;
.super Ljava/lang/Object;
.source "OKVideoPatch"

.implements Landroid/view/View$OnLongClickListener;

.field private final callback:Lcom/fongmi/android/tv/ui/adapter/EpisodeAdapter$oOoOoOoOoOoOoO0o;

.field private final episode:Lcom/fongmi/android/tv/bean/Episode;

.method public constructor <init>(Lcom/fongmi/android/tv/ui/adapter/EpisodeAdapter$oOoOoOoOoOoOoO0o;Lcom/fongmi/android/tv/bean/Episode;)V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p1, p0, Lcom/fongmi/android/tv/ui/holder/EpisodeLongClickListener;->callback:Lcom/fongmi/android/tv/ui/adapter/EpisodeAdapter$oOoOoOoOoOoOoO0o;

    iput-object p2, p0, Lcom/fongmi/android/tv/ui/holder/EpisodeLongClickListener;->episode:Lcom/fongmi/android/tv/bean/Episode;

    return-void
.end method

.method public onLongClick(Landroid/view/View;)Z
    .locals 2

    iget-object v0, p0, Lcom/fongmi/android/tv/ui/holder/EpisodeLongClickListener;->callback:Lcom/fongmi/android/tv/ui/adapter/EpisodeAdapter$oOoOoOoOoOoOoO0o;

    iget-object v1, p0, Lcom/fongmi/android/tv/ui/holder/EpisodeLongClickListener;->episode:Lcom/fongmi/android/tv/bean/Episode;

    invoke-interface {v0, v1}, Lcom/fongmi/android/tv/ui/adapter/EpisodeAdapter$oOoOoOoOoOoOoO0o;->onDownload(Lcom/fongmi/android/tv/bean/Episode;)V

    const/4 v0, 0x1

    return v0
.end method
"""
write(listener, listener_text)

# Attach long-press handler immediately after the existing normal-click handler.
for path in holders:
    s = read(path)
    if "EpisodeLongClickListener" in s:
        continue

    cls = next((line.split()[-1] for line in s.splitlines() if line.startswith(".class ")), None)
    if not cls:
        raise SystemExit(f"Unable to determine class for {path}")

    needle = "    invoke-virtual {v0, v1}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V"
    if needle not in s:
        raise SystemExit(f"Click listener insertion point not found in {path}")

    extra = f"""

    iget-object v1, p0, {cls}->oOoO0o0oOo0oO0Oo:Lcom/fongmi/android/tv/ui/adapter/EpisodeAdapter$oOoOoOoOoOoOoO0o;

    new-instance v2, Lcom/fongmi/android/tv/ui/holder/EpisodeLongClickListener;

    invoke-direct {{v2, v1, p1}}, Lcom/fongmi/android/tv/ui/holder/EpisodeLongClickListener;-><init>(Lcom/fongmi/android/tv/ui/adapter/EpisodeAdapter$oOoOoOoOoOoOoO0o;Lcom/fongmi/android/tv/bean/Episode;)V

    invoke-virtual {{v0, v2}}, Landroid/view/View;->setOnLongClickListener(Landroid/view/View$OnLongClickListener;)V"""
    s = s.replace(needle, needle + extra, 1)
    write(path, s)

marker = root / "assets" / "okvideo_patch_status.txt"
marker.parent.mkdir(parents=True, exist_ok=True)
marker.write_text(
    "OKVideo patch: tap an episode to play; long-press an episode to download using the app's built-in downloader.\n",
    encoding="utf-8",
)

print("OKVideo download patch applied successfully")
