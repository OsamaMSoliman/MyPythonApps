PROG1    START  0000         
         LDX    #0
         LDT    #10
RLOOP    TD     =X'0F'
         JEQ    RLOOP
         RD     =X'F1'
         STCH   RECORD,X
         TIXR   T 
         JLT    RLOOP 
         LTORG
RECORD   RESB   10
         END    PROG1 
                  
