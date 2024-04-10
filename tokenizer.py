import re

class Tokenizer:
    
    def tokenize(self,line):
        #remove comment
        comment = ""
        comment_pos = line.find("//")
        if comment_pos != -1:
            comment = line[comment_pos:].strip()
            line = line[:comment_pos]
        #tokenize
        line = line.strip().replace(',', ' ')
        tokens_temp = line.split()
        tokens = []
        before = None
        for i,token in enumerate(tokens_temp):
            if self.is_var_def(token,before):
                tmp = {"type":"var_def","token":True}
                tokens.append(tmp)
                before = tmp
            elif self.is_var_name(token,before):
                tmp = {"type":"var_name","token":token}
                tokens.append(tmp)
                before = tmp
            elif self.is_var_addr(token,before):
                tmp = {"type":"var_addr","token":int(token,0)}
                tokens.append(tmp)
                before = tmp
            elif self.is_cond(token):
                tmp = {"type":"cond","token":True}
                tokens.append(tmp)
                before = tmp
            elif self.is_inv(token):
                tmp = {"type":"inv","token":True}
                tokens.append(tmp)
                before = tmp
            elif self.is_flag(token):
                tmp = {"type":"flag","token":self.str_to_flag(token.lower())}
                tokens.append(tmp)
                before = tmp
            elif self.is_label_def(token):
                tmp = {"type":"label_def","token":token.replace(":","")}
                tokens.append(tmp)
                before = tmp
            elif self.is_symbol(token,before):
                tmp = {"type":"symbol","token":token}
                tokens.append(tmp)
                before = tmp
            elif self.is_symbol_hi(token,before):
                tmp = {"type":"symbol_hi","token":token[:-3]}
                tokens.append(tmp)
                before = tmp
            elif self.is_symbol_lo(token,before):
                tmp = {"type":"symbol_lo","token":token[:-3]}
                tokens.append(tmp)
                before = tmp
            elif self.is_mnemonic(token,before):
                tmp = {"type":"mnemonic","token":token.lower()}
                tokens.append(tmp)
                before = tmp
            elif self.is_reg(token):
                reg_num = int(token[1:])
                tmp = {"type":"reg","token":reg_num}
                tokens.append(tmp)
                before = tmp
            elif self.is_imm(token):
                imm_num = int(token,0)
                tmp = {"type":"imm","token":imm_num}
                tokens.append(tmp)
                before = tmp
            else:
                print(tokens)
                raise ValueError("Invalid token:" + token)
        if comment != "":
            tokens.append({"type":"comment","token":comment})
        return tokens

    def is_var_def(self,token,before):
        if token.lower() == "var" and before is None:
            return True
        return False
    
    def is_var_name(self,token,before):
        if not token.endswith(":") and not token[0].isdecimal():
            if before is not None and before["type"] == "var_def":
                return True
        return False

    def is_var_addr(self,token,before):
        if before is not None and before["type"] == "var_name":
            if re.match(r'^0x[0-9a-fA-F]{1,4}$', token) is not None:
                return True
            elif token.isdecimal() and int(token) < 0x10000:
                return True
        return False

    def is_cond(self,token):
        if token.lower() == "cond":
            return True
        return False

    def is_inv(self,token):
        if token.lower() == "inv":
            return True
        return False

    def is_flag(self,token):
        if re.match(r'^[csvzCSVZ]{1,4}$', token) is not None:
            return True
        else:
            return False

    def is_label_def(self,token):
        if token.endswith(':') and not token[0].isdecimal():
            return True
        return False
    
    def is_symbol(self,token,before):
        if re.match(r'^~?\w*$', token) is not None:
            if before is not None and before["type"] != "var_def"\
                and not token[0].isdecimal():
                return True
        return False

    def is_symbol_hi(self,token,before):
        if token.endswith(".hi"):
            if not token.endswith(":") and before is not None and not token[0].isdecimal():
                return True
        return False

    def is_symbol_lo(self,token,before):
        if token.endswith(".lo"):
            if not token.endswith(":") and before is not None and not token[0].isdecimal():
                return True
        return False
    
    def is_mnemonic(self,token,before):
        if not token.endswith(":") and before is None and token.isalnum() and not token[0].isdecimal():
            return True
        return False
    
    def is_reg(self,token):
        if token.startswith("$") and token[1:].isdecimal():
            if int(token[1:]) < 8 and int(token[1:]) >= 0:
                return True
        return False

    def is_imm(self,token):
        if re.match(r'^0x[0-9a-fA-F]{1,2}$', token) is not None:
            return True
        elif token.isdecimal() and int(token) < 256 and int(token) >= -128:
            return True
        else:
            return False
    
    def str_to_flag(self,s):
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

