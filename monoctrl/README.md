# MonoCtrl 1.0

**MonoCtrl** _[monocontrol]_  is a control interface for the Korg Monologue synthesiser.

Written by [Blokatt](https://twitter.com/blokatt).

### Download (v1.0): [itch.io](https://blokatt.itch.io/monoctrl),  [GitHub](https://github.com/Blokatt/FX4Reaper/releases/tag/MonoCtrl)

![](/monoctrl/monoctrlPreview.gif)

Features:
-----
- Two-way CC/PC sync
- Automatic preset requesting via SysEx
- Parameter randomisation/mutation
- User preset support
- MIDI passthrough options
- SysEx-safe MIDI channel selection

-----

Installation:
-----
- Simply run ***install_windows.bat*** *or* create a new directory called ***blokatt*** in your ***Effects*** folder (usually found in *%appdata%/Reaper/*) and copy the ***monoctrl*** folder into it.

Setup guide:
-----
1. Create a new track and change the following settings:
2. Input: **MIDI** - 
  - *'Monologue KBD/KNOB'* (All channels! -> important for SysEx reasons)
3. Routing -> **MIDI Hardware Output** -
  - *'Monologue SOUND'*, enable low latency mode in Options -> Preferences -> Devices -> MIDI outputs*
4. Add **MonoCtrl** as a track effect

Arm recording and enable monitoring.
Make sure Tx/Rx MIDI is enabled in the global settings of your Monologue!

##### *) Not doing this may result in timing issues.

![](/monoctrl/monoctrlGuide.gif)

-----

Notes:
-----
The **utils** folder contains various scripts I wrote to aid me in the development of this effect (mainly SysEx reverse-engineering). Some of them depend on [Mido - MIDI Objects for Python](https://mido.readthedocs.io/en/latest/).

**sysex.py** contains a partial documentation of the Monologue SysEx program data format in the form of comments. I plan on writing this all up properly in the future.
