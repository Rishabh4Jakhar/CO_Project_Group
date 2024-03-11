import sys
import os

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


# R-Type Instructions
def add(rd, rs1, rs2):
    return "0000000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "000" + format(register_dict[rd], "05b") + "0110011"

def sub(rd, rs1, rs2):
    return "0100000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "000" + format(register_dict[rd], "05b") + "0110011"

def sll(rd, rs1, rs2):
    return "0000000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "001" + format(register_dict[rd], "05b") + "0110011"

def slt(rd, rs1, rs2):
    return "0000000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "010" + format(register_dict[rd], "05b") + "0110011"

def sltu(rd, rs1, rs2):
    return "0000000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "011" + format(register_dict[rd], "05b") + "0110011"

def xor(rd, rs1, rs2):
    return "0000000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "100" + format(register_dict[rd], "05b") + "0110011"

def srl(rd, rs1, rs2):
    return "0000000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "101" + format(register_dict[rd], "05b") + "0110011"

def sra(rd, rs1, rs2):
    return "0100000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "101" + format(register_dict[rd], "05b") + "0110011"

def or_(rd, rs1, rs2):
    return "0000000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "110" + format(register_dict[rd], "05b") + "0110011"

def and_(rd, rs1, rs2):
    return "0000000" + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "111" + format(register_dict[rd], "05b") + "0110011"

# I-Type Instructions
def lw(rd, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b")  
    else:
        imm = format(imm, "012b")
    return imm + format(register_dict[rs1], "05b") + "010" + format(register_dict[rd], "05b") + "0000011"

def jalr(rd, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b")
    else:
        imm = format(imm, "012b")    
    return imm + format(register_dict[rs1], "05b") + "000" + format(register_dict[rd], "05b") + "1100111"

def addi(rd, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b") 
    else:
        imm = format(imm, "012b")    
    return imm + format(register_dict[rs1], "05b") + "000" + format(register_dict[rd], "05b") + "0010011"

def sltiu(rd, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b") 
    else:
        imm = format(imm, "012b")    
    return imm + format(register_dict[rs1], "05b") + "011" + format(register_dict[rd], "05b") + "0010011"

# S-Type Instructions
def sw(rs2, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b") 
    else:
        imm = format(imm, "012b")
    imm_4_0 = str(imm)[7:12] 
    imm_11_5 = str(imm)[0:7]
    return imm_11_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "010" + imm_4_0 + "0100011"

# B-Type Instructions
def beq(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b") 
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
        imm = format(imm & 0x1FFF, "013b")
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
        imm = format(imm & 0x1FFF, "013b")
    else:
        imm = format(imm, "013b")
    imm = imm[::-1]
    imm_4_1 = str(imm)[1:5]
    imm_11 = str(imm)[11]
    imm_10_5 = str(imm)[5:11]
    imm_12 = str(imm)[12]
    return imm_12 + imm_10_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "100" + imm_4_1[::-1] + imm_11 + "1100011"

def bge(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b")
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
        imm = format(imm & 0x1FFF, "013b")
    else:
        imm = format(imm, "013b")
    imm = imm[::-1]
    imm_4_1 = str(imm)[1:5]
    imm_11 = str(imm)[11]
    imm_10_5 = str(imm)[5:11]
    imm_12 = str(imm)[12]
    return imm_12 + imm_10_5[::-1] + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "110" + imm_4_1 + imm_11 + "1100011"

def bgeu(rs1, rs2, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0x1FFF, "013b")
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
        imm = format(abs(int(imm)), "032b")
        imm = imm.replace("0", "2").replace("1", "0").replace("2", "1")
        imm = bin(int(imm, 2) + 1)[2:]
        imm = imm[-32:-12]
    else:
        imm = format(int(imm), "032b")
        imm = imm[-32:-12]
    return imm + format(register_dict[rd], "05b") + "0110111"

def auipc(rd, imm):
    if int(imm) < 0:
        imm = format(abs(int(imm)), "032b")
        imm = imm.replace("0", "2").replace("1", "0").replace("2", "1")
        imm = bin(int(imm, 2) + 1)[2:]
        imm = imm[-32:-12]
    else:
        imm = format(int(imm), "020b")
        imm = imm[-32:-12]
    return imm + format(register_dict[rd], "05b") + "0010111"

# J-Type Instructions
def jal(rd, imm):
    if int(imm) < 0:
        imm = format(int(imm) & 0xFFFFF, "020b")
    else:
        imm = format(int(imm), "020b")
    imm = imm[::-1]
    imm_20 = str(imm)[19]
    imm_10_1 = str(imm)[10:0:-1]
    imm_11 = str(imm)[10]
    imm_19_12 = str(imm)[12:20]
    return imm_20 + imm_10_1 + imm_11 + imm_19_12 + format(register_dict[rd], "05b") + "1101111"
if len(sys.argv) < 3:
    sys.exit("Input file path and output file path are required")

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

if not os.path.exists(input_file_path):
    sys.exit("Input file does not exist")

input_file = open(input_file_path, "r")

if not input_file:
    sys.exit("Input file is empty")

output = []
line_number = 1
for line in input_file:
    line = line.strip()
    parts = line.split()
    parts[0] = parts[0].lower()
    sub_parts = parts[1].split(",")
    if parts[0] == "add":
        output.append(add(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "sub":
        output.append(sub(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "sll":
        output.append(sll(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "slt":
        output.append(slt(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "sltu":
        output.append(sltu(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "xor":
        output.append(xor(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "srl":
        output.append(srl(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "sra":
        output.append(sra(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "or":
        output.append(or_(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "and":
        output.append(and_(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "addi":
        output.append(addi(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "sltiu":
        output.append(sltiu(sub_parts[0], sub_parts[1], sub_parts[2]))
    elif parts[0] == "sw":
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
    elif parts[0] == "lw":
        output.append(lw(sub_parts[0], sub_parts[1].split("(")[1].replace(")", ""), sub_parts[1].split("(")[0]))
    elif parts[0] == "jalr":
        output.append(jalr(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "jal":
        output.append(jal(sub_parts[0], sub_parts[1]))
    
    line_number += 1

input_file.close()

output_file = open(output_file_path, "w")
for line in output:
    output_file.write(line + "\n")

output_file.close()

sys.exit()
