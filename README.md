## About this fork

To match the 3D printed [Raspberry Pi Pipboy](https://makerworld.com/en/models/1805084-raspberry-pi-pipboy?from=search#profileId-1925209), the GPIO handling is enabled for the buttons to work.

I've also added two handlres called `next_submodule` and `prev_submodule`, to replace the 5 knobs with two buttons.

Since I am running this on a "Lite" version of Raspberry PI OS, with no desktop, I replaced the gpio.py that comes with the model and made it work with `evdev` so it works without a desktop. You just need it to make sure the buttons are setup correctly, otherwise the handling is done in other source files.



## Autorun as a service


To make the Pip-Boy start automatically on a Raspberry Pi, the best method is using **systemd**. This ensures that the program starts after the network and graphics are ready, and it can automatically restart the app if it crashes.

I assume you are using a **virtual environment (venv)**, so we need to point the service specifically to the python executable inside that folder.

---

### 1. Create the Service File

Run the following command to create a new service file:

```bash
sudo nano /etc/systemd/system/pypboy.service
```

### 2. Paste the Configuration

Paste the following into the editor. **Note:** I am assuming your username is `pi` and the folder is `/home/pi/pypboy`. If your path is different, adjust it accordingly.

```ini
[Unit]
Description=PyPboy Interface
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pypboy
# Points to the python inside your venv
ExecStart=/home/pi/pypboy/venv/bin/python main.py
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1
# If using a physical screen, you might need to specify the display
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target
```

*Press `Ctrl+O`, `Enter`, then `Ctrl+X` to save and exit.*

---

### 3. Enable and Start the Service

Now, tell the system to recognize the new service and run it at boot:

```bash
# Reload the systemd daemon to see the new file
sudo systemctl daemon-reload

# Enable it to start on boot
sudo systemctl enable pypboy.service

# Start it now to test it
sudo systemctl start pypboy.service
```

### 4. How to Check the Status

If the app doesn't appear, or you want to see the logs (to check for that `xmltodict` error), use:

```bash
sudo systemctl status pypboy.service
```

To see live logs as the app runs:

```bash
journalctl -u pypboy.service -f
```

---

### Important: Permissions for Graphics

If you are running Raspberry Pi OS with a desktop (GUI), the service above should work. However, if you are running in **CLI/Lite mode**, Pygame needs permission to access the framebuffer.

If it fails to start, try adding your user to the video and input groups:

```bash
sudo usermod -a -G video,input pi
```

### Next Step

Try rebooting your Pi with `sudo reboot` to see if it launches on its own!

**Would you like me to show you how to add a "Safe Shutdown" button to your Python code so you can turn off the Pi safely from the Pip-Boy interface?**

#
Here is the original README.md :
# pypboy

> _Notes from ZapWizard:_
>
> This is a work in progress of the code for my Functional Pip-Boy 3000 MK IV.
>
> I branched off from the Fallout 3 style Pip-Boy 3000 code.
> The graphics are positioned for a 720x720 display.

## Installation

#### These installation instructions _assume_ that you're running on a Raspberry Pi running Raspberry Pi OS

To download and install dependencies required to run, run the following in a terminal (or remotely via SSH).

```sh
git clone https://github.com/zapwizard/pypboy.git
cd pypboy
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

At this point you should be good to go. If you're accessing the Pi remotely via SSH etc. then you'll have to first set the display with `export DISPLAY=:0` otherwise run:

```sh
python main.py
```

## Controls

#### Navigation

|     |             |
| --- | ----------- |
| F1  | Stats       |
| F2  | Inventory   |
| F3  | Data        |
| F4  | Map         |
| F5  | Radio       |
| F6  | Boot screen |

1,2,3,4, etc. are used to navigate the sub-header menu.

Up/Down arrow keys to navigate the sub-menus.

+/- to zoom the map

## Adding Radio Stations

Adding radio stations is now as easy as making a folder in sounds/radio with MP3, OGG or WAV files.
Make a file named `Station.py`, with `station_name = "Your name here"` to set the menu text. The folder name is used if this file is missing.
Add a number to the beginning of the folder name to set the menu position.

If you want the original in-game music you can use the B.A.E. program to extract the files from the game, then the Yakitori Audio Converter to convert them back to MP3 files.

## Developing

The easiest way to keep track of local development is by creating a Python virtual environment, create one using `python -m venv venv`, this creates a virtual env called `venv` which can be activated in Linux/Mac using `. ./venv/bin/activate`, if you're on Windows it's slightly different but you can find more information about virtual environments here https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment.

Once inside the virtual environment install all the necessary requirements with `pip install -r requirements.txt`. After this step you should be able to run `python main.py` and the app should run up.

### Caching Maps

- In `settings.py` set `LOAD_CACHED_MAP = False`
- Run the application once
- In `settings.py` set `LOAD_CACHED_MAP = True`
- Pypboy will now load the cached map on starting

### Enable app to startup on boot

```
pi@XXXX:~/Downloads/pypboy $ cat ~/launch_pipboy.sh
#!/bin/bash
cd ~/Downloads/pypboy
python ./main.py

pi@XXXX:~/Downloads/pypboy $ grep launch_pipboy /etc/lightdm/lightdm.conf
session-setup-script=/home/pi/launch_pipboy.sh
pi@XXXX:~/Downloads/pypboy $
```

## Authors

- Major overhaul by ZapWizard for the Functional Pip-Boy 3000 MK IV GUI

- Fixes and Updates by kingpinzs

- Fixes and Updates by amolloy

- Fixes and Updates by Goldstein

- Updates by Sabas of The Inventor's House Hackerspace

- Originally by grieve work original<br>

## License

MIT
