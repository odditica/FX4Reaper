from enum import Enum
from misc import *
import mido

def can_parse_from_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

class MonoPatch:

    class VCO1Wave(Enum):
        SQUARE = 0
        TRIANGLE = 1
        SAW = 2

    class VCO2Wave(Enum):
        NOISE = 0
        TRIANGLE = 1
        SAW = 2

    class RingSync(Enum):
        RING = 0
        OFF = 1
        SYNC = 2

    class EGType(Enum):
        GATE = 0
        AGD = 1
        AD = 2

    class EGTarget(Enum):
        CUTOFF = 0
        PITCH2 = 1
        PITCH = 2

    class LFOWave(Enum):
        SQUARE = 0
        TRIANGLE = 1
        SAW = 2

    class LFOMode(Enum):
        ONESHOT = 0
        SLOW = 1
        FAST = 2

    class LFOTarget(Enum):
        CUTOFF = 0
        SHAPE = 1
        PITCH = 2

    def __init__(self):
        self.drive = 0
        self.vco1_wave = MonoPatch.VCO1Wave.SAW
        self.vco1_shape = 0
        self.vco2_octave = 0
        self.vco2_wave = MonoPatch.VCO2Wave.NOISE
        self.ring_sync = MonoPatch.RingSync.OFF
        self.vco2_shape = 0
        self.vco2_pitch = 0
        self.vco1_level = 1023
        self.vco2_level = 0
        self.filter_cutoff = 1024
        self.filter_resonance = 0
        self.eg_type = MonoPatch.EGType.AD
        self.eg_attack = 0
        self.eg_decay = 1024
        self.eg_intensity = 0
        self.eg_target = MonoPatch.EGTarget.CUTOFF
        self.lfo_wave = MonoPatch.LFOWave.SAW
        self.lfo_mode = MonoPatch.LFOMode.SLOW
        self.lfo_rate = 0
        self.lfo_intensity = 0
        self.lfo_target = MonoPatch.LFOTarget.SHAPE
        self.name = "Init Program"

        self.seq_bpm = 120

    def decode_sysex(self, buf):
        print(buf)

        buf = [int(x, 16) for x in buf.split() if can_parse_from_hex(x)]
        offset = 0
        if (buf[6] == 0x4C):
            offset += 14
        else:
            offset += 12

        # Name (12*8 bits)
        # Byte 12 - 22
        # Byte 24 - 25

        #offset = 12
        self.name = ""
        for i in range(0, 14):
            if (buf[offset + i] != 0 and i != 11):
                self.name += chr(buf[offset + i])



        # VCO1 Level (10 bits)
        # Byte 23      - bit 7
        # Byte 23 + 7  - bit 1-7
        # Byte 23 + 22 - bit 1-2

        offset += 11
        #offset = 23
        value = ((buf[offset] & 64) << 3)
        value = value | ((buf[offset + 7] & 127) << 2)
        value = value | (buf[offset + 22] & 3)
        self.vco1_level = value

        # VCO2 Shape (10 bits)
        # Byte 23      - bit 6
        # Byte 23 + 6  - bit 1-7
        # Byte 23 + 20 - bit 2-4

        #offset = 23
        value = ((buf[offset] & 32) << 4)
        value = value | ((buf[offset + 6] & 127) << 2)
        value = value | ((buf[offset + 20] & 12) >> 2)
        self.vco2_shape = value

        # VCO2 Pitch (10 bits)
        # Byte 23      - bit 5
        # Byte 23 + 5  - bit 1-7
        # Byte 23 + 20 - bit 1-2

        #offset = 23
        value = ((buf[offset] & 16) << 5)
        value = value | ((buf[offset + 5] & 127) << 2)
        value = value | (buf[offset + 20] & 3)
        self.vco2_pitch = value

        # VCO1 Shape (10 bits)
        # Byte 23      - bit 4
        # Byte 23 + 4  - bit 1-7
        # Byte 23 + 19 - bit 3-4

        #offset = 23
        value = ((buf[offset] & 8) << 6)
        value = value | ((buf[offset + 4] & 127) << 2)
        value = value | ((buf[offset + 19] & 12) >> 2)
        self.vco1_shape = value

        # LFO Rate (10 bits)
        # Byte 31      - bit 7
        # Byte 31 + 7  - bit 1-7
        # Byte 31 + 17 - bit 2-4

        offset += 8
        #offset = 31
        value = (buf[offset] & 64) << 3
        value = value | ((buf[offset + 7] & 127) << 2)
        value = value | ((buf[offset + 17] & 12) >> 2)
        self.lfo_rate = value

        # EG Intensity (10 bits)
        # Byte 31      - bit 6
        # Byte 31 + 6  - bit 1-7
        # Byte 31 + 17 - bit 1-2
        # (hold shift for negative values)

        #offset = 31
        value = (buf[offset] & 32) << 4
        value = value | ((buf[offset + 6] & 127) << 2)
        value = value | (buf[offset + 17] & 3)
        self.eg_intensity = value - 512

        # EG Decay (10 bits)
        # Byte 31      - bit 5
        # Byte 31 + 5  - bit 1-7
        # Byte 31 + 15 - bit 5-6

        #offset = 31
        value = (buf[offset] & 16) << 5
        value = value | ((buf[offset + 5] & 127) << 2)
        value = value | ((buf[offset + 15] & 48) >> 4)
        self.eg_decay = value

        # EG Attack (10 bits)
        # Byte 31      - bit 4
        # Byte 31 + 4  - bit 1-7
        # Byte 31 + 15 - bit 2-4

        #offset = 31
        value = (buf[offset] & 8) << 6
        value = value | ((buf[offset + 4] & 127) << 2)
        value = value | ((buf[offset + 15] & 12) >> 2)
        self.eg_attack = value

        # Filter Resonance (10 bits)
        # Byte 31      - bit 3
        # Byte 31 + 3  - bit 1-7
        # Byte 31 + 8  - bit 6
        # Byte 31 + 14 - bit 7

        #offset = 31
        value = (buf[offset] & 4) << 7
        value = value | ((buf[offset + 3] & 127) << 2)
        value = value | ((buf[offset + 8] & 32) >> 4)
        value = value | ((buf[offset + 14] & 64) >> 6)
        self.filter_resonance = value

        # Filter Cutoff (10 bits)
        # Byte 31      - bit 2
        # Byte 31 + 2  - bit 1-7
        # Byte 31 + 14 - bit 5-6

        #offset = 31
        value = (buf[offset] & 2) << 8
        value = value | ((buf[offset + 2] & 127) << 2)
        value = value | ((buf[offset + 14] & 48) >> 4)
        self.filter_cutoff = value

        # VCO2 Level (10 bits)
        # Byte 31      - bit 1
        # Byte 31 + 1  - bit 1-7
        # Byte 31 + 14 - bit 2-4

        #offset = 31
        value = ((buf[offset] & 1) << 9)
        value = value | ((buf[offset + 1] & 127) << 2)
        value = value | (buf[offset + 14] & 12) >> 2
        self.vco2_level = value

        # EG Target (2 bits)
        # Byte 39      - bit 7
        # Byte 39 + 7  - bit 7

        offset += 8
        #offset = 39
        value = (buf[offset] & 64) >> 5
        value = value | ((buf[offset + 7] & 64) >> 6)
        self.eg_target = value

        # VCO2 Wave (2 bits)
        # Byte 39 - bit 4
        # Byte 39 + 4 - bit 7

        #offset = 39
        value = ((buf[offset] & 8) >> 2)
        value = value | ((buf[offset + 4] & 64) >> 6)
        self.vco2_wave = value

        # VCO1 Wave (2 bits)
        # Byte 39 - bit 3
        # Byte 39 + 3 - bit 7

        #offset = 39
        value = ((buf[offset] & 4) >> 1)
        value = value | ((buf[offset + 3] & 64) >> 6)
        self.vco1_wave = value

        # Drive (10 bits)
        # Byte 39     - bit 2
        # Byte 39 + 2 - bits 1 - 7
        # Byte 39 + 8 - bit 1
        # Byte 39 + 9 - bit 7

        #offset = 39
        value = ((buf[offset] & 2) << 8)
        value = value | ((buf[offset + 2] & 127) << 2)
        value = value | ((buf[offset + 8] & 1) << 1)
        value = value | ((buf[offset + 9] & 64) >> 6)
        self.drive = value


        # LFO Intensity (10 bits)
        # Byte 39      - bit 1
        # Byte 39 + 1  - bit 1-7
        # Byte 39 + 9  - bit 6-7
        # (hold shift for negative values)

        #offset = 39
        value = (buf[offset] & 1) << 9
        value = value | ((buf[offset + 1] & 127) << 2)
        value = value | ((buf[offset + 9] & 48) >> 4)
        self.lfo_intensity = value - 512

        # VCO2 Octave (2 bits)
        # Byte 43 - bit 5-6

        offset += 4
        #offset = 43
        value = (buf[offset] & 48) >> 4
        self.vco2_octave = value

        # Ring/Sync (2 bits)
        # Byte 44 - bit 1-2

        offset += 1
        #offset = 44
        value = (buf[offset] & 3)
        self.ring_sync = value

        # EG Type (2 bits)
        # Byte 46       - bit 1-2

        offset += 2
        #offset = 46
        value = (buf[offset] & 3)
        self.eg_type = value

        # LFO Target (2 bits)
        # Byte 49      - bit 5-6

        offset += 3
        #offset = 49
        value = (buf[offset] & 48) >> 4
        self.lfo_target = value


        # LFO Mode (2 bits)
        # Byte 49      - bit 2-4

        #offset = 49
        value = (buf[offset] & 12) >> 2
        self.lfo_mode = value

        # LFO Wave (2 bits)
        # Byte 49      - bit 1-2

        #offset = 49
        value = (buf[offset] & 3)
        self.lfo_wave = value

        #68 ---xxxxx
        #63 ----x---
        #67 -xxxxxxx

        # Tempo (13 bits)
        # Byte 63      - bit 7
        # Byte 67      - bit 1-7
        # Byte 68      - bit 2-4

        value = (buf[68] & 31) << 8
        value = value | ((buf[63] & 8) << 4)
        value = value | ((buf[67] & 127))
        value /= 10
        self.seq_bpm = value

    def __str__(self):
        #i love python
        return (
        """
Name: %s
============
Drive: %d
VCO1 Waveform: %s
VCO1 Shape: %s
VCO2 Octave: %s
VCO1 Waveform: %s
Ring/Sync: %s
VCO2 Shape: %s
VCO2 Pitch: %d
VCO1 Level: %d
VCO2 Level: %d
Filter cutoff: %d
Filter resonance: %d
EG Type: %s
EG Attack: %d 
EG Decay: %d
EG Intensity: %d
EG Target: %s
LFO Wave: %s
LFO Mode: %s
LFO Rate: %d
LFO Intensity: %d
LFO Target: %s

Tempo: %d BPM
        """
        ) % (
            self.name,
            self.drive,
            MonoPatch.VCO1Wave(self.vco1_wave).name,
            self.vco1_shape,
            str(2 << (3 - self.vco2_octave)) + "'",
            MonoPatch.VCO2Wave(self.vco2_wave).name,
            MonoPatch.RingSync(self.ring_sync).name,
            self.vco2_shape,
            self.vco2_pitch,
            self.vco1_level,
            self.vco2_level,
            self.filter_cutoff,
            self.filter_resonance,
            MonoPatch.EGType(self.eg_type).name,
            self.eg_attack,
            self.eg_decay,
            self.eg_intensity,
            MonoPatch.EGTarget(self.eg_target).name,
            MonoPatch.LFOWave(self.lfo_wave).name,
            MonoPatch.LFOMode(self.lfo_mode).name,
            self.lfo_rate,
            self.lfo_intensity,
            MonoPatch.LFOTarget(self.lfo_target).name,
            self.seq_bpm
        )

program = MonoPatch()

program.decode_sysex(
     """
     f0
     42 30 00 01 44 4C 00 00 00 50 52 4F 47 49 6E 69 00 74 20 50 72 6F 67 72 54 61 6D 00 00 00 00 7F 72 00 7F 00 00 00 00 00 5D 00 00 10 10 69 33 00 02 00 25 32 00 0C 24 00 20 38 22 06 66 00 7F 53 08 45 51 44 30 04 10 00 00 00 36 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   
     f7
     """
)
print(program)

program.decode_sysex(
     """
     f0
     42 30 00 01 44 40 00 50 52  4F 47 49 6E 69 00 74 20 50 72 6F 67 72 54 61 6D 00 00 00 00 7F 72 00 7F 00 00 00 00 00 5D 00 00 10 10 69 33 00 02 00 25 32 00 0C 24 00 20 38 22 06 66 00 7F 53 08 45 51 44 30 04 10 00 00 00 36 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
     f7
     """
)
print(program)
while True:
    try:
        with mido.open_input('monologue 1 KBD/KNOB 1') as inport:
            try:
                with mido.open_output('monologue 1 SOUND 2') as outport:
                    outport.reset()
                    print("=====================================")
                    print_full("Waiting... \n")
                    for msg in inport:
                        if msg.type == 'sysex':
                            if  len(msg.data) >= 518:
                                print("Getting ")
                                program.decode_sysex(msg.hex())
                                print(program)
                                print("=====================================")
                                print_full("Waiting for message... ")
                            else:
                                if msg.hex() == 'F0 7E 00 06 02 42 44 01 00 00 01 00 0E 00 F7':
                                    temp = bytearray.fromhex('42 30 00 01 44 1C 00 00');
                                    temp[6] = 83;
                                    outport.send(mido.Message('sysex', data=temp))
                        if msg.type == 'note_on' and msg.note == 60:

                            print_full("Sending program dump request..\n")
                            outport.send(mido.Message('sysex', data=bytearray.fromhex('7E 7F 06 01')))



            except OSError:
                print("Output device not connected.")
                break
    except OSError:
        print("Input device not connected.")
        break


            


