from time import sleep

size = input("Tamanho da tela (Formato: <X,Y>):\n");
size_split = size.split(',');

## Interpretate info
X = int(size_split[0])
Y = int(size_split[1])

empty     = "_";
allocated = "X";

matrix = []


## Generate Matrixes
for i in range(X):
    a = [];
    for j in range(Y):
        a.append(empty)
    matrix.append(a);

print("1. first fit\n"
    + "2. best fit\n"
    + "3. worst fit\n");

enter = input("Enter: ");
if enter == "1" or enter == "first":
    quantity = int(input("Quantidade de memoria a ser alocada: "))
    

    counter = 0
    for i in range(X):
        for j in range(Y):
            if matrix[i][j] == empty:
                counter+=1;
                if counter == quantity:
                    matrix[i][j] = allocated;
                    sleep(.3)
                    print("Memeoria alocada com sucesso!")
            else:
                counter = 0;



elif enter == "2" or enter == "best":
    quantity = input("Quantidade de memoria a ser alocada: ")
elif enter == "3" or enter == "worst":
    quantity = input("Quantidade de memoria a ser alocada: ")
else:
    print("invalid input")
    







## Printing
for i in range(X): 
    for j in range(Y): 
        print(str(matrix[i][j]), end = "|")
    print() 