#!/bin/bash
# ============================================================
#  Instagram Live Re-Streamer (FFmpeg)
#  Runs on GitHub Actions runner (4 vCPU) OR any Linux box.
#  Source: Rally TV (1080p50) -> rotated 90° + cover crop
#  => full-screen 9:16 vertical, no black bars.
# ============================================================
set -euo pipefail

INPUT_URL="${INPUT_URL:-https://rally-tv-live.akamaized.net/hls/live/2117704/RallyTV-Pri/master.m3u8}"
INSTA_RTMPS="${INSTA_RTMPS:-}"

[[ -z "$INSTA_RTMPS" ]] && { echo "ERROR: INSTA_RTMPS empty" >&2; exit 1; }

OUT_W="${OUT_W:-1080}"
OUT_H="${OUT_H:-1920}"
OUT_FPS="${OUT_FPS:-50}"
VB="${VIDEO_BITRATE:-6000k}"
MAXR="${MAXRATE:-6500k}"
CORES="$(nproc)"

echo ">>> Instagram Live restream (${OUT_W}x${OUT_H}@${OUT_FPS}fps, ${VB}, ${CORES} cores)"
echo ">>> Source: $INPUT_URL"

FILTER="transpose=1,scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=increase,crop=${OUT_W}:${OUT_H},fps=${OUT_FPS},setsar=1,format=yuv420p"

exec ffmpeg -hide_banner -loglevel warning \
  -re -i "$INPUT_URL" \
  -map 0:v:0 -map 0:a:0 \
  -vf "$FILTER" \
  -c:v libx264 -preset fast -tune zerolatency -threads "$CORES" \
  -b:v "$VB" -maxrate "$MAXR" -bufsize 13000k \
  -g $((OUT_FPS*2)) -r "$OUT_FPS" \
  -c:a aac -b:a 160k -ar 48000 \
  -f flv "$INSTA_RTMPS"
