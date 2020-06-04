from time import sleep
from os import system
import random

## Variaveis Globais ##
matrix = []

empty     = "_"
allocated = "X"
temp      = "T"

tempEmpty = "E"
tempEmpty0= "I"

X = 0
Y = 0

max_spc   = 0
empty_spc = max_spc

running   = True
searching = False
##------------------##


def matrix_setup(m):
    size = input("Tamanho da tela (Formato: <X,Y>):\n")
    try:
        size_split = size.split(',')
        x = int(size_split[0])
        y = int(size_split[1])
    except:
        x = 12
        y = 12
    space_maximum = x*y
    space_empty   = space_maximum

    ## Generate Matrixes
    for i in range(y):
        a = []
        for j in range(x):
            a.append("_")
        m.append(a)

    return x, y, space_maximum, space_empty

## Imprimir Matriz
def print_matrix(m, x, y):
    res = ""
    for i in range(y):
        res+="┃"
        for j in range(x): 
            res += str(m[i][j]) + "┃"
        res += '\n'
    return res 


## Atualizar Matriz
def update_temp(m, x, y):
    ## From temporary to allocated
    spaces = 0
    for i in range(y):
        for j in range(x):
            if m[i][j] == tempEmpty:
                m[i][j] = empty
                spaces+=1
            elif m[i][j] == temp:
                m[i][j] = allocated
            elif m[i][j] == empty:
                spaces+=1
    return spaces
    
def verify_worst(m, x, y):
    counter = 0
    highest = 0

    h_X = 0
    h_Y = 0

    for i in range(x):
        for j in range(y):
            if m[i][j] == empty:
                counter+=1
            elif m[i][j] == allocated:
                counter = 0
            if counter > highest:
                counter = highest
                h_X = i
                h_Y = j
    return h_X, h_Y



system('cls')
X, Y, max_spc, empty_spc = matrix_setup(matrix)




## Generate Matrixes
#for i in range(X):
#    a = []
#    for j in range(Y):
#        a.append(empty)
#    matrix.append(a)

while running:
    system('cls')
    print(print_matrix(matrix, X, Y) + f"({empty_spc}/{max_spc} - {round((empty_spc/max_spc)*100, 1)}%)\n")
    

    print("1. First fit\n"
        + "2. Best fit\n"
        + "3. Worst fit\n"
        + "4. Take out memory\n"
        + "--------------------\n\n"
        + "5. Clear matrix\n"
        + "6. Randomize memory\n"
        + "7. Change Size\n"
        + "--------------------\n\n"
        + "0. Exit\n")
    
    enter = input("Enter: ")
    if enter == "1" or enter == "first":
        system('cls')
        print(print_matrix(matrix, X, Y) + f"({empty_spc}/{max_spc} - {round((empty_spc/max_spc)*100, 1)}%)\n")
        quantity = int(input("Quantidade de memoria a ser alocada: "))

        counter = 0
        searching = True
        for i in range(Y):
            for j in range(X):
                if matrix[i][j] == empty:
                    counter+=1
                    if counter == quantity:
                        matrix[i][j] = temp
                        sleep(.3)
                        searching = False
                        break
                elif searching:
                    counter = 0


        ## Fill data
        counter = 0
        while counter < quantity-1: 
            # Nao sei o porque do -1, mas funcionou então está ótimo kk
            for i in range(Y):
                for j in range(X):
                    try:
                        if matrix[i][j] == temp:
                            matrix[prev_i][prev_j] = temp
                        prev_i = i
                        prev_j = j
                    except:
                        counter = quantity
            counter+=1

        if searching:
            print("Escpaco insuficiente.")
            sleep(1)
        empty_spc = update_temp(matrix, X, Y)

    
    
    
    elif enter == "2" or enter == "best":
        system('cls')
        print(print_matrix(matrix, X, Y) + f"({empty_spc}/{max_spc} - {round((empty_spc/max_spc)*100, 1)}%)\n")
        quantity = int(input("Quantidade de memoria a ser alocada: "))

        counter = 0
        counter_offset = 0

        searching = True
        while searching:
            verify_best = 0
            prev_i = 0
            prev_j = 0
            
            next_i = 0
            next_j = 0

            first_i = 0
            first_j = 0

            for i in range(Y):
                for j in range(X):

                    if counter == counter_offset:
                        first_i = i
                        first_j = j

                    if j == X-1:
                        next_j = 0
                        next_i = i+1
                    else:
                        next_j = j+1
                        next_i = i
                    
                    if matrix[i][j] == empty:
                        counter+=1
                    else:
                        counter=counter_offset
                    #if counter == quantity and matrix[next_i][next_j] == empty:
                    #    counter = counter_offset 
                    if counter == quantity and matrix[next_i][next_j] == allocated and searching:
                        counter = counter_offset
                        matrix[first_i][first_j] = temp
                        searching = False
                        break

                    prev_i = i
                    prev_j = j
            counter_offset-=1
                

        counter = 0
        while counter < quantity-1:
            for i in range(Y):
                for j in range(X):
                    if counter == quantity-1:
                        break
                    if j == X-1:
                        next_j = 0
                        next_i = i+1
                    else:
                        next_j = j+1
                        next_i = i

                    try:
                        if matrix[i][j] == temp and matrix[next_i][next_j] == empty:
                            matrix[next_i][next_j] = temp
                            counter+=1
                    except:
                        counter = quantity


                    '''try:
                        if matrix[i][j] == temp:
                            matrix[prev_i][prev_j] = temp
                        prev_i = i
                        prev_j = j
                    except:
                        counter = quantity'''
            counter+=1


        if searching:
            print("Escpaco insuficiente.")
            sleep(1)
        empty_spc = update_temp(matrix, X, Y)



    elif enter == "3" or enter == "worst":
        system('cls')
        quantity = input("Quantidade de memoria a ser alocada: ")
        
        gapX, gapY = verify_worst(matrix, X, Y)

        

        
    elif enter == "4" or enter == "takeout":
        system('cls')
        removing = False
        XY_inicial0  = input("Ponto inicial <X,Y>: ")
        XY_final0    = input("Ponto final <X,Y>: ")

        inicial_split   = XY_inicial0.split(',')
        final_split     = XY_final0.split(',')

        inicial_X = int(inicial_split[0]) -1
        inicial_Y = int(inicial_split[1]) -1

        final_X = int(final_split[0]) -1
        final_Y = int(final_split[1]) -1

        matrix[inicial_X][inicial_Y] = tempEmpty0
        matrix[final_X ][final_Y] = tempEmpty

        if inicial_X == final_X and inicial_Y == final_Y:
            matrix[inicial_X][inicial_Y] = tempEmpty
        else:
            removing = True

        while removing: 
            for i in range(Y):
                for j in range(X):
                    if matrix[i][j] == tempEmpty:
                        if matrix[prev_i][prev_j] == tempEmpty0:
                            matrix[inicial_X][inicial_Y] = tempEmpty
                            removing = False
                            break
                        matrix[prev_i][prev_j] = tempEmpty
                    prev_i = i
                    prev_j = j



        empty_spc = update_temp(matrix, X, Y)

    elif enter == "5" or enter == "clear":
        system('cls')
        for i in range(Y):
            for j in range(X):
                matrix[i][j] = empty
        empty_spc = update_temp(matrix, X, Y)
    elif enter == "6" or enter == "rand":
        system('cls')
        percent = int(input("Porcentagem de alocação(%): "))
        # Transforma em Porcentagem
        filler = max_spc * (percent/100)
        # Preenche a lista
        lst = int(filler) * ["X"] + int(max_spc-filler) * ["_"]
        # Embaralha os valores da lista
        random.shuffle(lst)
        # Reseta a lista/
        matrix = []
        
        # Aplica na matrix
        for i in range(Y):
            a = []
            # Pega as linhas da lista "lst" de acordo com o tamanho da matrix
            for j in range(X*i, X + X*i):
                # Tive de criar uma exceção para o ultimo item pois ele estava dando algum erro desconhecido,
                # portanto ele sempre será um X, acredito que isso não importe muito
                if j != max_spc-1:
                    a.append(lst[j])
                else:
                    a.append("X")
            # Aplica, concatena, uma lista a outra a cada linha.
            matrix.append(a)
        # Atualiza as "labels"
        empty_spc = update_temp(matrix, X, Y)
    elif enter == "7":
        system('cls')
        matrix = []
        X, Y, max_spc, empty_spc = matrix_setup(matrix)
    elif enter == "0" or enter  ==  "exit":
        exit()
    else:
        print("invalid input")
        sleep(.15)
    







