import sys
import os

# Define the register dictionary
register_dict = {
    "zero": 0,
    "ra": 1,
    "sp": 2,
    "gp": 3,
    "tp": 4,
    "t0": 5,
    "t1": 6,
    "t2": 7,
    "s0": 8,
    "s1": 9,
    "a0": 10,
    "a1": 11,
    "a2": 12,
    "a3": 13,
    "a4": 14,
    "a5": 15,
    "a6": 16,
    "a7": 17,
    "s2": 18,
    "s3": 19,
    "s4": 20,
    "s5": 21,
    "s6": 22,
    "s7": 23,
    "s8": 24,
    "s9": 25,
    "s10": 26,
    "s11": 27,
    "t3": 28,
    "t4": 29,
    "t5": 30,
    "t6": 31
}



# SW: imm[11:5] rs2 rs1 010 imm[4:0] 0100011

def sw(rs2, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b")  # Convert to 12-bit binary using 2's complement
    else:
        imm = format(imm, "012b")
    #imm = format(int(imm), "012b")
    imm_4_0 = str(imm)[7:12]  # Extract bits 11:7 from imm
    imm_11_5 = str(imm)[0:7]  # Extract bits 6:0 from imm
    return imm_11_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "010" + imm_4_0 + "0100011"

# B-Type Instructions
# beq: imm[12] imm[10:5] rs2 rs1 000 imm[4:1] imm[11] 1100011

def beq(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b")  # Convert to 13-bit binary using 2's complement
    else:
        imm = format(imm, "013b")
    imm = imm[::-1]
    imm_4_1 = str(imm)[1:5]
    imm_11 = str(imm)[11]
    imm_10_5 = str(imm)[5:11]
    imm_12 = str(imm)[12]
    return imm_12 + imm_10_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "000" + imm_4_1 + imm_11 + "1100011"

def bne(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b")  # Convert to 13-bit binary using 2's complement
    else:
        imm = format(imm, "013b")
    imm = imm[::-1]
    imm_4_1 = str(imm)[1:5]
    imm_11 = str(imm)[11]
    imm_10_5 = str(imm)[5:11]
    imm_12 = str(imm)[12]
    return imm_12 + imm_10_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "001" + imm_4_1 + imm_11 + "1100011"

def blt(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b")  # Convert to 13-bit binary using 2's complement
    else:
        imm = format(imm, "013b")
    imm = imm[::-1]
    imm_4_1 = str(imm)[1:5]
    imm_11 = str(imm)[11]
    imm_10_5 = str(imm)[5:11]
    imm_12 = str(imm)[12]
    return imm_12 + imm_10_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "100" + imm_4_1 + imm_11 + "1100011"

def bge(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b")  # Convert to 13-bit binary using 2's complement
    else:
        imm = format(imm, "013b")
    imm = imm[::-1]
    imm_4_1 = str(imm)[1:5]
    imm_11 = str(imm)[11]
    imm_10_5 = str(imm)[5:11]
    imm_12 = str(imm)[12]
    return imm_12 + imm_10_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "101" + imm_4_1 + imm_11 + "1100011"

def bltu(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b")  # Convert to 13-bit binary using 2's complement
    else:
        imm = format(imm, "013b")
    imm = imm[::-1]
    imm_4_1 = str(imm)[1:5]
    imm_11 = str(imm)[11]
    imm_10_5 = str(imm)[5:11]
    imm_12 = str(imm)[12]
    return imm_12 + imm_10_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "110" + imm_4_1 + imm_11 + "1100011"

def bgeu(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b")  # Convert to 13-bit binary using 2's complement
    else:
        imm = format(imm, "013b")
    imm = imm[::-1]
    imm_4_1 = str(imm)[1:5]
    imm_11 = str(imm)[11]
    imm_10_5 = str(imm)[5:11]
    imm_12 = str(imm)[12]
    return imm_12 + imm_10_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "111" + imm_4_1 + imm_11 + "1100011"
# U-Type Instructions
def lui(rd, imm):
    if int(imm) < 0:
        imm = format(int(imm) & 0xFFFFF, "020b")  # Convert to 20-bit binary
    else:
        imm = format(int(imm), "020b")
        imm = imm[:8]+"0"*12
    #imm = imm[::-1]
    return imm + format(register_dict[rd], "05b") + "0110111"

def auipc(rd, imm):
    if int(imm) < 0:
        imm = format(int(imm) & 0xFFFFF, "020b")  # Convert to 20-bit binary
    else:
        imm = format(int(imm), "020b")
        imm = imm[:8]+"0"*12
    return imm + format(register_dict[rd], "05b") + "0010111"


# Read input from file
#input_file = sys.stdin.readlines()
#input_file = input()
#input_file = input_file.split("\n")
# Process each line of input

# Check if the input file path is provided
if len(sys.argv) < 3:
    sys.exit("Input file path and output file path are required")

# Get the input file path and output file path from command line arguments
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Check if the input file exists
if not os.path.exists(input_file_path):
    sys.exit("Input file does not exist")

# Open the input file
input_file = open(input_file_path, "r")

# Check if the input file is empty
if not input_file:
    sys.exit("Input file is empty")
# Process each line of input
output = []
line_number = 1
for line in input_file:
    line = line.strip()
    parts = line.split()
    parts[0] = parts[0].lower()
    sub_parts = parts[1].split(",")
    
    
    if parts[0] == "sw":
        output.append(sw(sub_parts[0], sub_parts[1].split("(")[1].replace(")", ""), sub_parts[1].split("(")[0]))
    elif parts[0] == "beq":
        output.append(beq(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "bne":
        output.append(bne(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "blt":
        output.append(blt(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "bge":
        output.append(bge(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "bltu":
        output.append(bltu(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "bgeu":
        output.append(bgeu(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "lui":
        output.append(lui(sub_parts[0], int(sub_parts[1])))
    elif parts[0] == "auipc":
        output.append(auipc(sub_parts[0], int(sub_parts[1])))
   
    line_number += 1

# Close the input file
input_file.close()

# Write output to the output file
output_file = open(output_file_path, "w")
for line in output:
    output_file.write(line + "\n")

# Close the output file
output_file.close()

# Exit the program
sys.exit()
