import RPi.GPIO as GPIO
import time
from evdev import UInput, ecodes as e

# Initialize Virtual Keyboard
ui = UInput()

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Map GPIO Pins to evdev Keycodes
# Note: F-keys are e.KEY_F1, etc.
buttons = {
    17: e.KEY_F1,
    24: e.KEY_F2,
    27: e.KEY_F3
    10: e.KEY_F4,
    7:  e.KEY_F5,
    26: e.KEY_LEFT,    
    16: e.KEY_RIGHT,
    5:  e.KEY_UP,
    13: e.KEY_DOWN,
}

# Setup inputs with pull-up resistors
for pin in buttons:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Listening for button presses via evdev... (Ctrl+C to exit)")

try:
    while True:
        for pin, key_code in buttons.items():
            if GPIO.input(pin) == GPIO.LOW:  # Button Pressed
                ui.write(e.EV_KEY, key_code, 1) # 1 = Key Down
                ui.write(e.EV_KEY, key_code, 0) # 0 = Key Up
                ui.syn()
                print(f"Sent keycode: {key_code}")
                time.sleep(0.2) # Debounce
except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    ui.close()
    GPIO.cleanup()

