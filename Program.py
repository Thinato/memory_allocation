from time import sleep
from os import system

## Printing
def print_matrix(m, x, y):
    res = ""
    for i in range(x):
        res+="┃";
        for j in range(y): 
            res += str(m[i][j]) + "┃"
        res += '\n';
    return res 

def update_temp(m, x, y):
    ## From temporary to allocated
    spaces = 0
    for i in range(x):
        for j in range(y):
            if m[i][j] == temp:
                m[i][j] = allocated;
            elif m[i][j] == empty:
                spaces+=1
    return spaces;
    





system('cls')
size = input("Tamanho da tela (Formato: <X,Y>):\n");
try:
    size_split = size.split(',');
    X = int(size_split[0]);
    Y = int(size_split[1]);
except:
    X = 12;
    Y = 12;

## Interpretate info
empty     = "_";
allocated = "X";
temp      = "T";
running   = True;
max_spc   = X*Y;
empty_spc = max_spc;


matrix = []

## Generate Matrixes
for i in range(X):
    a = [];
    for j in range(Y):
        a.append(empty)
    matrix.append(a);

while running:
    system('cls')
    print(print_matrix(matrix, X, Y) + f"({empty_spc}/{max_spc} - {round((empty_spc/max_spc)*100, 1)}%)\n");
    

    print("1. first fit\n"
        + "2. best fit\n"
        + "3. worst fit\n"
        + "4. clear matrix\n");
    
    enter = input("Enter: ");
    if enter == "1" or enter == "first":
        system('cls')
        print(print_matrix(matrix, X, Y) + f"({empty_spc}/{max_spc} - {round((empty_spc/max_spc)*100, 1)}%)\n");
        quantity = int(input("Quantidade de memoria a ser alocada: "))

        counter = 0
        for i in range(X):
            for j in range(Y):
                if matrix[i][j] == empty:
                    counter+=1;
                    if counter == quantity:
                        matrix[i][j] = temp;
                        sleep(.3)
                        break;
                else:
                    counter = 0;


        ## Fill data
        counter = 0
        while counter < quantity-1: 
            # Nao sei o porque do -1, mas funcionou então está ótimo kk
            for i in range(X):
                for j in range(Y):
                    try:
                        if matrix[i][j] == temp:
                            matrix[prev_i][prev_j] = temp;
                        prev_i = i;
                        prev_j = j;
                    except:
                        counter = quantity
            counter+=1


        empty_spc = update_temp(matrix, X, Y);

    
    
    
    elif enter == "2" or enter == "best":
        system('cls')
        quantity = input("Quantidade de memoria a ser alocada: ")
    elif enter == "3" or enter == "worst":
        system('cls')
        quantity = input("Quantidade de memoria a ser alocada: ")
    elif enter == "4" or enter == "clear":
        system('cls')
        for i in range(X):
            for j in range(Y):
                matrix[i][j] = empty;
        update_temp(matrix, X, Y);
    else:
        print("invalid input")
    
    







