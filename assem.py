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
    sub_parts = parts[1].split(",")
    # If conditions to be added for all the instructions
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
