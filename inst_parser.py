import re

class InstParser:
    def __init__(self, inst_def,symbol_table):
        self.inst_def = inst_def
        self.symbol_table = symbol_table

    def convert_args(self, tokens,inst_def):
        # check argument types and convert them
        converted_args = []
        for i, arg in enumerate(tokens[1:]):
            if inst_def['args'][i] == 'Reg':
                if not arg.startswith('$') or \
                not arg[1:].isdigit() or \
                int(arg[1:]) < 0 or \
                int(arg[1:]) >= 8:
                    raise ValueError("Invalid register:" + str(arg))
                else:
                    converted_args.append(int(arg[1:]))
            elif inst_def['args'][i] == 'Imm':
                val = self.get_symbol(arg)
                if val is not None:
                    converted_args.append(val)
                elif not is_hex_byte(arg) and not is_decimal_byte(arg):
                    raise ValueError("Invalid immediate value:" + str(arg))
                else:
                    converted_args.append(int(arg, 0))
            elif inst_def['args'][i] == 'Flag':
                arg = arg.lower()
                if re.match(r'^[csvz]{1,4}$', arg) is None:
                    raise ValueError("Invalid flag:" + str(arg))
                else:
                    converted_args.append(str_to_flag(arg))
            elif inst_def['args'][i] == 'cond':
                if arg != "c":
                    raise ValueError("Invalid condition:" + str(arg))
                else:
                    converted_args.append("c")
            elif inst_def['args'][i] == 'inv':
                if arg != "i":
                    raise ValueError("Invalid inversion flag:" + str(arg))
                else:
                    converted_args.append("i")
            else:
                raise ValueError("Unknown argument type:" + str(arg))
        return converted_args

    def generate_bin(self,converted_args,inst_def):
        # generate binary instruction
        bin_inst = 0
        inst_type = inst_def['type']
        if inst_type == 'R':
            bin_inst |= 0x8000
            bin_inst |= converted_args[0] << 8
            bin_inst |= converted_args[1] << 5
            bin_inst |= inst_def["func"]
            if "c" in converted_args:
                bin_inst |= 1 << 13
        elif inst_type == 'I':
            bin_inst |= 0xc000
            bin_inst |= inst_def["imm_type"] << 11
            bin_inst |= converted_args[0] << 8
            bin_inst |= converted_args[1] & 0xff
            if "c" in converted_args:
                bin_inst |= 1 << 13             
        elif inst_type == 'J':
            bin_inst |= 0x4000
            bin_inst |= converted_args[0] << 8
            bin_inst |= converted_args[1] << 5
            if "c" in converted_args:
                bin_inst |= 1 << 13
        elif inst_type == 'F':
            if len(converted_args) == 0:
                bin_inst = 0
            else:
                bin_inst |= converted_args[0]
                bin_inst |= 1 << 11
                if "c" in converted_args:
                    bin_inst |= 1 << 13
                if "i" in converted_args:
                    bin_inst |= 1 << 8
        return bin_inst

    def inst_to_bin(self,inst):
        #toknize inst string
        inst = inst.replace(',', ' ')
        tokens = inst.split()
        mnemonic = tokens[0].lower()
        if mnemonic in self.inst_def:
            inst_def = self.inst_def[mnemonic]
            converted_args = self.convert_args(tokens, inst_def)
            bin_inst = self.generate_bin(converted_args, inst_def) 
        else:
            raise ValueError("Unknown instruction:" + str(tokens[0]))

        return bin_inst

    def get_symbol(self, arg):
        idx = arg.find('.')
        symbol = arg[:idx]
        byte_pos = arg[idx+1:].lower()
        if symbol not in self.symbol_table:
            return None
        if byte_pos not in ["lo", "hi"]:
            raise ValueError("Invalid byte position:" + byte_pos)
        symbol_addr = self.symbol_table[symbol]["symbol_addr"]
        if byte_pos == "lo":
            return symbol_addr & 0xff
        else:
            return (symbol_addr >> 8) & 0xff

# check if a string is a hexadecimal number
def is_hex_byte(c):
    return re.match(r'^0x[0-9a-fA-F]{1,2}$', c) is not None

def is_decimal_byte(c):
    return c >= -128 and c <= 255

def str_to_flag(s):
    flag_value = 0
    if "c" in s:
        flag_value |= 8
    if "s" in s:
        flag_value |= 4
    if "v" in s:
        flag_value |= 2
    if "z" in s:
        flag_value |= 1
    return flag_value
