from time import sleep, time
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
    size = input("Tamanho da tela (Formato: <linhas, colunas>):\n")
    try:
        if ' ' in size:
            size_split = size.split(', ')
            x = int(size_split[0])
            y = int(size_split[1])
        else:
            size_split = size.split(',') ## Só para evitar erros
            x = int(size_split[0])
            y = int(size_split[1])
    except:
        # tamanho padrão, facilitou no debug
        x = 12
        y = 12
    space_maximum = x*y
    space_empty   = space_maximum
    process = 0

    ## Gera as matrizes
    for i in range(y):
        a = []
        print(f"Processando. . . [{(process/y)*100}]") # {(process/y) * 100}
        process+=1
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
            # Substitui os "E"'s ou tempEmpty por "_" ou empty
            if m[i][j] == tempEmpty:
                m[i][j] = empty
                spaces+=1

            # Substitui os "T"'s ou temp por "X" ou allocated
            elif m[i][j] == temp:
                m[i][j] = allocated
            
            # Conta o numero de espaços e retorna pela função
            elif m[i][j] == empty:
                spaces+=1
    return spaces
    

def get_worst(m, x, y):
    counter = 0
    highest = 0

    start_X = 0
    start_Y = 0

    h_X = 0
    h_Y = 0

    for i in range(x):
        for j in range(y):
            if m[i][j] == empty:
                counter+=1
            elif m[i][j] == allocated:
                counter = 0
            if counter == 1:
                start_X = i
                start_Y = j
            if counter > highest:
                highest = counter
                h_X = start_X
                h_Y = start_Y
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
        + "5. Limpar matriz\n"
        + "6. Embaralhar memoria\n"
        + "7. Mudar tamanho\n"
        + "--------------------\n\n"
        + "8. Modo Teste\n"
        + "--------------------\n\n"
        + "0. Sair\n")
    
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
                    # Reseta as coordenadas se o espaço estiver errado
                    if counter == counter_offset:
                        first_i = i
                        first_j = j

                    # Pre-ve as prox coordenadas
                    if j == X-1:
                        next_j = 0
                        next_i = i+1
                    else:
                        next_j = j+1
                        next_i = i
                    
                    # Adiciona no counter, caso esteja um espaço vazio
                    if matrix[i][j] == empty:
                        counter+=1
                    else:
                        counter=counter_offset
                    #if counter == quantity and matrix[next_i][next_j] == empty:
                    #    counter = counter_offset 

                    # Aloca o primeiro temp
                    if counter == quantity and matrix[next_i][next_j] == allocated and searching:
                        counter = counter_offset
                        matrix[first_i][first_j] = temp
                        searching = False
                        break

                    prev_i = i
                    prev_j = j
            # Serve para procurar o tamanho correto, caso não tenha 2, vai para 3 e assim por diante
            counter_offset-=1 
                

        counter = 0
        # Preenche de acordo com a quantidade desejada
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

        # Caso ele encerre todos os loops e não consiga colocar a memoria,
        # vai retornar essa mensagem
        if searching:
            print("Escpaco insuficiente.")
            sleep(1)
        empty_spc = update_temp(matrix, X, Y)

    elif enter == "3" or enter == "worst":
        system('cls')
        print(print_matrix(matrix, X, Y) + f"({empty_spc}/{max_spc} - {round((empty_spc/max_spc)*100, 1)}%)\n")
        quantity = int(input("Quantidade de memoria a ser alocada: "))
        counter = 0
        highest = 0
    
        start_X = 0
        start_Y = 0
    
        h_X = 0
        h_Y = 0

        # Procura o maior lugar vazio possivel e coloca um caractere no inicio
        # para identificar onde deve começar a colocar os valores
        if empty_spc < quantity:
            empty_spc = update_temp(matrix, X, Y)
        for i in range(X):
            for j in range(Y):
                if matrix[i][j] == empty:
                    counter+=1
                elif matrix[i][j] == allocated:
                    counter = 0
                if counter == 1:
                    start_X = i
                    start_Y = j
                if counter > highest:
                    highest = counter
                    h_X = start_X
                    h_Y = start_Y
        matrix[h_X][h_Y] = temp

        # Procura o caractere "temp" e subsitui os proximos baseado na quantity colocada.
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
            counter+=1


        empty_spc = update_temp(matrix, X, Y)
        
    elif enter == "4" or enter == "takeout":
        # O takeout recebe como parametro duas coordenadas.
        # Toda a memoria que esta dentro delas ele vai esvaziar,
        # idependentemente se elas foram alocadas juntas ou não.
        
        system('cls')
        removing = False
        print(print_matrix(matrix, X, Y) + f"({empty_spc}/{max_spc} - {round((empty_spc/max_spc)*100, 1)}%)\n")
        
        # Ponto Inicial
        XY_inicial0  = input("Ponto inicial <linha,coluna>: ")
        # Ponto Final
        XY_final0    = input("Ponto final <linha,coluna>: ")

        # Faz a divisão do texto das coordenadas
        inicial_split   = XY_inicial0.split(',')
        final_split     = XY_final0.split(',')

        # Transforma os textos em variaveis de numero inteiro
        inicial_X = int(inicial_split[0]) -1
        inicial_Y = int(inicial_split[1]) -1
        final_X = int(final_split[0]) -1
        final_Y = int(final_split[1]) -1

        # Seta os pontos inicial e final, na matriz
        matrix[inicial_X][inicial_Y] = tempEmpty0
        matrix[final_X ][final_Y] = tempEmpty

        # Evitando erros, caso o inical seja o mesmo que o final.
        if inicial_X == final_X and inicial_Y == final_Y:
            matrix[inicial_X][inicial_Y] = tempEmpty
        else:
            removing = True

        # Seta todos os dentro da range inicial ao final como temp empty.
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
        

        # Faz um update, setando o tempEmpty como "_"
        empty_spc = update_temp(matrix, X, Y)

    elif enter == "5" or enter == "clear":
        system('cls')
        for i in range(Y):
            for j in range(X):
                matrix[i][j] = empty
        empty_spc = update_temp(matrix, X, Y)
    
    elif enter == "6" or enter == "rand":
        system('cls')
        print("Digite \'0\' para cancelar a operacao")
        percent = int(input("Porcentagem de alocacao(%): "))
        if percent == 0:
            empty_spc = update_temp(matrix, X, Y)
        else:
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
    
    elif enter == "8":
        system('cls')
        enter = input("Atencao!\nEste modo pode exigir muito do seu processamento e memoria\nDeseja continuar?(S/N)\n\n")
        if enter.lower() == "sim" or enter.lower() == "s":
            
            # !--Variaveis para o modo teste--!
            x = 5000
            y = 5000
            num_alocacoes = 1000000

            system('cls')
            '''x = int(input("Numero de linhas: "))
            y = int(input("Numero de colunas: "))
            num_alocacoes = int(input("Numero de alocacoes: "))
            system('cls')'''


            start = time()

            

            space_maximum = x*y
            space_empty   = space_maximum
            
            max_spc = space_maximum
            empty_spc = x*y

            X = x
            Y = y

            process = 0

            ## Gera as matrizes
            matrix = []
            for i in range(y):
                a = []
                print(f"Processando. . . [{round((process/y)*100, 1)}]") # {(process/y) * 100}
                process+=1
                for j in range(x):
                    a.append("_")
                matrix.append(a)
            system('cls')
            c = 1
            falha_alocacao = 0
            while c < num_alocacoes:
            #while c < 1000000:

                fit = random.randint(0,2)
                quantity = random.randint(1,5000)
                
                # FIRST FIT
                if fit == 0:
                    print(f"[{c}/{num_alocacoes}] - First Fit - ({round(time() - start, 2)}s)")
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
                        falha_alocacao += 1
                    empty_spc = update_temp(matrix, X, Y)

                # BEST FIT
                elif fit == 1:
                    print(f"[{c}/{num_alocacoes}] - Best Fit - ({round(time() - start, 2)}s)")
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
                                # Reseta as coordenadas se o espaço estiver errado
                                if counter == counter_offset:
                                    first_i = i
                                    first_j = j
            
                                # Pre-ve as prox coordenadas
                                if j == X-1:
                                    next_j = 0
                                    next_i = i+1
                                else:
                                    next_j = j+1
                                    next_i = i
                                
                                # Adiciona no counter, caso esteja um espaço vazio
                                if matrix[i][j] == empty:
                                    counter+=1
                                else:
                                    counter=counter_offset
                                
                                if counter == empty_spc:
                                    counter_offset = (counter_offset-empty_spc) + quantity
                                
                                #if counter == quantity and matrix[next_i][next_j] == empty:
                                #    counter = counter_offset 
            
                                # Aloca o primeiro temp
                                if counter == quantity and searching:
                                    counter = counter_offset
                                    matrix[first_i][first_j] = temp
                                    searching = False
                                    break
            
                                prev_i = i
                                prev_j = j
                        # Serve para procurar o tamanho correto, caso não tenha 2, vai para 3 e assim por diante
                        counter_offset-=1 
                            
            
                    counter = 0
                    # Preenche de acordo com a quantidade desejada
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
            
                    # Caso ele encerre todos os loops e não consiga colocar a memoria,
                    # vai retornar essa mensagem
                    if searching:
                        falha_alocacao += 1
                    empty_spc = update_temp(matrix, X, Y)

                # WORST FIT
                else:
                    print(f"[{c}/{num_alocacoes}] - Worst Fit - ({round(time() - start, 2)}s)")
                    counter = 0
                    highest = 0
                
                    start_X = 0
                    start_Y = 0
                
                    h_X = 0
                    h_Y = 0
            
                    # Procura o maior lugar vazio possivel e coloca um caractere no inicio
                    # para identificar onde deve começar a colocar os valores
                    if empty_spc < quantity:
                        falha_alocacao +=1
                        empty_spc = update_temp(matrix, X, Y)

                    for i in range(X):
                        for j in range(Y):
                            if matrix[i][j] == empty:
                                counter+=1
                            elif matrix[i][j] == allocated:
                                counter = 0
                            if counter == 1:
                                start_X = i
                                start_Y = j
                            if counter > highest:
                                highest = counter
                                h_X = start_X
                                h_Y = start_Y
                    matrix[h_X][h_Y] = temp
            
                    # Procura o caractere "temp" e subsitui os proximos baseado na quantity colocada.
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
                        counter+=1
                    empty_spc = update_temp(matrix, X, Y)
               
                c+=1
            print("\n\nTeste finalizado com sucesso!\n"
                +f"Numero de alocacoes: {c}\n"
                +f"Numero de alocacoes BEM-SUCEDIDAS: {c - falha_alocacao}\n"
                +f"Numero de alocacoes MALSUCEDIDAS:  {falha_alocacao}\n"
                + "Tempo elapsado:", round(time() - start, 2), "s\n")
            input("Pressione qualquer tecla para continuar")
            empty_spc = update_temp(matrix, X, Y)
            X, Y, max_spc, empty_spc = matrix_setup(matrix)
        else:
            empty_spc = update_temp(matrix, X, Y)

    elif enter == "0" or enter  ==  "exit":
        exit()
    else:
        print("invalid input")
        sleep(.15)









