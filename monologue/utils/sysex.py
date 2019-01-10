from reportlab.lib.validators import isNumberInRange

from misc import *
import mido

def canParseFromHex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def analyse_sysex(buf):
    #print(buf)
    buf = [int(x, 16) for x in buf.split() if canParseFromHex(x)]

    # Name (12*8 bits)
    # Byte 12 - 22
    # Byte 24 - 25

    offset = 12
    name = ""
    for i in range(0, 11):
        name += chr(buf[offset + i])
    offset = 24
    for i in range(0, 1):
        name += chr(buf[offset + i])
    print("Name: " + name)
    # Overdrive (10 bits)
    # Byte 39     - bit 2
    # Byte 39 + 2 - bits 1 - 7
    # Byte 39 + 8 - bit 1
    # Byte 39 + 9 - bit 7

    offset = 39
    value = ((buf[offset] & 2) << 8)
    value = value | ((buf[offset + 2] & 127) << 2)
    value = value | ((buf[offset + 8] & 1) << 1)
    value = value | ((buf[offset + 9] & 64) >> 6)
    CCDrive = value
    print("Drive: " + str(value))

    # VCO1 Wave (2 bits)
    # Byte 39 - bit 3
    # Byte 39 + 3 - bit 7

    offset = 39
    value = ((buf[offset] & 4) >> 1)
    value = value | ((buf[offset + 3] & 64) >> 6)
    CCVCO1Wave = value
    print("VCO1 Waveform: " + str(CCVCO1Wave))


    # VCO1 Shape (10 bits)
    # Byte 24      - bit 4
    # Byte 24 + 4  - bit 1-7
    # Byte 24 + 19 - bit 3-4

    offset = 23
    value = ((buf[offset] & 8) << 6)
    value = value | ((buf[offset + 4] & 127) << 2)
    value = value | ((buf[offset + 19] & 12) >> 2)
    CCVCO1Shape = value
    print("VCO1 Shape: " + str(CCVCO1Shape))

    # VCO2 Octave (2 bits)
    # Byte 43 - bit 5-6

    offset = 43
    value = (buf[offset] & 48) >> 4
    CCVCO2Octave = value
    print("VCO2 Octave: " + str(CCVCO2Octave))

    # VCO2 Wave (2 bits)
    # Byte 39 - bit 4
    # Byte 39 + 4 - bit 7

    offset = 39
    value = ((buf[offset] & 8) >> 2)
    value = value | ((buf[offset + 4] & 64) >> 6)
    CCVCO2Wave = value
    print("VCO1 Waveform: " + str(CCVCO2Wave))

    # Ring/Sync (2 bits)
    # Byte 39 - bit 1-2

    offset = 44
    value = (buf[offset] & 3)

    CCRingSync = value
    print("Ring/Sync: " + str(CCRingSync))

    # VCO2 Shape (10 bits)
    # Byte 24      - bit 6
    # Byte 24 + 6  - bit 1-7
    # Byte 24 + 20 - bit 2-4

    offset = 23
    value = ((buf[offset] & 32) << 4)
    value = value | ((buf[offset + 6] & 127) << 2)
    value = value | ((buf[offset + 20] & 12) >> 2)
    CCVCO2Shape = value
    print("VCO2 Shape: " + str(CCVCO2Shape))

    # VCO2 Pitch (10 bits)
    # Byte 24      - bit 5
    # Byte 24 + 5  - bit 1-7
    # Byte 24 + 20 - bit 1-2

    offset = 23
    value = ((buf[offset] & 16) << 5)
    value = value | ((buf[offset + 5] & 127) << 2)
    value = value | (buf[offset + 20] & 3)
    CCVCO2Pitch = value
    print("VCO2 Pitch: " + str(CCVCO2Pitch))

    # VCO1 Level (10 bits)
    # Byte 23      - bit 7
    # Byte 23 + 7  - bit 1-7
    # Byte 23 + 22 - bit 1-2

    offset = 23
    value = ((buf[offset] & 64) << 3)
    value = value | ((buf[offset + 7] & 127) << 2)
    value = value | (buf[offset + 22] & 3)
    CCVCO1Level = value
    print("VCO1 Level: " + str(CCVCO1Level))
    
    # VCO2 Level (10 bits)
    # Byte 31      - bit 1
    # Byte 31 + 1  - bit 1-7
    # Byte 31 + 14 - bit 2-4

    offset = 31
    value = ((buf[offset] & 1) << 9)
    value = value | ((buf[offset + 1] & 127) << 2)
    value = value | (buf[offset + 14] & 12) >> 2
    CCVCO2Level = value
    print("VCO2 Level: " + str(CCVCO2Level))

    # Filter Cutoff (10 bits)
    # Byte 31      - bit 2
    # Byte 31 + 2  - bit 1-7
    # Byte 31 + 14 - bit 5-6

    offset = 31
    value = (buf[offset] & 2) << 8
    value = value | ((buf[offset + 2] & 127) << 2)
    value = value | ((buf[offset + 14] & 48) >> 4)
    CCFilterCutoff = value
    print("Filter cutoff: " + str(CCFilterCutoff))

    # Filter Resonance (10 bits)
    # Byte 31      - bit 3
    # Byte 31 + 3  - bit 1-7
    # Byte 31 + 8  - bit 6
    # Byte 31 + 14 - bit 7

    offset = 31
    value = (buf[offset] & 4) << 7
    value = value | ((buf[offset + 3] & 127) << 2)
    value = value | ((buf[offset + 8] & 32) >> 4)
    value = value | ((buf[offset + 14] & 64) >> 6)
    CCFilterResonance = value
    print("Filter resonance: " + str(CCFilterResonance))

    # EG Type (2 bits)
    # Byte 46       - bit 1-2

    offset = 46
    value = (buf[offset] & 3)
    CCEGType = value
    print("EG Type: " + str(CCEGType))

    # EG Attack (10 bits)
    # Byte 31      - bit 4
    # Byte 31 + 4  - bit 1-7
    # Byte 31 + 15 - bit 2-4

    offset = 31
    value = (buf[offset] & 8) << 6
    value = value | ((buf[offset + 4] & 127) << 2)
    value = value | ((buf[offset + 15] & 12) >> 2)
    CCEGAttack = value
    print("EG Attack: " + str(CCEGAttack))

    # EG Decay (10 bits)
    # Byte 31      - bit 5
    # Byte 31 + 5  - bit 1-7
    # Byte 31 + 15 - bit 5-6

    offset = 31
    value = (buf[offset] & 16) << 5
    value = value | ((buf[offset + 5] & 127) << 2)
    value = value | ((buf[offset + 15] & 48) >> 4)
    CCEGDecay = value
    print("EG Decay: " + str(CCEGDecay))

    # EG Intensity (10 bits)
    # Byte 31      - bit 6
    # Byte 31 + 6  - bit 1-7
    # Byte 31 + 17 - bit 1-2
    # (hold shift for negative values, max at 1022)

    offset = 31
    value = (buf[offset] & 32) << 4
    value = value | ((buf[offset + 6] & 127) << 2)
    value = value | ((buf[offset + 17] & 2))
    CCEGIntensity = value
    print("EG Intensity: " + str(CCEGIntensity))

    # EG Target (2 bits)
    # Byte 39      - bit 7
    # Byte 39 + 7  - bit 7

    offset = 39
    value = (buf[offset] & 64) >> 5
    value = value | ((buf[offset + 7] & 64) >> 6)
    CCEGTarget = value
    print("EG Target: " + str(CCEGTarget))

    # LFO Wave (2 bits)
    # Byte 49      - bit 1-2

    offset = 49
    value = (buf[offset] & 3)
    CCLFOWave = value
    print("LFO Wave: " + str(CCLFOWave))

    # LFO Mode (2 bits)
    # Byte 49      - bit 2-4

    offset = 49
    value = (buf[offset] & 12) >> 2
    CCLFOMode = value
    print("LFO Mode: " + str(CCLFOMode))

    # LFO Rate (10 bits)
    # Byte 31      - bit 7
    # Byte 31 + 7  - bit 1-7
    # Byte 31 + 17 - bit 2-4

    offset = 31
    value = (buf[offset] & 64) << 3
    value = value | ((buf[offset + 7] & 127) << 2)
    value = value | ((buf[offset + 17] & 12) >> 2)
    CCLFORate = value
    print("LFO Rate: " + str(CCLFORate))

    # LFO Intensity (10 bits)
    # Byte 39      - bit 1
    # Byte 31 + 1  - bit 1-7
    # Byte 31 + 9  - bit 6-7
    # (hold shift for negative values, max at 1022)

    offset = 39
    value = (buf[offset] & 1)
    value = value | ((buf[offset + 1] & 127) << 1)
    value = value | ((buf[offset + 9] & 48) << 4)
    CCLFOIntensity = value
    print("LFO Intensity: " + str(CCLFOIntensity))

    # LFO Target (2 bits)
    # Byte 49      - bit 5-6

    offset = 49
    value = (buf[offset] & 48) >> 4
    CCLFOTarget = value
    print("LFO Target: " + str(CCLFOTarget))

while True:
    try:
        with mido.open_input('monologue 1 KBD/KNOB 1') as inport:
            print("=====================================")
            print_full("Waiting for message... ")
            for msg in inport:                
                if msg.type == 'sysex' and len(msg.data) == 518:                    
                    print("OK")
                    analyse_sysex(msg.hex())
                    print("=====================================")
                    print_full("Waiting for message... ")
    except OSError:
        print("Device not connected.")
        break
            


