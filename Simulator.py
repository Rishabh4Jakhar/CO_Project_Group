import sys
import os
reg_dic = {'pc': '0b00000000000000000000000000000000', '00000': '00000000000000000000000000000000', '00001': '00000000000000000000000000000000', '00010': '00000000000000000000000100000000', '00011': '00000000000000000000000000000000', '00100': '00000000000000000000000000000000', '00101': '00000000000000000000000000000000', '00110': '00000000000000000000000000000000', '00111': '00000000000000000000000000000000', 
    '01000': '00000000000000000000000000000000', '01001': '00000000000000000000000000000000', '01010': '00000000000000000000000000000000', '01011': '00000000000000000000000000000000', '01100': '00000000000000000000000000000000', '01101': '00000000000000000000000000000000', '01110': '00000000000000000000000000000000', '01111': '00000000000000000000000000000000', 
    '10000': '00000000000000000000000000000000', '10001': '00000000000000000000000000000000', '10010': '00000000000000000000000000000000', '10011': '00000000000000000000000000000000', '10100': '00000000000000000000000000000000', '10101': '00000000000000000000000000000000', '10110': '00000000000000000000000000000000', '10111': '00000000000000000000000000000000', 
    '11000': '00000000000000000000000000000000', '11001': '00000000000000000000000000000000', '11010': '00000000000000000000000000000000', '11011': '00000000000000000000000000000000', '11100': '00000000000000000000000000000000', '11101': '00000000000000000000000000000000', '11110': '00000000000000000000000000000000', '11111': '00000000000000000000000000000000'}


def sext(imm):
    if imm[0] == '0':
        while len(imm)<32 :
            imm = '0' + imm
    else: 
        while len(imm) < 32:
            imm = '1' + imm
    return imm

def dec_to_bin(decimal_num):
    decimal_num = int(decimal_num)
    num_bits = 32
    # Check if the number is within the representable range
    min_val = -(2**(num_bits - 1))
    max_val = (2**(num_bits - 1)) - 1
    if decimal_num < min_val or decimal_num > max_val:
        raise ValueError(f"The decimal number {decimal_num} is out of range for {num_bits}-bit two's complement representation.")
    
    # Convert the absolute value of the decimal number to binary
    binary_str = bin(abs(decimal_num))[2:].zfill(num_bits)

    # If the number is negative, apply two's complement
    if decimal_num < 0:
        # Invert the bits
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        # Add 1 to the inverted bits
        twos_complement = bin(int(inverted_bits, 2) + 1)[2:].zfill(num_bits)
        return twos_complement
    else:
        return binary_str
def sign_convo(imm):
    if imm[0] == '1':
        flipped_bits = ''.join('1' if bit == '0' else '0' for bit in imm)
        return -(int(flipped_bits, 2) + 1)  
    else:
        return int(imm, 2)

def beq(rs1, rs2, imm, pro_count):
    rs1 = sign_convo(rs1)
    rs2 = sign_convo(rs2)
    imm = sign_convo(imm)
    if rs1 == rs2:
        pro_count += imm                              
    else:
        pro_count += 4                                
    return pro_count

def bne(rs1, rs2, imm, pro_count):
    rs1 = sign_convo(rs1)
    rs2 = sign_convo(rs2)
    imm = sign_convo(imm)
    if rs1 != rs2:
        pro_count += imm                             
    else:
        pro_count += 4                                
    return pro_count

def bge(rs1, rs2, imm, pro_count):
    rs1 = sign_convo(rs1)
    rs2 = sign_convo(rs2)
    imm = sign_convo(imm)
    if rs1 >= rs2:
        pro_count += imm                              
    else:
        pro_count += 4                               
    return pro_count

def blt(rs1, rs2, imm, pro_count):
    rs1 = sign_convo(rs1)
    rs2 = sign_convo(rs2)
    imm = sign_convo(imm)
    if rs1 < rs2:
        pro_count += imm                              
    else:
        pro_count += 4                                                                   
    return pro_count


def B(i, pro_count):
    rev_in = i[::-1]
    
    imm = i[0] + rev_in[7] + i[1:7] + rev_in[8:12][::-1]
    imm = sext(imm)
    
    rs2 = rev_in[20:25][::-1]
    rs1 = rev_in[15:20][::-1]
    func3 = rev_in[12:15][::-1]
    if func3 == "000":
        pro_count = beq(reg_dic[rs1], reg_dic[rs2], imm, pro_count)
    elif func3 == "001":
        pro_count = bne(reg_dic[rs1], reg_dic[rs2], imm, pro_count)
    elif func3 == "100":
        pro_count = blt(reg_dic[rs1], reg_dic[rs2], imm, pro_count)
    elif func3 == "101":
        pro_count = bge(reg_dic[rs1], reg_dic[rs2], imm, pro_count)
    return pro_count                               


def add(rd, rs1, rs2, pro_count):
    reg_dic[rd] = dec_to_bin(int(rs1, 2) + int(rs2, 2))   
    return pro_count + 4                              


def sub(rd, rs1, rs2, pro_count):
    reg_dic[rd] = dec_to_bin(int(rs1, 2) - int(rs2, 2))   
    return pro_count + 4                             


def slt(rd, rs1, rs2, pro_count):
    if rs1 < rs2:
        reg_dic[rd] = dec_to_bin(1)
    return pro_count + 4                             

def sltu(rd, rs1, rs2, pro_count):
    if rs1 < rs2:
        reg_dic[rd] = dec_to_bin(1)
    return pro_count + 4                              


def sll(rd, rs1, rs2, pro_count):
    rs2 = rs2[-5:]
    reg_dic[rd] = dec_to_bin(int(rs1, 2) << int(rs2, 2))
    return pro_count + 4                             

def xor(rd, rs1, rs2, pro_count):
    reg_dic[rd] = dec_to_bin(rs1 ^ rs2)
    return pro_count + 4     

def srl(rd, rs1, rs2, pro_count):
    rs2 = rs2[-5:]                            
    reg_dic[rd] = dec_to_bin(int(rs1, 2) >> int(rs2, 2))
    return pro_count + 4                              


def or_inst(rd, rs1, rs2, pro_count):
    reg_dic[rd] = dec_to_bin(int(rs1,2) | int(rs2, 2))
    return pro_count + 4                              

def and_ins(rd, rs1, rs2, pro_count):
    reg_dic[rd] = dec_to_bin(int(rs1, 2) & int(rs2, 2))
    return pro_count + 4                              

def R(i, pro_count):
    rev_in = i[::-1]
    rd = rev_in[7:12][::-1]
    funct3 = rev_in[12:15][::-1]
    rs1 = rev_in[15:20][::-1]
    rs2 = rev_in[20:25][::-1]
    
    funct7 = i[:7]  
    if (funct3 == "000") and (funct7 == "0000000"):
        pro_count = add(rd, sign_convo(reg_dic[rs1]), sign_convo(reg_dic[rs2]), pro_count)
    elif (funct3 == "000") and (funct7 == "0100000"):
        pro_count = sub(rd, reg_dic[rs1], reg_dic[rs2], pro_count)
    elif (funct3 == "010") and (funct7 == "0000000"):
        pro_count = slt(rd, sign_convo(reg_dic[rs1]), sign_convo(reg_dic[rs2]), pro_count)
        
    elif (funct3 == "011") and (funct7 == "0000000"):
        pro_count = sltu(rd, sign_convo(reg_dic[rs1]), sign_convo(reg_dic[rs2]), pro_count)
    elif (funct3 == "100") and (funct7 == "0000000"):
        pro_count = xor(rd, reg_dic[rs1], reg_dic[rs2], pro_count)
    elif (funct3 == "001") and (funct7 == "0000000"):
        pro_count = sll(rd, reg_dic[rs1], reg_dic[rs2], pro_count)
    elif (funct3 == "101") and (funct7 == "0000000"):
        pro_count = srl(rd, reg_dic[rs1], reg_dic[rs2], pro_count)
    elif (funct3 == "110") and (funct7 == "0000000"):
        pro_count = or_inst(rd, reg_dic[rs1], reg_dic[rs2], pro_count)
    elif (funct3 == "111") and (funct7 == "0000000"):
        pro_count = and_ins(rd, reg_dic[rs1], reg_dic[rs2], pro_count)
    return pro_count

def lw(rd, rs1, imm, pro_count):        
    rs1 = f"0x{rs1:08X}"           
    immt = f"0x{imm:08X}"
    t= hex(int(rs1[2:], 16) + int(immt[2:], 16))
    t32 = f"0x{int(t, 16):08X}"

    reg_dic[rd] = mem[t32.lower()]             
    return pro_count + 4                              
def addi(rd, rs1, imm, pro_count):
    reg_dic[rd] = dec_to_bin(rs1 + imm)   
    return pro_count + 4                              

def jalr(rd, x6, imm, pro_count):
    reg_dic[rd] = dec_to_bin(pro_count + 4)      
    pro_count = dec_to_bin(x6 + imm)            
    pro_count = pro_count[:-1] + "0"
    pro_count = int(pro_count, 2)                        
    return pro_count 

def I(i, pro_count):
    imm = i[:12]
    imm = sext(imm)
    rd = i[-12:-7]
    rs1 = i[-20:-15]
    func3 = i[-15:-12]
    opcode = i[-7:]
    imm = sign_convo(imm)
    if func3 == "000" and (opcode == "1100111"):
        pro_count = jalr(rd, sign_convo(reg_dic[rs1]), imm, pro_count)    
    elif (func3 == "010") and (opcode == "0000011"):
        pro_count = lw(rd, sign_convo(reg_dic[rs1]), imm, pro_count)
    elif  (opcode == "0010011") and (func3 == "000"):
        pro_count = addi(rd, sign_convo(reg_dic[rs1]), imm, pro_count)
    return pro_count


def auipc(rd, imm, pro_count):
    reg_dic[rd] = dec_to_bin(imm+pro_count)
    return pro_count + 4 

def S_sw(i, pro_count, mem):
    rev_in = i[::-1]
    imm = i[:7]+i[20:25]    
    imm = sign_convo(sext(imm))
    rs1 = rev_in[15:20][::-1]
    rs1 = sign_convo(sext(reg_dic[rs1]))                         
    num = rs1+imm
    num = f"0x{num:08X}".lower()
    rs2 = rev_in[20:25][::-1]
    mem[num] = reg_dic[rs2]
    return pro_count + 4                                                          

def lui(rd, imm, pro_count):
    reg_dic[rd] = dec_to_bin(imm)   
    return pro_count + 4                            
                            

def U(i, pro_count):
    rev_in = i[::-1]
    opcode = i[-7:]    
    imm = rev_in[12:][::-1]
    imm =  imm + "000000000000"
    rd = rev_in[7:12][::-1]
    if opcode == "0110111":
        imm = sign_convo(imm)
        pro_count = lui(rd, imm, pro_count)
    elif opcode == "0010111":
        imm = sign_convo(imm)
        pro_count = auipc(rd, imm, pro_count)
    return pro_count

def J_jal(i, pro_count):
    rev_in = i[::-1]
    imm = i[0] + rev_in[12:20][::-1] + rev_in[20] + i[1:11]              
    imm = sign_convo(sext(imm))
    rd = rev_in[7:12][::-1]
    reg_dic[rd] = dec_to_bin(pro_count + 4)     
    pro_count = dec_to_bin(pro_count + imm)            
    pro_count = pro_count[:-1] + "0"
    pro_count = int(pro_count, 2)
    return pro_count                                                                           
def append_inst(i):
    l=[]
    for i in reg_dic.keys():
        if i=="pc":
            l.append(reg_dic[i])
        else:
            l.append('0b'+reg_dic[i])
    out_list.append(" ".join(l)) 


def sim():
    pro_count = 0
    while pro_count <= 252:
        inst = pc_dict[pro_count]
        op = inst[-7:]
        #00000001100000000000000011101111
        if inst == "00000000000000000000000001100011":
            append_inst(i)      
            break
        if op == "0110011":
            pro_count = R(inst, pro_count)
        elif op == "0000011" or op == "0010011" or op == "1100111":
            pro_count = I(inst, pro_count)
        elif op == "0100011":
            pro_count = S_sw(inst, pro_count, mem)
        elif op == "1100011":
            pro_count = B(inst, pro_count)
        elif op == "0010111" or op == "0110111":
            pro_count = U(inst, pro_count)
        elif op == "1101111":
            pro_count = J_jal(inst, pro_count)
        reg_dic["pc"] = "0b" + dec_to_bin(pro_count) 
        #print(pro_count, type(pro_count))
        append_inst(i)
mem = {}
mem_add = {}
for i in range(32):  
    address = f'0x{int(0x00010000 + i*4):08X}'.lower() 
    mem[address] = '0' * 32
mem_keys = list(mem.keys())
keys1 = list(reg_dic.keys())
keys1.remove('pc')
keys2 = list(mem.keys())
for key1, key2 in zip(keys1, keys2):
    mem_add[key1] = key2
input = sys.argv[1]
output = sys.argv[2]
if not os.path.exists(input):
    sys.exit("Input file path does not exist")
out_list = []
with open(input, "r") as input_file:
    if not input_file:
        sys.exit("Input file empty")
    x = input_file.readlines()
    pc_dict = {}
    pro_count = 0
    for line in x:
        pc_dict[pro_count] = line.strip("\n")
        pro_count += 4
sim()
with open(output, "w") as output_file:
    for line in out_list:
        output_file.write(line + "\n")
    for i in mem.keys():
        output_file.write(i + ":" + "0b" + mem[i] + "\n")

sys.exit()