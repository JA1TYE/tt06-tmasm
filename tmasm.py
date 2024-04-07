import argparse
import os
import yaml
import inst_parser
import symbol_mapper

def main():
    # parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="input file name")
    parser.add_argument("-d", "--inst_def", help="specify instruction definition file")
    parser.add_argument("-m", "--macro", help="specify macro definition file")
    args = parser.parse_args()

    # load instruction definition  
    if args.inst_def is None:
        inst_def_file = "inst_defs.yaml"
    else:
        inst_def_file = args["def"]
    with open(inst_def_file, 'r') as f:
        inst_def = yaml.safe_load(f)

    # set output file name
    output_bin_filename = os.path.splitext(args.filename)[0] + '.bin'
    output_txt_filename = os.path.splitext(args.filename)[0] + '.txt'
    output_list_filename = os.path.splitext(args.filename)[0] + '.lst'

    # preprocessing

    # make symbol table
    instruction_lines = []
    s_mapper = symbol_mapper.SymbolMapper(inst_def)
    with open(args.filename, 'r') as infile:
        for line in infile:
            ret = s_mapper.make_symbol_table(line)
            if ret is None:
                instruction_lines.append(line.strip())
    symbol_table = s_mapper.get_symbol_table()
    
    print(instruction_lines)

    # assemble
    i_parser = inst_parser.InstParser(inst_def,symbol_table)
    binary = []
    for line in instruction_lines:
        dat = i_parser.inst_to_bin(line)
        binary.append(dat)
    
    # write binary to file
    with open(output_bin_filename, 'wb') as binfile , open(output_txt_filename, 'w') as txtfile:
        for dat in binary:
            binfile.write(dat.to_bytes(2, byteorder='big'))
            bin_str = format(dat >> 8, '08b') + "\n" + format(dat & 0xff, '08b') + "\n"
            txtfile.write(bin_str) 

if __name__ == '__main__':
    main()