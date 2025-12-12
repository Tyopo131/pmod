import sys
import os

log_level = os.getenv("PMOD_LOG", "warn").lower()
stream = sys.stderr
# Prints text to stderr
def fatal(text): 
    print(f"[FATAL] {text}", file=stream)
def error(text):
    if log_level not in ("debug", "info", "warn", "error"): return -1
    print(f"[ERROR] {text}", file=stream)
def warn(text):
    if log_level not in ("debug", "info", "warn"): return -1
    print(f"[WARN] {text}", file=stream)
def info(text):
    if log_level not in ("debug", "info"): return -1
    print(f"[INFO] {text}", file=stream)
def debug(text):
    if log_level != "debug": return -1
    print(f"[DEBUG] {text}", file=stream)
def shutdown():
    if not stream.closed:
        stream.close()
