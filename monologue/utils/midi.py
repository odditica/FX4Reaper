from misc import *
import mido


while True:
    msg_a = None
    msg_b = None    
    print("=====================================")
    print_full("Waiting for first message... ")
    seen = list()
    try:
        with mido.open_input('monologue 1 KBD/KNOB 1') as inport:
            for msg in inport:
                if (msg.type == 'control_change' and msg.control not in seen):                
                    print("CC(" + str(msg.control) + ") ", end='')
                    seen.append(msg.control)
                if (msg.type == 'program_change' and "PC" not in seen):                
                    print("PC ", end='')
                    seen.append("PC")
                if (msg.type == 'sysex'):
                    if (msg_a  == None):
                        msg_a = msg.data
                        print("OK")
                        print_full("Waiting for second message... ")
                        seen.clear()
                    else:
                        msg_b = msg.data
                        print("OK")
                        break
        print_full("Comparison: \n")            
        if (len(msg_a) != len(msg_b)):
            print_full("Message length mismatch.")
        else:
            diff_count = 0
            offset = -1
            print("---")
            for i in range(0, len(msg_a)):
                if (msg_a[i] != msg_b[i]):
                    if (offset == -1):
                        offset = i + 1
                        print("Byte %s" % (str(offset)))                    
                    else:
                        print("Byte %s (+%s)" % (str(i + 1), str(i + 1 - offset)))
                    
                    bin_a = list("{:08b}".format(msg_a[i]))
                    bin_b = list("{:08b}".format(msg_b[i]))
                    dec_or = (msg_a[i] ^ msg_b[i])
                    for j in range(0, len(bin_a)):
                        if (bin_a[j] == bin_b[j]):
                            bin_a[j] = 'x'
                            bin_b[j] = 'x'
                        else:
                            diff_count += 1                        
                    print("A:   " + ''.join(bin_a))
                    print("B:   " + ''.join(bin_b))
                    print("XOR: " + str(dec_or))
                    print("-")
            print("---")
            print(str(diff_count) + " differing bits in total.")
            pass
    except OSError:
        print("Device not connected.")
        break
            
