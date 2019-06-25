import matplotlib.pyplot as plt

def read_coords(filename):
    
    x = open(filename, "r")

    x_moves = []
    y_moves = []
    moves = []
    for line in x:
        if "Up" not in line:
            term = line.split("\t")
            x_moves.append(float(term[3]))
            y_moves.append(float(term[4]))
            moves.append(str(term[5]))

    counter = 0
    for i in moves:
        if i =="touch":
            counter += 1
            
    slices = []
    for number, value in enumerate(moves):
        if value == "touch":
            slices.append(number)
    # to match the dimensions
    slices.append(len(x_moves))

    #creating list of lists for x and y
    list_of_lists_x = [[] for i in range(counter)]
    list_of_lists_y = [[] for i in range(counter)]

    for i in range(0, counter):
        list_of_lists_x[i] = x_moves[slices[i]:slices[i+1]]
    for i in range(0, counter):
        list_of_lists_y[i] = y_moves[slices[i]:slices[i+1]]
        
    #plotting the chunks
    for i in range(0, counter):
        plt.plot(list_of_lists_x[i], list_of_lists_y[i], "k")
    plt.show()
    

filename = "21_5_2019_9_4_4_VP1_Copy.txt"
read_coords(filename)
