def canParseFromHex(s):
    try: 
        int(s, 16)
        return True
    except ValueError:
        return False

buf = """
 SYSX: F0 42 30 00 01 44 40 00 50 52 4F 47 49 6E 69 00 74 20
 SYSX: 50 72 6F 67 72 44 61 6D 00 00 00 00 7F 72 00 7F 00 00
 SYSX: 00 00 00 5D 00 00 10 10 69 33 00 02 00 25 32 00 0C 24
 SYSX: 00 20 38 22 06 66 00 7F 53 08 45 51 44 30 04 10 00 00
 SYSX: 00 36 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 SYSX: 00 00 00 00
"""
buf = [int(x, 16) for x in buf.split() if canParseFromHex(x)];
print(buf);


# Overdrive (10 bits)
# Byte 39     - bit 2
# Byte 39 + 2 - bits 1 - 7
# Byte 39 + 8 - bit 1
# Byte 39 + 9 - bit 7

driveFirstByteIndex = 39;
value = (buf[driveFirstByteIndex + 9] & 64) >>  6;
value = value | ((buf[driveFirstByteIndex + 8] & 1) << 1); 
value = value | ((buf[driveFirstByteIndex + 2] & 127) << 2)
value = value | ((buf[driveFirstByteIndex] & 2) << 8);
CCDrive = value;
print("Drive: " + str(value));

# VCO1 Wave (2 bits)
# Byte 39 - bit 3
# Byte 39 + 3 - bit 7

VCO1WaveOffset = 39;
value = (buf[VCO1WaveOffset + 3] & 64) >>  6;
value = value | ((buf[VCO1WaveOffset] & 4) >> 1); 
CCVCO1Wave = value;
print("VCO1 Waveform: " + str(CCVCO1Wave));


# VCO1 Shape (10 bits)
# Byte 24      - bit 4
# Byte 24 + 4  - bit 1-7
# Byte 24 + 19 - bit 3-4

VCO1ShapeOffset = 23;
value = (buf[VCO1ShapeOffset + 19] & 12) >>  2;
value = value | ((buf[VCO1ShapeOffset + 4] & 127) << 2); 
value = value | ((buf[VCO1ShapeOffset] & 8) << 6); 
CCVCO1Shape = value;
print("VCO1 Shape: " + str(CCVCO1Shape));

# VCO2 Octave (2 bits)
# Byte 43 - bit 5-6

VCO2OctaveOffset = 43;
value = (buf[VCO2OctaveOffset] & 48) >>  4;
CCVCO2Octave = value;
print("VCO2 Octave: " + str(CCVCO2Octave));

# VCO2 Wave (2 bits)
# Byte 39 - bit 4
# Byte 39 + 4 - bit 7

VCO2WaveOffset = 39;
value = (buf[VCO2WaveOffset + 4] & 64) >>  6;
value = value | ((buf[VCO2WaveOffset] & 8) >> 2); 
CCVCO2Wave = value;
print("VCO1 Waveform: " + str(CCVCO2Wave));

# Ring/Sync (2 bits)
# Byte 39 - bit 1-2

RingSyncOffset = 44;
value = (buf[RingSyncOffset] & 3);

CCRingSync = value;
print("Ring/Sync: " + str(CCRingSync));

# VCO2 Shape (10 bits)
# Byte 24      - bit 6
# Byte 24 + 6  - bit 1-7
# Byte 24 + 20 - bit 2-4

VCO2ShapeOffset = 23;
value = (buf[VCO2ShapeOffset + 20] & 12) >> 2;
value = value | ((buf[VCO2ShapeOffset + 6] & 127) << 2); 
value = value | ((buf[VCO2ShapeOffset] & 32) << 4); 
CCVCO2Shape = value;
print("VCO2 Shape: " + str(CCVCO2Shape));

# VCO2 Pitch (10 bits)
# Byte 24      - bit 5
# Byte 24 + 5  - bit 1-7
# Byte 24 + 20 - bit 1-2

VCO2PitchOffset = 23;
value = (buf[VCO2PitchOffset + 20] & 3);
value = value | ((buf[VCO2PitchOffset + 5] & 127) << 2); 
value = value | ((buf[VCO2PitchOffset] & 16) << 5); 
CCVCO2Pitch = value;
print("VCO2 Pitch: " + str(CCVCO2Pitch));

print(hex(buf[VCO2ShapeOffset]));

#rint(hex(buf[driveFirstByteIndex]));
#bytesbuf = bytes(buf);
#print(bytesbuf);
