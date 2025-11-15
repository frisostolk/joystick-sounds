#!/usr/bin/env python3
"""
Raspberry Pi Joystick Sound Player

This script reads input from an XY joystick connected via MCP3008 ADC
and plays different animal sounds based on the joystick direction.

Connections:
- Joystick X axis to MCP3008 channel 0
- Joystick Y axis to MCP3008 channel 1
- MCP3008 connected to Raspberry Pi SPI pins

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

from gpiozero import MCP3008
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

# Set up ADC channels for joystick
# Assuming MCP3008 is connected to SPI
x_axis = MCP3008(channel=0)  # X axis
y_axis = MCP3008(channel=1)  # Y axis

# Thresholds for direction detection (adjust as needed)
THRESHOLD_HIGH = 0.6
THRESHOLD_LOW = 0.4

def get_direction(x_val, y_val):
    """
    Determine direction based on joystick values
    Values are between 0 and 1
    """
    if x_val > THRESHOLD_HIGH and y_val > THRESHOLD_HIGH:
        return 'northeast'
    elif x_val > THRESHOLD_HIGH and y_val < THRESHOLD_LOW:
        return 'southeast'
    elif x_val < THRESHOLD_LOW and y_val > THRESHOLD_HIGH:
        return 'northwest'
    elif x_val < THRESHOLD_LOW and y_val < THRESHOLD_LOW:
        return 'southwest'
    elif x_val > THRESHOLD_HIGH:
        return 'east'
    elif x_val < THRESHOLD_LOW:
        return 'west'
    elif y_val > THRESHOLD_HIGH:
        return 'north'
    elif y_val < THRESHOLD_LOW:
        return 'south'
    else:
        return 'center'

def main():
    print("Joystick Sound Player started. Move joystick to play sounds.")
    print("Press Ctrl+C to exit.")

    last_direction = None

    try:
        while True:
            # Read joystick values
            x_val = x_axis.value
            y_val = y_axis.value

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
        x_axis.close()
        y_axis.close()
        pygame.mixer.quit()

if __name__ == "__main__":
    main()