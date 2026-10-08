# Insta-Restream 🏎️➡️📱

Re-stream any IPTV channel to an Instagram Live via RTMPS, offloaded to **GitHub Actions** (free 4-vCPU runner) so your local box stays idle.

## How it works
```
Rally TV (1080p50, 16:9)
   │  ffmpeg on GitHub Actions runner (4 cores)
   │  rotate 90° + scale-cover + crop → 1080x1920 (9:16 full screen)
   ▼
Instagram Live (RTMPS)
```

## One-time setup (do this ONCE)

### 1. Push this repo to GitHub
```bash
cd insta-restream
git init
git add .
git commit -m "insta restream"
git branch -M main
git remote add origin https://github.com/<YOUR_USER>/insta-restream.git
git push -u origin main
```

### 2. Add secrets (Settings → Secrets and variables → Actions)
| Secret | Value |
|--------|-------|
| `INSTA_RTMPS` | your Instagram RTMPS URL (from .env, the `rtmps://...` line) |
| `INPUT_URL` | `https://rally-tv-live.akamaized.net/hls/live/2117704/RallyTV-Pri/master.m3u8` |

> ⚠️ The RTMPS key/token **expires every session**. Fetch a fresh one from
> Instagram (mobile → Live → share link) before each run.

### 3. Run it
- Go to **Actions → "Instagram Live Restream" → Run workflow**.
- (Optional) the cron already auto-runs every hour.

## Local run (optional, on this box)
```bash
cp .env.example .env   # then fill in INSTA_RTMPS
bash run_live.sh
```

## Notes
- Instagram caps live resolution at ~1080p and 6000 kbps — this is the ceiling.
- Free GitHub runner = 6h job limit; IG live = ~4h; both are fine together.
- `.env` is gitignored — the secret never leaves your machine.
