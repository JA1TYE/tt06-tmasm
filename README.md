# TMASM: Tiny Macro Assembler for tt06-TYE-tiny-cpu
## Description
This is a tiny macro assembler designed for [tt06-TYE-tiny-cpu](https://github.com/JA1TYE/tt06-TYE-tiny-cpu).

### Main feature
- Support variable, label and macro definition
- Support .bin and .txt (for $readmemb) format output
- Instruction and Macro can be defined by YAML format

### How to use it
```sh
>python ./tmasm.py input.asm
```

## Assembly syntax
```C
//Single-line comment
//Variable (alias for data memory region) definition
VAR VARIABLE_NAME 0xfff0
//Label definition
LABEL:
    LDI $0,225//In-line comment is also accepted
    INC $0,$0
    SCF C,Inv//[csvzCSVZ] = Flag argument,Inv = Condition bit inversion
    LDI $6,LABEL.hi//LABEL.hi = Upper byte of LABEL address
    LDI $7,LABEL.lo//LABEL.lo = Lower byte of LABEL address
    GOTO $6,$7,Cond//Cond = Conditional execution enable
    GOTO LABEL,Cond//You can use a label name directly if you define a macro
```

## Instruction definition

```YAML
- mnemonic: "scf"   #define mnemonic
  type: "F"         #define instruction type (used in inst_parser.py)
  flag_bit_11: 1    #Instruction-type specific parameter
  args: ["Flag", "inv", "cond"]  #Arguments(order and type of operands)
```

## Macro definition

```YAML
#You can define macro that has the same mnemonic with original instruction
- mnemonic: "st"
  args: ["Reg", "Symbol"] #Arguments(order and type of operands)
  replace:                #Instructions to be replaced (you can use a macro instruction in the macro definition)
    - "mov %0,$0"
    - "ldi $7,%1.lo"
    - "st  $7,%1.hi"
```