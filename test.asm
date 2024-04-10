//Instruction set test
VAR GPIO_DIR 0xf000
VAR GPIO_OUT 0xf001
INIT_GPIO:
    LDI $1,0xff
    LDI $2,0x0
    ST  $1,GPIO_DIR
    ST  $2,GPIO_OUT
SLR_TEST:
    LDI $1,0x01
    LDI $2,0x00
    SLR $1,$2
    ST  $2,GPIO_OUT
SLL_TEST:
    LDI $1,0x01
    LDI $2,0x00
    SLL $1,$2
    ST  $2,GPIO_OUT
INC_TEST:
    LDI $1,0x01
    LDI $2,0x00
    INC $1,$2
    ST  $2,GPIO_OUT
DEC_TEST:
    LDI $1,0x01
    LDI $2,0x00
    DEC $1,$2
    ST  $2,GPIO_OUT
ADD_TEST:
    LDI $1,0x01
    LDI $2,0x00
    ADD $1,$2
    ADD $1,$2
    ST  $2,GPIO_OUT
NOT_TEST:
    LDI $1,0x01
    LDI $2,0x00
    NOT $1,$2
    ST  $2,GPIO_OUT
AND_TEST:
    LDI $1,0xaa
    LDI $2,0xa5
    AND $1,$2
    ST  $2,GPIO_OUT
OR_TEST:
    LDI $1,0xaa
    LDI $2,0xa5
    OR  $1,$2
    ST  $2,GPIO_OUT
XOR_TEST:
    LDI $1,0xaa
    LDI $2,0xa5
    XOR $1,$2
    ST  $2,GPIO_OUT
MOV_TEST:
    LDI $1,0xaa
    LDI $2,0xa5
    XOR $1,$2
    ST  $2,GPIO_OUT
GOTO_TEST:
    LDI $1,0x00
    GOTO GOTO_END
    LDI $1,0xff
GOTO_END:
    ST  $1,GPIO_OUT
LOAD_TEST:
    LDI $1,0x01
LOAD_TEST2:
    LD  $1,GPIO_OUT.hi
    NOT $0,$0
    ST  $0,GPIO_OUT