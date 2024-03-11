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

# Define the opcode dictionary
valid={"add":"011011","sub":"0110011","sll":"0110011","slt":"0110011","sltu":"0110011","xor":"0110011","srl":"0110011","or":"0110011"
       ,"and":"0110011","lw":"0000011","addi":"0010011","sltiu":"0010011","jalr":"1100111","sw":"0100011","beq":"1100011","bne":"1100011","blt":"1100011","bge":"1100011","bltu":"1100011","bgeu":"1100011"
      , "lui":"0110111","auipc":"0010111","jal":"1101111"}
# List of registers (useless)
regi=["zero","ra","sp","gp","tp","t0","t1","t2","s0","fp","a0","a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5","s6","s7","s8"
      ,"s9","s10","s11","t3","t4","t5","t6", "s1"]

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
        imm = format(imm & 0xFFF, "012b")  # Convert to 12-bit binary using 2's complement
    else:
        imm = format(imm, "012b")
    return imm + format(register_dict[rs1], "05b") + "010" + format(register_dict[rd], "05b") + "0000011"

def jalr(rd, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b")  # Convert to 12-bit binary using 2's complement
    else:
        imm = format(imm, "012b")    
    return imm + format(register_dict[rs1], "05b") + "000" + format(register_dict[rd], "05b") + "1100111"

def addi(rd, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b")  # Convert to 12-bit binary using 2's complement
    else:
        imm = format(imm, "012b")    
    return imm + format(register_dict[rs1], "05b") + "000" + format(register_dict[rd], "05b") + "0010011"

def sltiu(rd, rs1, imm):
    imm = int(imm)
    if imm < 0:
        imm = format(imm & 0xFFF, "012b")  # Convert to 12-bit binary using 2's complement
    else:
        imm = format(imm, "012b")    
    return imm + format(register_dict[rs1], "05b") + "011" + format(register_dict[rd], "05b") + "0010011"

# S-Type Instructions
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
    return imm_12 + imm_10_5 + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "100" + imm_4_1[::-1] + imm_11 + "1100011"

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
    return imm_12 + imm_10_5[::-1] + format(register_dict[rs2], "05b") + format(register_dict[rs1], "05b") + "110" + imm_4_1 + imm_11 + "1100011"

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
        imm = format(abs(int(imm)), "032b")
        #imm=imm[-32:-12]
        imm = imm.replace("0", "2").replace("1", "0").replace("2", "1")
        imm = bin(int(imm, 2) + 1)[2:]
        imm = imm[-32:-12]

        #print("#",imm)
        #imm = imm[-32:-12]
    else:
        imm = format(int(imm), "032b")
        imm = imm[-32:-12]
    return imm + format(register_dict[rd], "05b") + "0110111"

def auipc(rd, imm):
    if int(imm) < 0:
        imm = format(abs(int(imm)), "032b")
        #imm=imm[-32:-12]
        imm = imm.replace("0", "2").replace("1", "0").replace("2", "1")
        imm = bin(int(imm, 2) + 1)[2:]
        imm = imm[-32:-12]

        #print("#",imm)
        #imm = imm[-32:-12]
    else:
        imm = format(int(imm), "020b")
        imm = imm[-32:-12]
    return imm + format(register_dict[rd], "05b") + "0010111"

# J-Type Instructions
def jal(rd, imm):
    if int(imm) < 0:
        imm = format(int(imm) & 0xFFFFF, "020b")  # Convert to 20-bit binary
    else:
        imm = format(int(imm), "020b")
    imm = imm[::-1]
    #print("#", imm, "#")
    imm_20 = str(imm)[19]
    imm_10_1 = str(imm)[10:0:-1]
    imm_11 = str(imm)[10]
    imm_19_12 = str(imm)[12:20]
    return imm_20 + imm_10_1 + imm_11 + imm_19_12 + format(register_dict[rd], "05b") + "1101111"

#input_file = input()
#input_file = input_file.split("\n")
# Process each line of input

if len(sys.argv) < 3:
    sys.exit("Input file path and output file path are required")

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Open the input file
input_file = open(input_file_path, "r")

# Check if the input file is empty
if not input_file:
    sys.exit("Input file is empty")

# Process each line of input
output = []
total_lines = len(input_file.readlines())
input_file.seek(0)
line_number = 1
for line in input_file:

    line = line.strip()
    parts = line.split()
    parts[0] = parts[0].lower()
    sub_parts = parts[1].split(",")
    cont=False
    lt=[]
    label=False # No label present
    labels={}
    vt=0
    opcode=valid.get(parts[0])
    if parts[0]=="beq" and sub_parts[0]=="zero" and sub_parts[1]=="zero" and sub_parts[2]=="0":
        vt+=1
    if line_number == total_lines:
        if parts[0]!="beq" or sub_parts[0]!="zero" or sub_parts[1]!="zero" or sub_parts[2]!="0":
            #vt+=1
            print(" Virtual instruction not being used as last instruction at line",line_number)
            cont=True
        if vt == 0:
            print("Virtual instruction not present", line_number)
            

    for i in range(len(sub_parts)):
         if sub_parts[i].isalpha():
              lt.append(sub_parts[i])
         else:
              if '(' in sub_parts[i]:
                   sube=sub_parts[i].split("(")
                   sube=sube[1].split(")")
                   if sube[0].isalpha():
                        lt.append(sube[0])
              elif not sub_parts[i].isdigit():
                   lt.append(sub_parts[i])
              elif parts[0] in ["lw","addi","sltiu","jalr"]:
                   if int(sub_parts[i])>(2**12-1):
                        print("Illegal immediate",sub_parts[i],"at line",line_number)
                        cont=True
                        break
              elif parts[0] in ["sw"]:
                   sube=sub_parts[i].split("(")
                   if int(sube[0])>(2**12-1):
                        print("Illegal immediate",sub_parts[i],"at line",line_number)
                        cont=True
                        break
              elif parts[0] in ["beq","bne","blt","bge","bltu","bgeu"]:
                   if int(sub_parts[i])>(2**12-1):
                        print("Illegal immediate",sub_parts[i],"at line",line_number)
                        cont=True
                        break
              elif parts[0] in ["lui","auipc"]:
                   if int(sub_parts[i])>(2**32-1):
                        print("Illegal immediate",sub_parts[i],"at line",line_number)
                        cont=True
                        break
              elif parts[0] in ["jal"]:
                   if int(sub_parts[i])>(2**20-1):
                        print("Illegal immediate",sub_parts[i],"at line",line_number)
                        cont=True
                        break
    if cont == True:
        exit()            
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
        #lw t2,100(sp)
        output.append(lw(sub_parts[0], sub_parts[1].split("(")[1].replace(")", ""), sub_parts[1].split("(")[0]))
    elif parts[0] == "jalr":
        output.append(jalr(sub_parts[0], sub_parts[1], int(sub_parts[2])))
    elif parts[0] == "jal":
        output.append(jal(sub_parts[0], sub_parts[1]))
    else:
        # Assuming a label is present
        label = True
        labell = line.split(":")
        if " " in labell[0]:
            print(f"Error: Invalid label: {labell[0]} at line",line_number)
            exit()
        if labell[1][0] != " ":
            print(f"Error: Invalid label: {labell[0]} at line",line_number)
            exit()
        parts=labell[1].strip().split()
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
            #lw t2,100(sp)
            output.append(lw(sub_parts[0], sub_parts[1].split("(")[1].replace(")", ""), sub_parts[1].split("(")[0]))
        elif parts[0] == "jalr":
            output.append(jalr(sub_parts[0], sub_parts[1], int(sub_parts[2])))
        elif parts[0] == "jal":
            output.append(jal(sub_parts[0], sub_parts[1]))        
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