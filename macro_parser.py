import re
import tokenizer
import tmasm_utils

class MacroParser:
    def __init__(self,macro_def):
        self.tokenizer = tokenizer.Tokenizer()

        # make a macro table
        self.macro_table = tmasm_utils.make_mnemonic_table(macro_def)

        self.temporary_label_index = 0
    

    def expand_macro(self,tokens):
        #serch mached macro
        if tokens[0]["type"] != "mnemonic":
            return [tokens]
        else:
            mnemonic = tokens[0]["token"]
            if mnemonic not in self.macro_table:
                return [tokens]
            else:
                macro = tmasm_utils.search_definition(tokens,self.macro_table)
                if macro is None:#if macro is not found
                    return [tokens]
                else: #if macro is found, expand it
                    new_tokens = self.replace_macro(macro,tokens)
                    return new_tokens

    def replace_macro(self,macro,tokens):
        replaced_tokens = []
        temporary_label_flag = False
        temporary_label_name = ""
        arg_tokens = tmasm_utils.get_arg_tokens(tokens)
        for line in macro["replace"]:
            new_line = line
            #replace %-expressions
            arg_len = len(arg_tokens)
            #In case of %-expression with >= 2-digits, replace from the last one
            for i in reversed(range(arg_len)):
                new_line = new_line.replace("%" + str(i),tmasm_utils.get_arg_text(arg_tokens[i]))
            #if there is @, replace it with a temporary label
            if "@" in new_line:
                if temporary_label_flag == False:
                    temporary_label_name = "~TEMP_"+str(self.temporary_label_index)
                    self.temporary_label_index += 1
                    temporary_label_flag = True
                new_line = new_line.replace("@",temporary_label_name)
            #tokenize new_line and check macro recursively
            new_tokens = self.tokenizer.tokenize(new_line)
            expanded_tokens = self.expand_macro(new_tokens)
            replaced_tokens.extend(expanded_tokens)
        return replaced_tokens

