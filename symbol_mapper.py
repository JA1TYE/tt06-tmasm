class SymbolMapper:
    def __init__(self,inst_def):
        self.symbol_table = {}
        self.inst_def = inst_def
        self.current_address = 0

    def make_symbol_table(self,line):
        line = line.replace(',', ' ')
        tokens = line.split()
        #check if the line is a label or variable definition
        if tokens[0].lower() in self.inst_def:
            self.current_address += 2
            return None
        elif tokens[0].endswith(':'):
            if "." in tokens[0]:
                raise ValueError("Invalid label:" + tokens[0])
            label_name = tokens[0][:-1]
            label_addr = self.current_address
            symbol = {"symbol_type":"label","symbol_addr":label_addr}
            if label_name in self.symbol_table:
                raise ValueError("Duplicate label:" + label_name)
            self.symbol_table[label_name] = symbol
            return symbol
        elif tokens[0].lower() == "var":
            if "." in tokens[1]:
                raise ValueError("Invalid variable name:" + tokens[1])
            var_name = tokens[1]
            var_addr = int(tokens[2],0)
            if var_addr < 0 or var_addr > 0xffff:
                raise ValueError("Invalid variable address:" + str(var_addr))
            symbol = {"symbol_type":"var","symbol_addr":var_addr}
            if var_name in self.symbol_table:
                raise ValueError("Duplicate variable:" + var_name)
            self.symbol_table[var_name] = symbol
            return symbol
        else:
            raise ValueError("Invalid line:" + line)
    
    def get_symbol_table(self):
        return self.symbol_table

    def dump_symbol_table(self):
        for key in self.symbol_table:
            print(key + ":" + str(self.symbol_table[key]))