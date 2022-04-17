def solver(arr):

    # Horizontal
    for row in arr:
        if (row[0] == row[1] == row[2]) and (row[0] != "E"):
            return f"{row[0]} Wins!"

    # Vertical
    for i in range(3):
        if (arr[0][i] == arr[1][i] == arr[2][i]) and (arr[0][i] != "E"):
            return f"{arr[0][i]} Wins!"

    # Diagonal
    if (arr[0][0] == arr[1][1] == arr[2][2]) and (arr[0][0] != "E"):
        return f"{arr[0][0]} Wins!"

    if (arr[0][2] == arr[1][1] == arr[2][0]) and (arr[0][2] != "E"):
        return f"{arr[0][2]} Wins!"
        
    return -1