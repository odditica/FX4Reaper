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

    # Overdrive (10 bits)
    # Byte 39     - bit 2
    # Byte 39 + 2 - bits 1 - 7
    # Byte 39 + 8 - bit 1
    # Byte 39 + 9 - bit 7


    driveFirstByteIndex = 39
    value = (buf[driveFirstByteIndex + 9] & 64) >>  6
    value = value | ((buf[driveFirstByteIndex + 8] & 1) << 1) 
    value = value | ((buf[driveFirstByteIndex + 2] & 127) << 2)
    value = value | ((buf[driveFirstByteIndex] & 2) << 8)
    CCDrive = value
    print("Drive: " + str(value))

    # VCO1 Wave (2 bits)
    # Byte 39 - bit 3
    # Byte 39 + 3 - bit 7

    VCO1WaveOffset = 39
    value = (buf[VCO1WaveOffset + 3] & 64) >>  6
    value = value | ((buf[VCO1WaveOffset] & 4) >> 1) 
    CCVCO1Wave = value
    print("VCO1 Waveform: " + str(CCVCO1Wave))


    # VCO1 Shape (10 bits)
    # Byte 24      - bit 4
    # Byte 24 + 4  - bit 1-7
    # Byte 24 + 19 - bit 3-4

    VCO1ShapeOffset = 23
    value = (buf[VCO1ShapeOffset + 19] & 12) >>  2
    value = value | ((buf[VCO1ShapeOffset + 4] & 127) << 2) 
    value = value | ((buf[VCO1ShapeOffset] & 8) << 6) 
    CCVCO1Shape = value
    print("VCO1 Shape: " + str(CCVCO1Shape))

    # VCO2 Octave (2 bits)
    # Byte 43 - bit 5-6

    VCO2OctaveOffset = 43
    value = (buf[VCO2OctaveOffset] & 48) >>  4
    CCVCO2Octave = value
    print("VCO2 Octave: " + str(CCVCO2Octave))

    # VCO2 Wave (2 bits)
    # Byte 39 - bit 4
    # Byte 39 + 4 - bit 7

    VCO2WaveOffset = 39
    value = (buf[VCO2WaveOffset + 4] & 64) >>  6
    value = value | ((buf[VCO2WaveOffset] & 8) >> 2) 
    CCVCO2Wave = value
    print("VCO1 Waveform: " + str(CCVCO2Wave))

    # Ring/Sync (2 bits)
    # Byte 39 - bit 1-2

    RingSyncOffset = 44
    value = (buf[RingSyncOffset] & 3)

    CCRingSync = value
    print("Ring/Sync: " + str(CCRingSync))

    # VCO2 Shape (10 bits)
    # Byte 24      - bit 6
    # Byte 24 + 6  - bit 1-7
    # Byte 24 + 20 - bit 2-4

    VCO2ShapeOffset = 23
    value = (buf[VCO2ShapeOffset + 20] & 12) >> 2
    value = value | ((buf[VCO2ShapeOffset + 6] & 127) << 2) 
    value = value | ((buf[VCO2ShapeOffset] & 32) << 4) 
    CCVCO2Shape = value
    print("VCO2 Shape: " + str(CCVCO2Shape))

    # VCO2 Pitch (10 bits)
    # Byte 24      - bit 5
    # Byte 24 + 5  - bit 1-7
    # Byte 24 + 20 - bit 1-2

    VCO2PitchOffset = 23
    value = (buf[VCO2PitchOffset + 20] & 3)
    value = value | ((buf[VCO2PitchOffset + 5] & 127) << 2) 
    value = value | ((buf[VCO2PitchOffset] & 16) << 5) 
    CCVCO2Pitch = value
    print("VCO2 Pitch: " + str(CCVCO2Pitch))

    # VCO1 Level (10 bits)
    # Byte 23      - bit 7
    # Byte 23 + 7  - bit 1-7
    # Byte 23 + 22 - bit 1-2

    VCO1LevelOffset = 23
    value = (buf[VCO1LevelOffset + 22] & 3)
    value = value | ((buf[VCO1LevelOffset + 7] & 127) << 2) 
    value = value | ((buf[VCO1LevelOffset] & 64) << 3) 
    CCVCO1Level = value
    print("VCO1 Level: " + str(CCVCO1Level))
    
    # VCO2 Level (10 bits)
    # Byte 31      - bit 1
    # Byte 31 + 1  - bit 1-7
    # Byte 31 + 14 - bit 2-4

    VCO2LevelOffset = 31    
    value = ((buf[VCO2LevelOffset] & 1) << 9) 
    value = value | ((buf[VCO2LevelOffset + 1] & 127) << 2) 
    value = value | (buf[VCO2LevelOffset + 14] & 12) >> 2
    CCVCO2Level = value
    print("VCO2 Level: " + str(CCVCO2Level))


    # Filter Cutoff (10 bits)
    # Byte 31      - bit 2
    # Byte 31 + 2  - bit 1-7
    # Byte 31 + 14 - bit 5-6

    FilterCutoff = 31
    value = (buf[FilterCutoff] & 2) << 8
    value = value | ((buf[FilterCutoff + 2] & 127) << 2) 
    value = value | ((buf[FilterCutoff + 14] & 48) >> 4) 
    CCFilterCutoff = value
    print("Filter cutoff: " + str(CCFilterCutoff))

    print(hex(buf[VCO2ShapeOffset]))

    #rint(hex(buf[driveFirstByteIndex]))
    #bytesbuf = bytes(buf)
    #print(bytesbuf)


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
            


