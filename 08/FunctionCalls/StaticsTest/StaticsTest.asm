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



(Class1.set)



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

@SP
M=M-1
A=M
D=M
@StaticsTest.0
M=D

@1
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

@SP
M=M-1
A=M
D=M
@StaticsTest.1
M=D

@0
D=A
@SP
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

(Class1.get)



@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1

@StaticsTest.1
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
D=D-M
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

@256
D=A
@SP
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



(Sys.init)



@6
D=A
@SP
A=M
M=D
@SP
M=M+1

@8
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
@2
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

@23
D=A
@SP
A=M
M=D
@SP
M=M+1

@15
D=A
@SP
A=M
M=D
@SP
M=M+1

@RETURN_LABEL3
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
@2
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

(RETURN_LABEL3)



@SP
M=M-1
A=M
D=M
@5
M=D

@RETURN_LABEL4
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

(RETURN_LABEL4)



@RETURN_LABEL5
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

(RETURN_LABEL5)



(WHILE)




@WHILE
0;JMP

@256
D=A
@SP
M=D

@RETURN_LABEL6
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

(RETURN_LABEL6)



(Class2.set)



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

@SP
M=M-1
A=M
D=M
@StaticsTest.0
M=D

@1
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

@SP
M=M-1
A=M
D=M
@StaticsTest.1
M=D

@0
D=A
@SP
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

(Class2.get)



@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1

@StaticsTest.1
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
D=D-M
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