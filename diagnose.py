#!/usr/bin/env python3
import time
import sys
from grove.adc import ADC

def draw_bar(val, center=2047.5):
    # val is 0-4095
    # Normalize to -1.0 to 1.0
    norm = (val - center) / center
    norm = max(-1.0, min(1.0, norm))
    
    # Width of half-bar
    width = 20
    
    # Calculate bars
    if norm < 0:
        # Left side
        # Length of bar is proportional to abs(norm)
        # e.g. norm = -0.5 -> len = 10
        # string: " " * (width - len) + "#" * len + "|" + " " * width
        bar_len = int(abs(norm) * width)
        s = " " * (width - bar_len) + "#" * bar_len + "|" + " " * width
    else:
        # Right side
        bar_len = int(norm * width)
        s = " " * width + "|" + "#" * bar_len + " " * (width - bar_len)
        
    return f"{s} {norm:+.2f} ({val})"

def main():
    print("Joystick Diagnostic Tool")
    print("------------------------")
    print("Checking Channels 0 (X) and 6 (Y) as defined in main.py")
    print("Please move the joystick to ALL limits (Up, Down, Left, Right)")
    print("Press Ctrl+C to stop.\n")

    try:
        adc = ADC()
    except Exception as e:
        print(f"Error connecting to HAT: {e}")
        return

    # Channels expected by main.py
    CH_X = 0
    CH_Y = 6

    try:
        while True:
            try:
                x = adc.read_raw(CH_X)
                y = adc.read_raw(CH_Y)
            except OSError:
                print("I/O Error reading ADC")
                time.sleep(1)
                continue

            bar_x = draw_bar(x)
            bar_y = draw_bar(y)

            # Signal quality check
            status = []
            
            # center approx 2048. If it's 0 or 4095 stuck, warn
            if x < 100 or x > 4000: status.append("X STUCK")
            if y < 100 or y > 4000: status.append("Y STUCK")
            
            # Check weak signal (if user is moving it)
            # We can't know if they are moving it, but we can show the max seen?
            # Let's just print the bars dynamically
            
            sys.stdout.write(f"\rX: {bar_x}  Y: {bar_y}   ")
            sys.stdout.flush()
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\nTest Finished.")

if __name__ == "__main__":
    main()
