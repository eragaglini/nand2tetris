// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)

@SCREEN
D=A
@address
M=D
@8191
D=A
@n
M=D
@i
M=0

@KBD
D=M
@SETVALONE
D;JNE
@SETVALZERO
D;JEQ

(ROW)
@i
D = M
@n
D = D - M
@LOOP
D;JGT		// if i > n goto END

@val
D=M
@address
A = M		// writing to memory using a pointer
M = D	// RAM[address] = -1 (16 pixels)

@i
M = M + 1	// i = i + 1
@address
M = M+1	// address = address + 32
@ROW
0;JMP		// goto LOOP


(SETVALZERO)
@val
M=0
@ROW
0;JMP

(SETVALONE)
@val
M=-1
@ROW
0;JMP
