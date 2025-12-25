import os
import sys

print("Checking Environment Variables...")
xdg = os.environ.get('XDG_RUNTIME_DIR')
print(f"XDG_RUNTIME_DIR: {xdg}")

if xdg:
    print(f"Service file should use: Environment=XDG_RUNTIME_DIR={xdg}")
else:
    print("WARNING: XDG_RUNTIME_DIR is not set in this shell!")
