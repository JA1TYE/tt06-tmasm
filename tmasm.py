import argparse
import os
import yaml
import inst_parser
import symbol_mapper
import tokenizer
import macro_parser
import tmasm_utils

def main():
    # parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="input file name")
    parser.add_argument("-d", "--inst_def", help="specify instruction definition file")
    parser.add_argument("-m", "--macro_def", help="specify macro definition file")
    args = parser.parse_args()

    # load instruction definition  
    if args.inst_def is None:
        inst_def_file = "inst_defs.yaml"
    else:
        inst_def_file = args.inst_def
    with open(inst_def_file, 'r') as f:
        inst_def = yaml.safe_load(f)

    # load macro definition  
    if args.macro_def is None:
        macro_def_file = "macro_defs.yaml"
    else:
        macro_def_file = args.macro_def
    with open(macro_def_file, 'r') as f:
        macro_def = yaml.safe_load(f)

    # set output file name
    output_bin_filename = os.path.splitext(args.filename)[0] + '.bin'
    output_txt_filename = os.path.splitext(args.filename)[0] + '.txt'
    output_list_filename = os.path.splitext(args.filename)[0] + '.lst'

    # preprocessing
    mp = macro_parser.MacroParser(macro_def)
    tk = tokenizer.Tokenizer()
    sm = symbol_mapper.SymbolMapper()
    preprocessing_result = []
    with open(args.filename, 'r') as infile:
        for line in infile:
            tokens = tk.tokenize(line)
            if tmasm_utils.check_tilda_symbol(tokens):
                raise ValueError("Label/Variable name sould not start with tilda")
            tokens = mp.expand_macro(tokens)
            # make a symbol table
            for token_line in tokens:
                sm.make_symbol_table(token_line)
                preprocessing_result.append(token_line)
    print("--------PREPROCESSING RESULT--------")
    tmasm_utils.print_tokens(preprocessing_result)

    # get symbol table
    print("--------SYMBOL TABLE--------")
    symbol_table = sm.get_symbol_table()
    tmasm_utils.print_symbol_table(symbol_table)

    print("--------CONVERT TO BINARY--------")
    # resolve symbols and convert assembly to binary
    ip = inst_parser.InstParser(inst_def,symbol_table)
    binary = []
    for tokens in preprocessing_result:
        dat = ip.inst_to_bin(tokens)
        if dat is not None:
            binary.append(dat)
    
    # write binary to file
    with open(output_bin_filename, 'wb') as binfile , open(output_txt_filename, 'w') as txtfile:
        for dat in binary:
            binfile.write(dat.to_bytes(2, byteorder='big'))
            bin_str = format(dat >> 8, '08b') + "\n" + format(dat & 0xff, '08b') + "\n"
            txtfile.write(bin_str) 

if __name__ == '__main__':
    main()