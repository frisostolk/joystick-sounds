# Raspberry Pi Joystick Sound Player

A Python project that reads input from an XY joystick controller connected to a Raspberry Pi and plays different animal sounds based on the joystick direction.

## Hardware Requirements

- Raspberry Pi (any model with GPIO)
- XY Joystick module (analog output)
- MCP3008 ADC converter (for reading analog joystick values)
- Speaker or audio output

## Wiring

Connect the joystick and MCP3008 to the Raspberry Pi:

### MCP3008 to Raspberry Pi:
- MCP3008 VDD -> Raspberry Pi 3.3V
- MCP3008 VREF -> Raspberry Pi 3.3V
- MCP3008 AGND -> Raspberry Pi GND
- MCP3008 DGND -> Raspberry Pi GND
- MCP3008 CLK -> Raspberry Pi SCLK (GPIO 11)
- MCP3008 DOUT -> Raspberry Pi MISO (GPIO 9)
- MCP3008 DIN -> Raspberry Pi MOSI (GPIO 10)
- MCP3008 CS -> Raspberry Pi CE0 (GPIO 8)

### Joystick to MCP3008:
- Joystick X axis -> MCP3008 CH0
- Joystick Y axis -> MCP3008 CH1
- Joystick GND -> MCP3008 AGND
- Joystick VCC -> MCP3008 VDD

## Software Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Enable SPI on Raspberry Pi:
   ```bash
   sudo raspi-config
   ```
   Go to Interfacing Options > SPI > Enable

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

- If SPI is not working, ensure it's enabled in raspi-config
- Check wiring connections
- Verify sound files are in the correct format (MP3)
- Run with `sudo` if you get permission errors for GPIO