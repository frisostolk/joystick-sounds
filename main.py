#!/usr/bin/env python3
"""
Raspberry Pi Joystick Sound Player

This script reads input from a Grove Base Hat Dual-Axis Joystick
and plays different animal sounds based on the joystick direction.

Connections:
- Joystick X axis connected to A0 (ADC channel 2)
- Joystick Y axis connected to A1 (ADC channel 6)
- Grove Base Hat properly seated on Raspberry Pi

Sound files should be placed in the 'sounds' directory:
- cow.mp3 for north
- horse.mp3 for northeast
- pig.mp3 for east
- bird.mp3 for southeast
- elephant.mp3 for south
- tiger.mp3 for southwest
- frog.mp3 for west
- owl.mp3 for northwest
"""

from grove.adc import ADC
import pygame
import time
import os
from collections import deque
import signal
import threading
#os.environ['SDL_AUDIODRIVER'] = 'alsa'
# Initialize pygame mixer with specific settings to reduce buffer underuns/lag
# frequency=44100, size=-16, channels=2, buffer=1024
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)


# Define sound mappings
sound_files = {
    'north': 'sounds/cow.mp3',
    'northeast': 'sounds/horse.mp3',
    'east': 'sounds/pig.mp3',
    'southeast': 'sounds/bird.mp3',
    'south': 'sounds/elephant.mp3',
    'southwest': 'sounds/tiger.mp3',
    'west': 'sounds/frog.mp3',
    'northwest': 'sounds/owl.mp3'
}

# Special gesture sound
FEYENOORD_FILE = 'sounds/feyenoord.mp3'

# Load sounds
sounds = {}
for direction, file_path in sound_files.items():
    if os.path.exists(file_path):
        sounds[direction] = pygame.mixer.Sound(file_path)
    else:
        print(f"Warning: Sound file {file_path} not found")

feyenoord_sound = None
if os.path.exists(FEYENOORD_FILE):
    feyenoord_sound = pygame.mixer.Sound(FEYENOORD_FILE)
else:
    print(f"Warning: Gesture sound {FEYENOORD_FILE} not found")

# Play startup sound so user checks audio immediately
if 'north' in sounds:
    print("Playing startup sound (cow)...")
    sounds['north'].play()
    time.sleep(1.0)


# Set up ADC for Grove Base Hat
adc = None
try:
    adc = ADC()
except Exception as e:
    print(f"\nError initializing Grove Base Hat: {e}")
    print("Please check:\n1. Is the HAT properly seated?\n2. Is I2C enabled? (raspi-config)\n3. Are the wires connected securely?")
    running = False


# ADC channels for joystick (based on your setup)
X_CHANNEL = 0  # A0
Y_CHANNEL = 6  # A1

# Thresholds for direction detection (adjust based on your joystick)
THRESHOLD = 0.5  # Normalized values are -1 to 1

# Gesture detection parameters
GESTURE_WINDOW_SECONDS = 2.0

# Single mixer channel so there cannot be two sounds simultaneously
PLAY_CHANNEL = pygame.mixer.Channel(0)

# Global flag for clean shutdown
running = True

def signal_handler(sig, frame):
    global running
    print("\nInterrupt received, shutting down...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

def read_adc_safe(adc, channel):
    """Read ADC value safely without heavy threading."""
    try:
        return adc.read_raw(channel)
    except Exception as e:
        print(f"ADC read error: {e}")
        return None


def get_direction(x_val, y_val):
    """
    Determine direction based on joystick values
    Values are normalized to -1 to 1, with 0 being center
    """
    if x_val > THRESHOLD and y_val > THRESHOLD:
        return 'northeast'
    elif x_val > THRESHOLD and y_val < -THRESHOLD:
        return 'southeast'
    elif x_val < -THRESHOLD and y_val > THRESHOLD:
        return 'northwest'
    elif x_val < -THRESHOLD and y_val < -THRESHOLD:
        return 'southwest'
    elif x_val > THRESHOLD:
        return 'east'
    elif x_val < -THRESHOLD:
        return 'west'
    elif y_val > THRESHOLD:
        return 'north'
    elif y_val < -THRESHOLD:
        return 'south'
    else:
        return 'center'

def main():
    print("Joystick Sound Player started. Move joystick to play sounds.")

    print("Press Ctrl+C to exit.")

    global running


    last_direction = None
    # For gesture detection (store tuples of (direction, timestamp))
    gesture_events = deque()

    try:
        while running:
            if adc is None:
                print("Hardware not initialized. Exiting.")
                break

            # Read raw values from ADC safely
            raw_x = read_adc_safe(adc, X_CHANNEL)

            raw_y = read_adc_safe(adc, Y_CHANNEL)

            
            if raw_x is None or raw_y is None:
                print("ADC read failed, skipping...")
                time.sleep(0.1)
                continue
            
            # Normalize to -1 to 1 (center at 2047.5 for 12-bit ADC)
            center = 2047.5
            x_val = (raw_x - center) / center
            y_val = (raw_y - center) / center
            
            # Clamp values
            x_val = max(-1.0, min(1.0, x_val))
            y_val = max(-1.0, min(1.0, y_val))

            # Get current direction
            direction = get_direction(x_val, y_val)

            # Gesture tracking: only consider left/right events
            now = time.time()
            if direction in ('west', 'east'):
                # Append event only if different from last recorded event
                if not gesture_events or gesture_events[-1][0] != direction:
                    gesture_events.append((direction, now))
                
                # Purge old events
                while gesture_events and now - gesture_events[0][1] > GESTURE_WINDOW_SECONDS:
                    gesture_events.popleft()

                # Check for gesture patterns in the window
                seq = [d for d, t in gesture_events]
                if len(seq) >= 3 and feyenoord_sound:
                    last_three = seq[-3:]
                    if last_three == ['west', 'east', 'west'] or last_three == ['east', 'west', 'east']:
                        # Stop any currently playing sound and play gesture sound
                        if PLAY_CHANNEL.get_busy():
                            PLAY_CHANNEL.stop()
                        print("Gesture detected: left-right-left -> playing feyenoord.mp3")
                        PLAY_CHANNEL.play(feyenoord_sound)
                        # clear events so we don't retrigger
                        gesture_events.clear()
                        last_direction = 'gesture'
                        
                        # Wait for 30 seconds before detecting new inputs
                        # We use a loop to ensure we can still catch the shutdown signal
                        print("Gesture detected. Pausing detection for 30 seconds...")
                        for _ in range(300):  # 300 * 0.1s = 30s
                            if not running:
                                break
                            time.sleep(0.1)
                        continue

            # Sound control rules:
            # - Do not play two sounds at once: stop channel before playing new sound
            # - Stop playback when joystick returns to neutral
            if direction == 'center':
                if PLAY_CHANNEL.get_busy():
                    PLAY_CHANNEL.stop()
                    print("Joystick centered -> stopping sound")
                last_direction = None
            elif direction != last_direction and direction in sounds:
                # Play corresponding sound, ensuring single sound at a time
                if PLAY_CHANNEL.get_busy():
                    PLAY_CHANNEL.stop()
                print(f"Playing {direction} sound")
                PLAY_CHANNEL.play(sounds[direction])
                last_direction = direction

            time.sleep(0.1)  # Small delay to prevent rapid triggering

    except KeyboardInterrupt:
        print("\nExiting...")
        running = False
    finally:
        # Clean up
        if PLAY_CHANNEL.get_busy():
            PLAY_CHANNEL.stop()
        pygame.mixer.quit()

if __name__ == "__main__":
    main()