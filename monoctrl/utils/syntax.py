import re;
f = open("../monoctrl/monologue", 'r')
code = f.readlines()
indent_level = 0
for i in range(0, len(code)):
    for j in range(0, len(code[i])):
        if code[i][j] != ' ': break

    #code[i] = code[i][j:]
    #for j in range(0, indent_level):
    #    code[i] = "  " + code[i]
    for j in range(0, len(code[i])):
        if code[i][j] == '(': indent_level += 1
        if code[i][j] == ')': indent_level -= 1
    code[i] = code[i].replace("LFO", "Lfo")
    code[i] = code[i].replace("VCO", "Vco")
    code[i] = code[i].replace("PC", "Pc")
    code[i] = code[i].replace("CC", "Cc")
    code[i] = code[i].replace("EG", "Eg")
    code[i] = code[i].replace("MIDI", "Midi")
    code[i] = re.sub(r'([a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)',
                     r'\1_\2_\3_\4_\5_\6', code[i])
    code[i] = re.sub(r'([a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)', r'\1_\2_\3_\4_\5', code[i])
    code[i] = re.sub(r'([a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)', r'\1_\2_\3_\4', code[i])
    code[i] = re.sub(r'([a-z|0-9]+)([A-Z][a-z|0-9]+)([A-Z][a-z|0-9]+)', r'\1_\2_\3', code[i])
    code[i] = re.sub(r'([a-z|0-9]+)([A-Z][a-z|0-9]+)', r'\1_\2', code[i])

    code[i] = code[i].lower()
    #code[i] = re.sub('(?!^)([A-Z]+)', r'_\1', code[i]).lower()
    #code[i] = re.sub(r'[\s!(]?([a-z|0-9]+)([A-Z][a-z|0-9]+)[\s|(]', r'\1_\2'.lower(), code[i])

print("".join(code));
#print(code);