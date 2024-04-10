class SymbolMapper:
    def __init__(self):
        self.symbol_table = {}
        self.current_address = 0

    def make_symbol_table(self,tokens):
        #enumerate
        for idx,token in enumerate(tokens):
            if token["type"] == "label_def":
                label_name = token["token"]
                label_addr = self.current_address
                symbol = {"symbol_type":"label","symbol_addr":label_addr}
                if label_name in self.symbol_table:
                    raise ValueError("Duplicate label:" + label_name)
                self.symbol_table[label_name] = symbol
                return symbol
            elif token["type"] == "var_def":
                var_name = tokens[idx+1]["token"]
                var_addr = tokens[idx+2]["token"]
                if var_addr < 0 or var_addr > 0xffff:
                    raise ValueError("Invalid variable address:" + str(var_addr))
                symbol = {"symbol_type":"var","symbol_addr":var_addr}
                if var_name in self.symbol_table:
                    raise ValueError("Duplicate variable:" + var_name)
                self.symbol_table[var_name] = symbol
                return symbol
            elif token["type"] == "mnemonic":
                self.current_address += 2
                return None
            else:
                return None
    
    def get_symbol_table(self):
        return self.symbol_table