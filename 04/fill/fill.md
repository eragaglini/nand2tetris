while True:

    address = RAM[SCREEN]

    k = RAM[KBD]
    
    if k != 0:
        v = -1
    else:
        v = 0

    columns = 16

    i = 0

    while i < columns:

        rows = 256
        j = 0

        while j < rows:
            RAM[address] = v

            j += 1
        i+=1