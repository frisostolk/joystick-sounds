#!/usr/bin/env python3
"""
test.py

Reads raw X and Y values from the Grove Base Hat ADC and prints when the
absolute difference from neutral (center) is greater than 50 units.

This uses the same channels as main.py (A0 -> channel 2, A1 -> channel 6).
"""
import time
from grove.adc import ADC

MAX_RAW = 4095
CENTER = MAX_RAW / 2.0  # 2047.5
X_CHANNEL = 2
Y_CHANNEL = 6
THRESHOLD_RAW = 50  # units in raw ADC scale


def main():
    try:
        adc = ADC()
    except Exception as e:
        print(f"Error initializing ADC: {e}")
        return

    print("Reading joystick raw values. Press Ctrl+C to stop.")

    try:
        while True:
            raw_x = adc.read_raw(X_CHANNEL)
            raw_y = adc.read_raw(Y_CHANNEL)

            diff_x = raw_x - CENTER
            diff_y = raw_y - CENTER

            if abs(diff_x) > THRESHOLD_RAW or abs(diff_y) > THRESHOLD_RAW:
                print(f"X: Raw={raw_x:4d}, Diff={diff_x:+6.1f} | Y: Raw={raw_y:4d}, Diff={diff_y:+6.1f}")

            time.sleep(0.05)
    except KeyboardInterrupt:
        print('\nStopped by user')


if __name__ == '__main__':
    main()
