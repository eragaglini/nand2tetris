@256
D=A
@SP
M=D

@RETURN_LABEL0
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=A
@SP
A=M
M=D
@SP
M=M+1

@5
D=A
@0
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

(RETURN_LABEL0)



(Sys.init)



@4000
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@THIS
M=D

@5000
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@THAT
M=D

@RETURN_LABEL1
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=A
@SP
A=M
M=D
@SP
M=M+1

@5
D=A
@0
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

(RETURN_LABEL1)



@SP
M=M-1
A=M
D=M
@6
M=D

(LOOP)




@LOOP
0;JMP

(Sys.main)

@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1


@4001
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@THIS
M=D

@5001
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@THAT
M=D

@200
D=A
@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@LCL
A=M
D=D+A
@LCL
M=D
@SP
M=M-1
A=M
D=M
@LCL
A=M
M=D
@1
D=A
@LCL
A=M
D=A-D
@LCL
M=D

@40
D=A
@SP
A=M
M=D
@SP
M=M+1

@2
D=A
@LCL
A=M
D=D+A
@LCL
M=D
@SP
M=M-1
A=M
D=M
@LCL
A=M
M=D
@2
D=A
@LCL
A=M
D=A-D
@LCL
M=D

@6
D=A
@SP
A=M
M=D
@SP
M=M+1

@3
D=A
@LCL
A=M
D=D+A
@LCL
M=D
@SP
M=M-1
A=M
D=M
@LCL
A=M
M=D
@3
D=A
@LCL
A=M
D=A-D
@LCL
M=D

@123
D=A
@SP
A=M
M=D
@SP
M=M+1

@RETURN_LABEL2
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=A
@SP
A=M
M=D
@SP
M=M+1

@5
D=A
@1
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

(RETURN_LABEL2)



@SP
M=M-1
A=M
D=M
@5
M=D

@0
D=A
@LCL
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@LCL
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@2
D=A
@LCL
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@3
D=A
@LCL
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@4
D=A
@LCL
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D+M
@SP
M=M-1
M=M-1
A=M
M=D
@SP
M=M+1

@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D+M
@SP
M=M-1
M=M-1
A=M
M=D
@SP
M=M+1

@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D+M
@SP
M=M-1
M=M-1
A=M
M=D
@SP
M=M+1

@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D+M
@SP
M=M-1
M=M-1
A=M
M=D
@SP
M=M+1

@LCL
D=M
@FRAME
M=D

@5
A=D-A
D=M
@RET
M=D

@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1@ARG
D=M+1
@SP
M=D

@FRAME
D=M-1
AM=D
D=M
@THAT
M=D

@FRAME
D=M-1
AM=D
D=M
@THIS
M=D

@FRAME
D=M-1
AM=D
D=M
@ARG
M=D

@FRAME
D=M-1
AM=D
D=M
@LCL
M=D


@RET
0;JMP

(Sys.add12)



@4002
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@THIS
M=D

@5002
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@THAT
M=D

@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@12
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D+M
@SP
M=M-1
M=M-1
A=M
M=D
@SP
M=M+1

@LCL
D=M
@FRAME
M=D

@5
A=D-A
D=M
@RET
M=D

@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1@ARG
D=M+1
@SP
M=D

@FRAME
D=M-1
AM=D
D=M
@THAT
M=D

@FRAME
D=M-1
AM=D
D=M
@THIS
M=D

@FRAME
D=M-1
AM=D
D=M
@ARG
M=D

@FRAME
D=M-1
AM=D
D=M
@LCL
M=D


@RET
0;JMP