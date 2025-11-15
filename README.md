# Raspberry Pi Joystick Sound Player

A Python project that reads input from a Grove Base Hat Dual-Axis Joystick connected to a Raspberry Pi and plays different animal sounds based on the joystick direction.

## Hardware Requirements

- Raspberry Pi (any model)
- Grove Base Hat
- Grove Dual-Axis Joystick module
- Speaker or audio output

## Wiring

Connect the Grove Dual-Axis Joystick to the Grove Base Hat:

- Joystick X axis -> A0 port on Grove Base Hat
- Joystick Y axis -> A1 port on Grove Base Hat
- Ensure Grove Base Hat is properly seated on Raspberry Pi GPIO pins

## Software Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure I2C is enabled on Raspberry Pi:
   ```bash
   sudo raspi-config
   ```
   Go to Interfacing Options > I2C > Enable

3. Place sound files in the `sounds/` directory:
   - `cow.mp3` - for north direction
   - `horse.mp3` - for northeast
   - `pig.mp3` - for east
   - `bird.mp3` - for southeast
   - `elephant.mp3` - for south
   - `tiger.mp3` - for southwest
   - `frog.mp3` - for west
   - `owl.mp3` - for northwest

## Usage

Run the script:
```bash
python main.py
```

Move the joystick in different directions to play the corresponding animal sounds.

## Direction Mapping

- **North**: Cow sound
- **Northeast**: Horse sound
- **East**: Pig sound
- **Southeast**: Bird sound
- **South**: Elephant sound
- **Southwest**: Tiger sound
- **West**: Frog sound
- **Northwest**: Owl sound

## Calibration

You may need to adjust the threshold values in `main.py` (THRESHOLD_HIGH and THRESHOLD_LOW) based on your joystick's center position and range.

## Troubleshooting

- If I2C is not working, ensure it's enabled in raspi-config and Grove Base Hat is properly seated
- Check joystick connections to A0 and A1 ports
- Verify sound files are in the correct format (MP3) and in the `sounds/` directory
- Run with `sudo` if you get permission errors for I2C/GPIO access