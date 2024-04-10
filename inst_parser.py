import re
import tmasm_utils

class InstParser:
    def __init__(self, inst_def,symbol_table):
        self.symbol_table = symbol_table
        self.inst_table = tmasm_utils.make_mnemonic_table(inst_def)

    def inst_to_bin(self,tokens):
        # skip if the line is not instruction
        if tokens[0]["type"] != "mnemonic":
            return None
        else:
            # resolve symbols first
            resolved_tokens = self.resolve_symbol(tokens)
            # check if the instruction is valid and get the definition
            mnemonic = resolved_tokens[0]["token"]
            definition = tmasm_utils.search_definition(resolved_tokens,self.inst_table)
            if definition is None:
                raise ValueError("Invalid instruction:" + str(resolved_tokens))
            # generate binary instruction
            print(resolved_tokens)
            bin_inst = self.generate_bin(resolved_tokens,definition)
            return bin_inst

    # resolve symbols in the instruction
    def resolve_symbol(self,tokens):
        ret_tokens = []
        for token in tokens:
            if token["type"] == "symbol":
                symbol = token["token"]
                if symbol not in self.symbol_table:
                    raise ValueError("Unknown symbol:" + symbol)
                else:
                    raise ValueError("Symbol without .lo/.hi suffix is not allowed in operand:" + symbol)
            elif token["type"] == "symbol_hi":
                symbol = token["token"]
                if symbol not in self.symbol_table:
                    raise ValueError("Unknown symbol:" + symbol)
                addr = (self.symbol_table[symbol]["symbol_addr"] >> 8) & 0xff
                new_token = {"type":"imm","token":addr}
                ret_tokens.append(new_token)
            elif token["type"] == "symbol_lo":
                symbol = token["token"]
                if symbol not in self.symbol_table:
                    raise ValueError("Unknown symbol:" + symbol)
                addr = self.symbol_table[symbol]["symbol_addr"] & 0xff
                new_token = {"type":"imm","token":addr}
                ret_tokens.append(new_token)
            else:
                ret_tokens.append(token)
        return ret_tokens

    def generate_bin(self,tokens,inst_def):
        # generate binary instruction
        bin_inst = 0
        inst_type = inst_def['type']
        args = tmasm_utils.get_arg_tokens(tokens)
        if inst_type == 'R':
            bin_inst |= 0x8000
            bin_inst |= args[0]["token"] << 8
            bin_inst |= args[1]["token"] << 5
            bin_inst |= inst_def["func"]
            for arg in args[2:]:
                if arg["type"] == "cond":
                    bin_inst |= 1 << 13
        elif inst_type == 'I':
            bin_inst |= 0xc000
            bin_inst |= inst_def["imm_type"] << 11
            bin_inst |= args[0]["token"] << 8
            bin_inst |= args[1]["token"] & 0xff
            for arg in args[2:]:
                if arg["type"] == "cond":
                    bin_inst |= 1 << 13        
        elif inst_type == 'J':
            bin_inst |= 0x4000
            bin_inst |= args[0]["token"] << 8
            bin_inst |= args[1]["token"] << 5
            for arg in args[2:]:
                if arg["type"] == "cond":
                    bin_inst |= 1 << 13   
        elif inst_type == 'F':
            if len(args) == 0:
                bin_inst = 0
            else:
                bin_inst |= args[0]["token"]
                bin_inst |= 1 << 11
                for arg in args[1:]:
                    if arg["type"] == "cond":
                        bin_inst |= 1 << 13
                    if arg["type"] == "inv":
                        bin_inst |= 1 << 8   
        return bin_inst

