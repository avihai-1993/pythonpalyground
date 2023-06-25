
def print_spiral(mat_rect):
    '''

    :param mat_rect:
    :return: void

    print the matrix MxN  in spiral manner start for 0,0

    '''
    rows = len(mat_rect)
    cols = len(mat_rect[0])

    current_cicrcal = {"row_up": 0 , "col_rigt": cols - 1 , "row_bottom" : rows - 1 , "col_left": 0 }
    #print(current_cicrcal)
    while current_cicrcal["row_up"] <= current_cicrcal["row_bottom"] and current_cicrcal["col_left"] <= current_cicrcal["col_rigt"] :

        #left to right basiclly most upper row of ituration
        for i in range(current_cicrcal["row_up"],current_cicrcal["col_rigt"]):
            print("A",mat_rect[current_cicrcal["row_up"]][i])

        #up to bottom basiclly rightest  column of ituration
        for i in range(current_cicrcal["row_up"],current_cicrcal["row_bottom"] + 1):
            print("B",mat_rect[i][current_cicrcal["col_rigt"]])

        if current_cicrcal["row_up"] == current_cicrcal["row_bottom"]: break


        #right to left most lower row of ituration
        for i in range(current_cicrcal["col_rigt"] - 1, current_cicrcal["col_left"] -1  , -1):
            print("C",mat_rect[current_cicrcal["row_bottom"]][i])

        #down to up laftest column in ituration
        for i in range(current_cicrcal["row_bottom"] -1 , current_cicrcal["row_up"] , - 1):
            print("D",mat_rect[i][current_cicrcal["row_up"]])

        current_cicrcal["row_up"]  += 1
        current_cicrcal["col_rigt"] -= 1
        current_cicrcal["col_left"] += 1
        current_cicrcal["row_bottom"] -= 1
        #print(current_cicrcal)




#print(list(range(2,0,-1)))
m = [[3, 2, 1],
     [4, 9, 8],
     [5, 6, 7]]

m1 = [[3, 2, 1 , 0],
     [4, 9, 8 , 0],
     [5, 6, 7 , 8]]

m2 = [[3, 2, 1 , 0],
     [4, 9, 8 , 0],
     [5, 6, 7 , 8],
      [2, 6, 9 , 35]]

m3 = [[3, 2],
     [4, 9,],
     [5, 6,],
      [2, 6,]]

print_spiral(m)
print("_______________")
print_spiral(m1)
print("_______________")
print_spiral(m2)
print("_______________")
print_spiral(m3)