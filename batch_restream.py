#!/usr/bin/env python3
# Batch Restreamer — CPU-friendly segment-based streaming
import os, sys, time, subprocess, glob

INPUT_URL   = os.environ.get("INPUT_URL",
    "https://rally-tv-live.akamaized.net/hls/live/2117704/RallyTV-Pri/master.m3u8")
INSTA_RTMPS = os.environ.get("INSTA_RTMPS", "")

if not INSTA_RTMPS:
    print("[!] INSTA_RTMPS is empty", file=sys.stderr)
    sys.exit(1)

SEG_SECONDS  = float(os.environ.get("SEG_SECONDS", "5"))
REST_SECONDS = float(os.environ.get("REST_SECONDS", "1"))
OUT_W        = os.environ.get("OUT_W", "720")
OUT_H        = os.environ.get("OUT_H", "1280")
OUT_FPS      = os.environ.get("OUT_FPS", "30")
VB           = os.environ.get("VIDEO_BITRATE", "4500k")
PRESET       = os.environ.get("PRESET", "superfast")
WORK_DIR     = "/tmp/restream_segs"

os.makedirs(WORK_DIR, exist_ok=True)

FILTER = (f"transpose=1,scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=increase,"
          f"crop={OUT_W}:{OUT_H},fps={OUT_FPS},setsar=1,format=yuv420p")

def clean():
    for f in glob.glob(os.path.join(WORK_DIR, "*.ts")):
        try: os.remove(f)
        except OSError: pass

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    seg_i = 0
    print(f"[>] Batch restream: seg={SEG_SECONDS}s rest={REST_SECONDS}s "
          f"{OUT_W}x{OUT_H}@{OUT_FPS}fps {VB} preset={PRESET}")
    try:
        while True:
            seg_i += 1
            seg = os.path.join(WORK_DIR, f"seg_{seg_i:04d}.ts")
            grab = ["ffmpeg", "-hide_banner", "-loglevel", "error",
                "-re", "-i", INPUT_URL, "-map", "0:v:0", "-map", "0:a:0",
                "-c", "copy", "-t", str(SEG_SECONDS), "-f", "mpegts", seg]
            r = run(grab)
            if r.returncode != 0 or not os.path.exists(seg) or os.path.getsize(seg) < 1000:
                time.sleep(1)
                continue
            enc = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", seg,
                "-vf", FILTER, "-c:v", "libx264", "-preset", PRESET, "-tune", "zerolatency",
                "-b:v", VB, "-maxrate", "6000k", "-bufsize", "12000k",
                "-g", str(int(float(OUT_FPS)*2)), "-r", OUT_FPS,
                "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
                "-f", "flv", INSTA_RTMPS]
            run(enc)
            clean()
            print(f"[>] seg {seg_i} done — resting {REST_SECONDS}s", flush=True)
            time.sleep(REST_SECONDS)
    except KeyboardInterrupt:
        print("\n[!] stopped by user")
    finally:
        clean()

if __name__ == "__main__":
    main()
