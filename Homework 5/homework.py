import numpy as np

arr = np.array([[1, 2, 3], [5, 7, 9], [2, 4, 6], [7, 7, 7]])

def only_odd(in_arr):
    odd_rows = np.all(in_arr % 2 == 1, axis=1)
    return in_arr[odd_rows]

def checkerboard():
    # 2.1
    board = np.zeros((8,8))
    # 2.2
    board[1::2, 1::2] = 1
    # 2.3
    board[::2, ::2] = 1
    return board

def reverse_checkerboard():
    board = np.ones((8,8))
    board[1::2, 1::2] = 0
    board[::2, ::2] = 0
    return board

def universe_expansion(in_universe, num_spaces):
    result = []
    
    for string in in_universe:
        chars = np.array(list(string))
        spaces = np.full((chars.size - 1,), " " * num_spaces)
        expanded_string = np.char.add(chars[:-1], spaces)
        expanded_string = np.append(expanded_string, chars[-1])
        result.append(''.join(expanded_string))
    
    return np.array(result)

def second_largest(arr):
    second_largest_values = np.partition(arr, -2, axis=0)[-2, :]
    return second_largest_values