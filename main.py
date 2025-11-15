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

# Initialize pygame mixer
pygame.mixer.init()

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

# Load sounds
sounds = {}
for direction, file_path in sound_files.items():
    if os.path.exists(file_path):
        sounds[direction] = pygame.mixer.Sound(file_path)
    else:
        print(f"Warning: Sound file {file_path} not found")

# Set up ADC for Grove Base Hat
adc = ADC()

# ADC channels for joystick (based on your setup)
X_CHANNEL = 2  # A0
Y_CHANNEL = 6  # A1

# Thresholds for direction detection (adjust based on your joystick)
THRESHOLD = 0.3  # Normalized values are -1 to 1

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

    last_direction = None

    try:
        while True:
            # Read raw values from ADC
            raw_x = adc.read_raw(X_CHANNEL)
            raw_y = adc.read_raw(Y_CHANNEL)
            
            # Normalize to -1 to 1 (center at 2047.5 for 12-bit ADC)
            center = 2047.5
            x_val = (raw_x - center) / center
            y_val = (raw_y - center) / center
            
            # Clamp values
            x_val = max(-1.0, min(1.0, x_val))
            y_val = max(-1.0, min(1.0, y_val))

            # Get current direction
            direction = get_direction(x_val, y_val)

            # Play sound if direction changed and sound exists
            if direction != last_direction and direction in sounds and direction != 'center':
                print(f"Playing {direction} sound")
                sounds[direction].play()
                last_direction = direction
            elif direction == 'center':
                last_direction = None  # Reset when centered

            time.sleep(0.1)  # Small delay to prevent rapid triggering

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Clean up
        pygame.mixer.quit()

if __name__ == "__main__":
    main()