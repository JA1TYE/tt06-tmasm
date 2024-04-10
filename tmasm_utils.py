def check_match_args(arg_def,arg_in):
    if len(arg_def) < len(arg_in):
        return False
    check_len = len(arg_def)
    idx_def = 0
    idx_in = 0
    while idx_def < check_len:
        if idx_in < len(arg_in) and arg_def[idx_def].lower() == arg_in[idx_in].lower():
            idx_def += 1
            idx_in += 1
        elif arg_def[idx_def][0].islower():#if arg_def[idx_def] is a optional argument
            idx_def += 1
        else:#if arg_def[idx_def] is a required argument and it isn't matched with arg_in[idx_in]
            return False
    if idx_in < len(arg_in):
        return False
    return True

def search_definition(tokens,search_table):
    #search definition that is matched with tokens
    if tokens[0]["type"] == "mnemonic" and tokens[0]["token"] in search_table:
        for definition in search_table[tokens[0]["token"]]:
            arg_types = get_arg_types(tokens)
            if check_match_args(definition["args"],arg_types):
                return definition
    return None

def make_mnemonic_table(definitions):
    # make a open-hash table that have a mnemonic as a key 
    mnemonic_table = {}
    for definition in definitions:
        if definition["mnemonic"] in mnemonic_table:
            mnemonic_table[definition["mnemonic"]].append(definition)
        else:
            mnemonic_table[definition["mnemonic"]] = [definition] 
    return mnemonic_table

def get_arg_types(tokens):
    arg_types = []
    for token in tokens:
        if token["type"] in ["symbol","symbol_hi","symbol_lo","reg","imm","cond","inv","flag"]:
            arg_types.append(token["type"])
    return arg_types

def get_arg_tokens(tokens):
    arg_tokens = []
    for token in tokens:
        if token["type"] in ["symbol","symbol_hi","symbol_lo","reg","imm","cond","inv","flag"]:
            arg_tokens.append(token)
    return arg_tokens

def get_arg_text(token):
    if token["type"] == "symbol":
        return token["token"]
    elif token["type"] == "symbol_hi":
        return token["token"]+".hi"
    elif token["type"] == "symbol_lo":
        return token["token"]+".lo"
    elif token["type"] == "reg":
        return "$"+str(token["token"])
    elif token["type"] == "imm":
        return str(token["token"])
    elif token["type"] == "cond":
        if token["token"] == 1:
            return "cond"
        return ""
    elif token["type"] == "inv":
        if token["token"] == 1:
            return "inv"
        return ""
    elif token["type"] == "flag":
        flag_str = ""
        if token["token"] & 0x01:
            flag_str += "z"
        if token["token"] & 0x02:
            flag_str += "v"
        if token["token"] & 0x04:
            flag_str += "s"
        if token["token"] & 0x08:
            flag_str += "c"
        return flag_str

def print_tokens(tokens):
    for token in tokens:
        print(token)

def print_symbol_table(symbol_table):
    for symbol in symbol_table:
        print(symbol + ":" + str(symbol_table[symbol]))

# symbol name that starts with "~" is a temporary label
# so, if there is a temporary label in tokens before macro expansion,
# these tokens are invalid
def check_tilda_symbol(tokens):
    for token in tokens:
        if token["type"] == "symbol" and token["token"][0] == "~":
            return True
        if token["type"] == "symbol_hi" and token["token"][0] == "~":
            return True
        if token["type"] == "symbol_lo" and token["token"][0] == "~":
            return True
        if token["type"] == "label_def" and token["token"][0] == "~":
            return True
        if token["type"] == "var_name" and token["token"][0] == "~":
            return True
    return False