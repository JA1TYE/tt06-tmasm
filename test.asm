    SCF Z
    LDI $0,0xa5
    LDI $1,0x22
    ST  $1,0x02
    LDI $0,0x5a
    LD  $1,0x02
    LDI $5,0x00
    LDI $6,0x12
    LDI $3,0x00
    LDI $2,0x10
WAIT_LOOP:
    ADD $2,$3
    SCF C,i
    GOTO $5,$6,c
    LDI $6,INF_LOOP.lo
    LDI $0,0x0f
    LDI $1,GPIO_DIR.lo
    ST  $1,GPIO_DIR.hi
    LDI $0,0xa5
    INC $1,$1
    ST  $1,0xf0
INF_LOOP:
    GOTO $5,$6
VAR GPIO_DIR 0xf000
VAR GPIO_OUT 0xf001